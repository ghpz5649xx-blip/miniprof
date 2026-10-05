"""Contrôle d'un module HTML (modules/<id>.html), avant de le publier.

Usage :
    python tools/check_html.py modules/<id>.html [autres.html …]
    python tools/check_html.py --llm modules/<id>.html   # texte de correction pour le LLM

Pourquoi : un module HTML est une page générée par un LLM, avec son propre JS,
servie sur le même site que la progression des enfants (localStorage). On ne
relit pas ce JS ligne à ligne : on vérifie le contrat (docs/module-html.md) et
on refuse tout ce qui pourrait faire sortir des données ou abîmer le journal.

Ce contrôle n'est pas une preuve de sécurité (on peut toujours contourner une
recherche de texte) : c'est un garde-fou contre les erreurs du LLM, pas contre
un attaquant. Le contenu vient du parent, sans tiers.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from common import load_schema

SCHEMA = load_schema()
ID_MODULE = re.compile(SCHEMA["properties"]["id"]["pattern"])
ID_COMPETENCE = re.compile(SCHEMA["$defs"]["identifiant"]["pattern"])
MATIERES = SCHEMA["properties"]["subject"]["enum"]
NIVEAUX = SCHEMA["properties"]["level"]["enum"]
CHAMPS_FICHE = ["id", "title", "subject", "level", "description", "skills"]

FICHE = re.compile(
    r'<script\s+type="application/json"\s+id="miniprof-module"\s*>(.*?)</script>', re.DOTALL)
# Politique de sécurité obligatoire, recopiée telle quelle dans chaque page.
# connect-src 'none' : le navigateur bloque toute requête (fetch, XHR, beacon…),
# même écrite de façon que la recherche de texte ci-dessous ne verrait pas.
# 'unsafe-inline' : la page générée a son script et ses styles dans le fichier.
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; connect-src 'none'; object-src 'none'; frame-src 'none'; "
       "base-uri 'none'; form-action 'none'")
BALISE_CSP = f'<meta http-equiv="Content-Security-Policy" content="{CSP}">'

SUIVI = re.compile(r'<script\s+type="module"\s+src="\.\./js/suivi\.js"\s*>\s*</script>')
APPEL_SUIVI = re.compile(r"miniprof\.reponse\s*\(")

# (motif, explication pour le LLM). Les URL de namespace SVG/XML
# (http://www.w3.org/…) sont autorisées : ce sont des noms, pas des requêtes.
INTERDITS = [
    (r"\bfetch\s*\(", "pas de fetch() : la page ne doit rien télécharger"),
    (r"XMLHttpRequest|WebSocket|EventSource|sendBeacon", "pas de requête réseau"),
    (r"\bimport\s*\(", "pas d'import() dynamique"),
    (r"https?://(?!www\.w3\.org/)", "aucune URL externe (polices, images, scripts) : "
                                   "polices système, images en SVG dans la page"),
    (r"""(?:src|href)\s*=\s*["']//""", "aucune URL externe (adresse commençant par //)"),
    (r"localStorage|sessionStorage|indexedDB|document\.cookie",
     "pas d'accès direct au stockage : utiliser miniprof.reponse() (js/suivi.js)"),
    (r"<iframe|<object|<embed", "pas de page ou d'objet intégré"),
    (r"serviceWorker|new\s+Worker", "pas de worker"),
]


class Rapport:
    def __init__(self):
        self.erreurs = []
        self.fiche = None

    @property
    def valide(self):
        return not self.erreurs


def lire_fiche(texte, rapport):
    """Renvoie la fiche du module (dict) ou None, en notant les erreurs."""
    trouve = FICHE.findall(texte)
    if len(trouve) != 1:
        rapport.erreurs.append(
            'fiche : il faut exactement un <script type="application/json" id="miniprof-module"> '
            f"(trouvé : {len(trouve)})")
        return None
    try:
        fiche = json.loads(trouve[0])
    except json.JSONDecodeError as e:
        rapport.erreurs.append(f"fiche : JSON invalide ({e})")
        return None
    if not isinstance(fiche, dict):
        rapport.erreurs.append("fiche : doit être un objet JSON")
        return None

    for champ in CHAMPS_FICHE:
        if champ not in fiche:
            rapport.erreurs.append(f"fiche.{champ} : champ obligatoire manquant")
    for champ in ("title", "description"):
        if champ in fiche and (not isinstance(fiche[champ], str) or not fiche[champ].strip()):
            rapport.erreurs.append(f"fiche.{champ} : texte non vide attendu")
    if "id" in fiche and not (isinstance(fiche["id"], str) and ID_MODULE.match(fiche["id"])):
        rapport.erreurs.append("fiche.id : minuscules sans accents et tirets (ex. sciences-cm1-circuit-electrique)")
    if "subject" in fiche and fiche["subject"] not in MATIERES:
        rapport.erreurs.append(f"fiche.subject : une valeur parmi {', '.join(MATIERES)}")
    if "level" in fiche and fiche["level"] not in NIVEAUX:
        rapport.erreurs.append(f"fiche.level : une valeur parmi {', '.join(NIVEAUX)}")

    skills = fiche.get("skills")
    if "skills" in fiche:
        if not isinstance(skills, list) or not skills:
            rapport.erreurs.append("fiche.skills : liste non vide de { id, label } attendue")
        else:
            vus = set()
            for i, s in enumerate(skills):
                ou = f"fiche.skills[{i}]"
                if not isinstance(s, dict) or set(s) != {"id", "label"}:
                    rapport.erreurs.append(f"{ou} : objet {{ id, label }} attendu")
                    continue
                if not (isinstance(s["id"], str) and ID_COMPETENCE.match(s["id"])):
                    rapport.erreurs.append(f"{ou}.id : minuscules, chiffres, _ ou -")
                elif s["id"] in vus:
                    rapport.erreurs.append(f"{ou}.id : « {s['id']} » est en double")
                vus.add(s["id"])
                if not isinstance(s["label"], str) or not s["label"].strip():
                    rapport.erreurs.append(f"{ou}.label : texte non vide attendu")
    return fiche


def verifier_texte(texte, nom_fichier):
    rapport = Rapport()
    fiche = lire_fiche(texte, rapport)
    rapport.fiche = fiche
    if fiche and isinstance(fiche.get("id"), str) and nom_fichier != fiche["id"] + ".html":
        rapport.erreurs.append(f"fichier : doit s'appeler « {fiche['id']}.html »")
    if BALISE_CSP not in texte:
        rapport.erreurs.append(f"sécurité : recopier tel quel dans <head> : {BALISE_CSP}")
    if not SUIVI.search(texte):
        rapport.erreurs.append('suivi : charger <script type="module" src="../js/suivi.js"></script>')
    if not APPEL_SUIVI.search(texte):
        rapport.erreurs.append("suivi : la page doit enregistrer les réponses avec miniprof.reponse(…)")
    # Ligne par ligne : le numéro de ligne aide le LLM à retrouver le fautif.
    for motif, explication in INTERDITS:
        for n, ligne in enumerate(texte.splitlines(), 1):
            if re.search(motif, ligne):
                rapport.erreurs.append(f"ligne {n} : {explication}")
    return rapport


def verifier_fichier(path):
    path = Path(path)
    return verifier_texte(path.read_text(encoding="utf-8"), path.name)


def texte_llm(rapport):
    """Message à recopier tel quel au LLM (même forme que validate.py --llm)."""
    if rapport.valide:
        return "Aucune erreur : rien à renvoyer au LLM."
    return "\n".join([
        "Ta page HTML ne respecte pas le contrat miniprof (docs/module-html.md) :",
        "",
        *[f"- {e}" for e in rapport.erreurs],
        "",
        "Corrige uniquement ces points, sans changer l'id du module ni des compétences, "
        "puis renvoie la page complète.",
    ])


def main():
    parser = argparse.ArgumentParser(description="Contrôle un module HTML miniprof.")
    parser.add_argument("pages", nargs="+", help="fichier(s) modules/<id>.html")
    parser.add_argument("--llm", action="store_true", help="texte de correction pour le LLM")
    args = parser.parse_args()

    tout_ok = True
    for page in args.pages:
        rapport = verifier_fichier(page)
        tout_ok = tout_ok and rapport.valide
        if args.llm:
            print(texte_llm(rapport))
        elif rapport.valide:
            print(f"✔ {page} : conforme au contrat")
        else:
            print(f"✘ {page} : {len(rapport.erreurs)} erreur(s)")
            for e in rapport.erreurs:
                print(f"  - {e}")
    sys.exit(0 if tout_ok else 1)


if __name__ == "__main__":
    main()
