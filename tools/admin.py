"""Écran d'admin du projet, sur le Mac seulement (plan P014).

    python3 tools/admin.py

Lance un petit serveur sur 127.0.0.1 et ouvre la page dans le navigateur. Le sponsor y gère ses
tâches, les idées, les consignes à l'agent et lit les plans. Chaque enregistrement réécrit une
section de `pilotage.md` ou de `plans/index.md`, puis committe et pousse : l'agent lit ces
fichiers en début de session, y compris dans une session cloud.

Pourquoi un serveur local et pas une page de l'app : le site est public (accessible depuis
l'iPhone) et ce qu'on saisit dans une page reste dans le navigateur, illisible pour l'agent.
Ce serveur n'écoute que sur le Mac et ne fait pas partie de l'app des enfants.

Bibliothèque standard seulement : rien à installer.
"""

import datetime
import http.server
import json
import re
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = Path(__file__).resolve().parent / "admin" / "page.html"
PORT = 8642  # fixe, pour pouvoir mettre l'écran en favori

PILOTAGE = "pilotage.md"
INDEX = "plans/index.md"
SECTION_TACHES = "Tâches du sponsor"
SECTION_CONSIGNES = "Consignes pour Claude"
SECTION_IDEES = "Idées (sans fiche)"
PRIORITES = ("haute", "moyenne", "basse")

MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin",
        "juil.", "août", "sept.", "oct.", "nov.", "déc."]

# Une ligne par élément : c'est ce format que l'agent lit et que le sponsor peut corriger à la main.
RE_TACHE = re.compile(r"^- \*\*(.+?)\*\* — (.+)$")
RE_IDEE = re.compile(r"^- \*\*(.+?)\*\* \(depuis le (.+?), priorité (haute|moyenne|basse)\) : (.+)$")


class ErreurFormat(Exception):
    """Une ligne écrite à la main n'a pas le format attendu : on refuse d'écrire plutôt que de la perdre."""


# --- Dates ----------------------------------------------------------------------------------

def date_fr(d):
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def lire_date_fr(texte):
    """« 19 oct. 2026 » → date ; tout autre texte (« Quand tu veux ») → None."""
    m = re.fullmatch(r"(\d{1,2}) (\S+) (\d{4})", texte.strip())
    if not m or m.group(2) not in MOIS:
        return None
    try:
        return datetime.date(int(m.group(3)), MOIS.index(m.group(2)) + 1, int(m.group(1)))
    except ValueError:
        return None


# --- Sections Markdown ----------------------------------------------------------------------

def decouper_section(texte, titre):
    """Coupe le fichier en (avant, intro, éléments, après) pour la section `## titre`.

    `intro` : les lignes de la section avant le premier élément (gardées telles quelles).
    `éléments` : les lignes « - … », une ligne de suite (indentée) étant recollée à son élément,
    pour accepter un élément coupé à la main sur plusieurs lignes.
    """
    lignes = texte.split("\n")
    entete = f"## {titre}"
    if entete not in lignes:
        raise ErreurFormat(f"section « {entete} » introuvable")
    debut = lignes.index(entete) + 1
    fin = next((i for i in range(debut, len(lignes)) if lignes[i].startswith("## ")), len(lignes))
    intro, elements = [], []
    for ligne in lignes[debut:fin]:
        if ligne.startswith("- "):
            elements.append(ligne)
        elif ligne.startswith("  ") and elements:
            elements[-1] += " " + ligne.strip()
        elif not ligne.strip():
            continue
        elif elements:
            raise ErreurFormat(f"ligne inattendue après la liste « {titre} » : {ligne}")
        else:
            intro.append(ligne)
    return lignes[:debut], intro, elements, lignes[fin:]


def remplacer_section(texte, titre, elements):
    avant, intro, _, apres = decouper_section(texte, titre)
    corps = [""]
    if intro:
        corps += intro + [""]
    corps += elements
    corps += [""] if apres else []
    return "\n".join(avant + corps + apres).rstrip("\n") + "\n"


def analyser(elements, motif, titre):
    resultat = []
    for ligne in elements:
        m = motif.match(ligne)
        if not m:
            raise ErreurFormat(f"ligne non reconnue dans « {titre} » : {ligne}")
        resultat.append(m.groups())
    return resultat


# --- Lecture --------------------------------------------------------------------------------

def lire_taches(texte, aujourdhui):
    _, _, elements, _ = decouper_section(texte, SECTION_TACHES)
    taches = []
    for echeance, contenu in analyser(elements, RE_TACHE, SECTION_TACHES):
        d = lire_date_fr(echeance)
        taches.append({"echeance": echeance, "texte": contenu, "echue": d is not None and d < aujourdhui})
    return taches


def lire_consignes(texte):
    _, _, elements, _ = decouper_section(texte, SECTION_CONSIGNES)
    return [{"date": d, "texte": t} for d, t in analyser(elements, RE_TACHE, SECTION_CONSIGNES)]


def lire_idees(texte):
    _, _, elements, _ = decouper_section(texte, SECTION_IDEES)
    return [{"titre": t, "depuis": d, "priorite": p, "description": desc}
            for t, d, p, desc in analyser(elements, RE_IDEE, SECTION_IDEES)]


def lire_plans(texte):
    """Le tableau de l'index, en lecture seule : n°, date, titre, statut."""
    plans = []
    for ligne in texte.split("\n"):
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 4 and re.fullmatch(r"P\d{3}", cellules[0]):
            plans.append({"id": cellules[0], "date": cellules[1], "titre": cellules[2], "statut": cellules[3]})
    return plans


def lire_fiche(racine, ident):
    if not re.fullmatch(r"P\d{3}", ident or ""):
        return None
    fiches = sorted((racine / "plans").glob(f"{ident}-*.md"))
    return fiches[0].read_text(encoding="utf-8") if fiches else None


def etat(racine, aujourdhui=None):
    aujourdhui = aujourdhui or datetime.date.today()
    pilotage = (racine / PILOTAGE).read_text(encoding="utf-8")
    index = (racine / INDEX).read_text(encoding="utf-8")
    return {
        "aujourdhui": date_fr(aujourdhui),
        "taches": lire_taches(pilotage, aujourdhui),
        "consignes": lire_consignes(pilotage),
        "idees": lire_idees(index),
        "plans": lire_plans(index),
    }


# --- Écriture -------------------------------------------------------------------------------

def propre(valeur, nom, en_gras=False):
    """Un champ sur une seule ligne. Le champ écrit en gras (échéance, titre) ne peut pas contenir
    « ** », qui fermerait le gras trop tôt ; le texte, lui, peut avoir du gras."""
    texte = " ".join(str(valeur or "").split())
    if not texte:
        raise ErreurFormat(f"champ « {nom} » vide")
    if en_gras and "**" in texte:
        raise ErreurFormat(f"« ** » interdit dans « {nom} »")
    return texte


def lignes_taches(taches):
    return [f"- **{propre(t.get('echeance'), 'échéance', True)}** — {propre(t.get('texte'), 'tâche')}" for t in taches]


def lignes_consignes(consignes):
    return [f"- **{propre(c.get('date'), 'date', True)}** — {propre(c.get('texte'), 'consigne')}" for c in consignes]


def lignes_idees(idees):
    lignes = []
    for i in idees:
        if i.get("priorite") not in PRIORITES:
            raise ErreurFormat(f"priorité inconnue : {i.get('priorite')}")
        lignes.append(f"- **{propre(i.get('titre'), 'titre', True)}** (depuis le {propre(i.get('depuis'), 'depuis')}, "
                      f"priorité {i['priorite']}) : {propre(i.get('description'), 'description')}")
    return lignes


# Quoi écrire pour chaque route : (fichier, section, mise en lignes).
ECRITURES = {
    "/api/taches": (PILOTAGE, SECTION_TACHES, lignes_taches),
    "/api/consignes": (PILOTAGE, SECTION_CONSIGNES, lignes_consignes),
    "/api/idees": (INDEX, SECTION_IDEES, lignes_idees),
}


def ecrire(racine, route, liste):
    fichier, section, mise_en_lignes = ECRITURES[route]
    chemin = racine / fichier
    texte = chemin.read_text(encoding="utf-8")
    # Refuse d'écrire si une ligne corrigée à la main est devenue illisible : sinon l'écran,
    # qui ne l'a pas affichée, l'effacerait sans prévenir.
    analyser(decouper_section(texte, section)[2], RE_IDEE if section == SECTION_IDEES else RE_TACHE, section)
    chemin.write_text(remplacer_section(texte, section, mise_en_lignes(liste)), encoding="utf-8")


# --- Git ------------------------------------------------------------------------------------

def git(racine, *args):
    return subprocess.run(["git", *args], cwd=racine, capture_output=True, text=True)


def synchroniser(racine, message):
    """Committe les deux fichiers du pilotage, puis pull --rebase et push. Ne force jamais.

    `git commit -- <fichiers>` ne prend que ces fichiers : le travail en cours de l'agent n'est
    pas embarqué. `--autostash` le met de côté le temps du rebase.
    Renvoie (réussi, message pour l'écran).
    """
    if git(racine, "branch", "--show-current").stdout.strip() != "main":
        return False, "Pas sur la branche main : rien n'a été committé (fichiers modifiés sur le disque)."
    if git(racine, "status", "--porcelain", "--", PILOTAGE, INDEX).stdout.strip():
        r = git(racine, "commit", "-q", "-m", message, "--", PILOTAGE, INDEX)
        if r.returncode:
            return False, f"Commit impossible : {r.stderr.strip() or r.stdout.strip()}"
    r = git(racine, "pull", "--rebase", "--autostash", "-q", "origin", "main")
    if r.returncode:
        git(racine, "rebase", "--abort")
        return False, ("Enregistré et committé sur le Mac, mais pas envoyé sur GitHub "
                       f"(réseau ou conflit) : {r.stderr.strip()[:300]}")
    r = git(racine, "push", "-q", "origin", "main")
    if r.returncode:
        return False, f"Enregistré et committé sur le Mac, mais le push a échoué : {r.stderr.strip()[:300]}"
    return True, "Envoyé sur GitHub."


# --- Serveur --------------------------------------------------------------------------------

def creer_serveur(racine=ROOT, port=PORT):
    class Admin(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def hote_autorise(self):
            # Un site ouvert dans le navigateur ne doit pas pouvoir écrire dans le dépôt, même en
            # se faisant passer pour 127.0.0.1 (rebinding DNS) : on exige notre propre adresse.
            vrai_port = self.server.server_address[1]
            return self.headers.get("Host") in (f"127.0.0.1:{vrai_port}", f"localhost:{vrai_port}")

        def repondre(self, code, corps, type_="application/json; charset=utf-8"):
            if isinstance(corps, (dict, list)):
                corps = json.dumps(corps, ensure_ascii=False)
            donnees = corps.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", type_)
            self.send_header("Content-Length", str(len(donnees)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(donnees)

        def do_GET(self):
            if not self.hote_autorise():
                return self.repondre(403, {"erreur": "hôte refusé"})
            chemin, _, requete = self.path.partition("?")
            if chemin == "/":
                return self.repondre(200, PAGE.read_text(encoding="utf-8"), "text/html; charset=utf-8")
            if chemin == "/api/etat":
                try:
                    return self.repondre(200, etat(racine))
                except ErreurFormat as e:
                    return self.repondre(500, {"erreur": str(e)})
            if chemin == "/api/fiche":
                texte = lire_fiche(racine, requete.removeprefix("id="))
                if texte is None:
                    return self.repondre(404, {"erreur": "fiche introuvable"})
                return self.repondre(200, {"texte": texte})
            self.repondre(404, {"erreur": "introuvable"})

        def do_POST(self):
            # application/json obligatoire : un formulaire d'un autre site ne peut pas l'envoyer
            # sans que le navigateur demande d'abord la permission (qu'on ne donne jamais).
            if not self.hote_autorise() or not self.headers.get("Content-Type", "").startswith("application/json"):
                return self.repondre(403, {"erreur": "requête refusée"})
            if self.path not in ECRITURES:
                return self.repondre(404, {"erreur": "introuvable"})
            try:
                corps = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                action = propre(corps.get("action"), "action")[:80]
                ecrire(racine, self.path, corps["liste"])
            except (ErreurFormat, KeyError, TypeError, ValueError) as e:
                return self.repondre(400, {"erreur": f"Rien n'a été enregistré : {e}"})
            ok, message = synchroniser(racine, f"Pilotage : {action}")
            self.repondre(200, {"ok": ok, "message": message, "etat": etat(racine)})

    return http.server.ThreadingHTTPServer(("127.0.0.1", port), Admin)


def main():
    adresse = f"http://127.0.0.1:{PORT}/"
    try:
        serveur = creer_serveur()
    except OSError:
        # Le port est pris : l'écran tourne sans doute déjà dans un autre terminal.
        print(f"L'écran d'admin semble déjà lancé : {adresse}")
        webbrowser.open(adresse)
        return 0
    print(f"Écran d'admin : {adresse}  (Ctrl+C pour arrêter)")
    webbrowser.open(adresse)
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
