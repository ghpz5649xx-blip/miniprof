"""Valide un fichier de module miniprof.

Usage :
    python tools/validate.py modules/mon-module.json
    python tools/validate.py reponse-llm.json --llm       # texte de correction à recopier au LLM
    python tools/validate.py reponse-llm.json --nettoyer  # réécrit le fichier en JSON propre

Deux niveaux de contrôle :
1. le schéma (schema/module.schema.json) : structure, types, champs obligatoires ;
2. les règles sémantiques ci-dessous : ce qu'un schéma ne sait pas exprimer
   (ids uniques, références, cohérence des QCM, répartition…).

Code de sortie : 0 si aucune erreur (les avertissements n'empêchent pas), 1 sinon.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from common import ModuleIllisible, normalize_text, read_module, schema_errors

MAX_QUESTIONS = 250          # au-delà, le fichier devient lourd à charger sur téléphone
CIBLE_QUESTIONS = 100        # objectif d'une banque complète
MIN_PAR_COMPETENCE = 5
ERREUR_TEXTE_AUTOUR = (
    "le fichier contient du texte autour du JSON : l'app ne pourra pas le lire. "
    "Relance avec --nettoyer pour réécrire un fichier propre."
)


class Rapport:
    def __init__(self):
        self.erreurs = []
        self.avertissements = []
        self.data = None
        self.extrait = False
        self.structure_ok = False   # vrai si le schéma est respecté

    @property
    def valide(self):
        return not self.erreurs


# ---------------------------------------------------------------------------
# Règles sémantiques
# ---------------------------------------------------------------------------

def doublons(valeurs):
    return [v for v, n in Counter(valeurs).items() if n > 1]


def verifier_semantique(data, rapport):
    err = rapport.erreurs.append
    warn = rapport.avertissements.append

    skills = [s["id"] for s in data["skills"]]
    for d in doublons(skills):
        err(f"skills : l'id de compétence « {d} » est utilisé plusieurs fois")
    skills = set(skills)

    # --- Leçon : chaque compétence doit être expliquée -----------------------
    for i, bloc in enumerate(data["lesson"]):
        if bloc["skill"] not in skills:
            err(f"lesson[{i}].skill : compétence « {bloc['skill']} » absente de skills")
        if bloc["type"] == "guided_steps":
            for j, step in enumerate(bloc["steps"]):
                if "▢" not in step["prompt"]:
                    warn(f"lesson[{i}].steps[{j}].prompt : pas de ▢ pour montrer où écrire la réponse")
    for s in sorted(skills):
        types = {b["type"] for b in data["lesson"] if b["skill"] == s}
        if not types:
            err(f"lesson : aucun bloc de leçon pour la compétence « {s} » (leçon obligatoire)")
        elif "worked_example" not in types:
            warn(f"lesson : pas d'exemple résolu (worked_example) pour la compétence « {s} »")

    # --- Questions -------------------------------------------------------------
    questions = data["questions"]
    for d in doublons([q["id"] for q in questions]):
        err(f"questions : l'id « {d} » est utilisé plusieurs fois")

    enonces = Counter(normalize_text(q["prompt"]) for q in questions)
    for q in questions:
        if enonces[normalize_text(q["prompt"])] > 1:
            warn(f"questions ({q['id']}) : énoncé identique à une autre question")

    for i, q in enumerate(questions):
        ou = f"questions[{i}] (question {q['id']})"
        if q["skill"] not in skills:
            err(f"{ou}.skill : compétence « {q['skill']} » absente de skills")
        if q["type"] == "number":
            verifier_number(q, ou, err)
        elif q["type"] == "choice":
            verifier_choice(q, ou, err)
        elif q["type"] == "text":
            verifier_text(q, ou, err, warn)

    # --- Taille et répartition -----------------------------------------------
    n = len(questions)
    if n > MAX_QUESTIONS:
        err(f"questions : {n} questions, maximum {MAX_QUESTIONS} (découper en deux modules)")
    elif n < CIBLE_QUESTIONS:
        warn(f"questions : {n} questions, objectif {CIBLE_QUESTIONS} à 200 (ajouter des lots avec merge.py)")

    for s in sorted(skills):
        diffs = Counter(q["difficulty"] for q in questions if q["skill"] == s)
        total = sum(diffs.values())
        if total < MIN_PAR_COMPETENCE:
            warn(f"compétence « {s} » : seulement {total} question(s), au moins {MIN_PAR_COMPETENCE} conseillées")
        manquantes = [str(d) for d in range(1, 5) if diffs[d] == 0]
        if total and manquantes:
            warn(f"compétence « {s} » : aucune question de difficulté {', '.join(manquantes)}")


def verifier_number(q, ou, err):
    keys = [f["key"] for f in q["fields"]]
    for d in doublons(keys):
        err(f"{ou}.fields : la case « {d} » est définie plusieurs fois")
    answers = {f["key"]: f["answer"] for f in q["fields"]}
    for j, ce in enumerate(q.get("common_errors", [])):
        inconnues = [k for k in ce["when"] if k not in answers]
        if inconnues:
            err(f"{ou}.common_errors[{j}].when : case(s) inconnue(s) {', '.join(inconnues)}")
        elif all(answers[k] == v for k, v in ce["when"].items()):
            err(f"{ou}.common_errors[{j}].when : correspond à la bonne réponse, ce n'est pas une erreur")


def verifier_choice(q, ou, err):
    ids = [c["id"] for c in q["choices"]]
    for d in doublons(ids):
        err(f"{ou}.choices : l'id de choix « {d} » est utilisé plusieurs fois")
    for d in doublons([normalize_text(c["label"]) for c in q["choices"]]):
        err(f"{ou}.choices : deux choix ont le même libellé (« {d} »)")
    if q["answer"] not in ids:
        err(f"{ou}.answer : « {q['answer']} » ne fait pas partie des choix ({', '.join(ids)})")
    for j, ce in enumerate(q.get("common_errors", [])):
        if ce["when"] not in ids:
            err(f"{ou}.common_errors[{j}].when : « {ce['when']} » ne fait pas partie des choix")
        elif ce["when"] == q["answer"]:
            err(f"{ou}.common_errors[{j}].when : c'est la bonne réponse, ce n'est pas une erreur")


def verifier_text(q, ou, err, warn):
    normalises = [normalize_text(a) for a in q["accepted"]]
    if any(not a for a in normalises):
        err(f"{ou}.accepted : une réponse acceptée est vide après normalisation")
    for d in doublons(normalises):
        warn(f"{ou}.accepted : « {d} » est présent plusieurs fois (casse/accents ignorés)")
    for j, ce in enumerate(q.get("common_errors", [])):
        if normalize_text(ce["when"]) in normalises:
            err(f"{ou}.common_errors[{j}].when : « {ce['when']} » est une réponse acceptée")


# ---------------------------------------------------------------------------
# Rapport
# ---------------------------------------------------------------------------

def valider_donnees(data, rapport=None):
    """Valide un module déjà chargé en mémoire (utilisé aussi par merge.py)."""
    rapport = rapport or Rapport()
    rapport.data = data
    if not isinstance(data, dict):
        rapport.erreurs.append("(racine) : le module doit être un objet { … }")
        return rapport

    rapport.erreurs.extend(schema_errors(data))
    if rapport.erreurs:
        # Les règles sémantiques supposent une structure correcte : on s'arrête là.
        return rapport

    rapport.structure_ok = True
    verifier_semantique(data, rapport)
    return rapport


def valider_fichier(path):
    rapport = Rapport()
    try:
        data, rapport.extrait = read_module(path)
    except ModuleIllisible as e:
        rapport.erreurs.append(f"fichier illisible : {e}")
        return rapport
    except OSError as e:
        rapport.erreurs.append(f"impossible d'ouvrir le fichier : {e.strerror}")
        return rapport

    valider_donnees(data, rapport)
    if not rapport.structure_ok:
        return rapport
    if rapport.extrait:
        rapport.erreurs.append(ERREUR_TEXTE_AUTOUR)
    if Path(path).stem != data["id"]:
        rapport.avertissements.append(
            f"nom de fichier : « {Path(path).name} » devrait être « {data['id']}.json »"
        )
    return rapport


def repartition(data):
    """Tableau compétence × difficulté, sous forme de texte."""
    lignes = ["  compétence            d1  d2  d3  d4  total"]
    for s in data["skills"]:
        c = Counter(q["difficulty"] for q in data["questions"] if q["skill"] == s["id"])
        cases = "".join(f"{c[d]:>4}" for d in range(1, 5))
        lignes.append(f"  {s['id'][:20]:<20}{cases}{sum(c.values()):>7}")
    c = Counter(q["difficulty"] for q in data["questions"])
    lignes.append(f"  {'TOTAL':<20}" + "".join(f"{c[d]:>4}" for d in range(1, 5)) + f"{len(data['questions']):>7}")
    return "\n".join(lignes)


def afficher(path, rapport):
    data = rapport.data if isinstance(rapport.data, dict) else {}
    if data.get("title"):
        print(f"Module : {data['title']} ({data.get('id', '?')}, version {data.get('version', '?')})")
    else:
        print(f"Fichier : {path}")

    if rapport.valide:
        print("✔ VALIDE : aucune erreur.")
    else:
        print(f"✘ INVALIDE : {len(rapport.erreurs)} erreur(s).")
        for e in rapport.erreurs[:50]:
            print(f"  - {e}")
        if len(rapport.erreurs) > 50:
            print(f"  … et {len(rapport.erreurs) - 50} autres.")

    if rapport.avertissements:
        print(f"\n⚠ {len(rapport.avertissements)} avertissement(s) (n'empêchent pas l'utilisation) :")
        for w in rapport.avertissements:
            print(f"  - {w}")

    # Si le schéma a échoué, la structure peut être cassée : pas de tableau.
    if rapport.structure_ok:
        print("\nRépartition des questions :")
        print(repartition(data))


def texte_llm(rapport):
    """Message à recopier tel quel dans la conversation avec le LLM."""
    # Le texte autour du JSON se corrige avec --nettoyer, pas besoin du LLM.
    erreurs = [e for e in rapport.erreurs if e != ERREUR_TEXTE_AUTOUR]
    if not erreurs:
        conseil = " (lance seulement --nettoyer)" if rapport.extrait else ""
        return f"Aucune erreur : rien à renvoyer au LLM{conseil}."
    lignes = [
        "Ton JSON contient les erreurs suivantes (chemin : problème) :",
        "",
        *[f"- {e}" for e in erreurs],
        "",
        "Corrige uniquement ces erreurs, sans changer les \"id\" existants, "
        "puis renvoie le JSON complet, valide, sans aucun texte avant ou après.",
    ]
    return "\n".join(lignes)


def main():
    parser = argparse.ArgumentParser(description="Valide un module miniprof.")
    parser.add_argument("module", help="fichier JSON du module")
    parser.add_argument("--llm", action="store_true",
                        help="afficher le texte de correction à recopier au LLM")
    parser.add_argument("--nettoyer", action="store_true",
                        help="réécrire le fichier en JSON propre (retire le texte autour)")
    args = parser.parse_args()

    rapport = valider_fichier(args.module)

    if args.nettoyer and rapport.data is not None:
        Path(args.module).write_text(
            json.dumps(rapport.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Fichier réécrit en JSON propre : {args.module}\n")
        rapport = valider_fichier(args.module)

    if args.llm:
        print(texte_llm(rapport))
    else:
        afficher(args.module, rapport)
    sys.exit(0 if rapport.valide else 1)


if __name__ == "__main__":
    main()
