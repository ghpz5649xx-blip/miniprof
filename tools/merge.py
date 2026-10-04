"""Fusionne un lot de questions dans un module existant.

Usage :
    python tools/merge.py modules/mon-module.json lot.json
    python tools/merge.py modules/mon-module.json lot.json --essai   # n'écrit rien

Le lot est la réponse du LLM au prompt « lot suivant » (tools/prompt.py --mode lot) :
{"questions": [...]}, éventuellement entouré de texte ou de ```json. Un module complet
est aussi accepté (cas d'un module corrigé renvoyé en entier).

Règles :
- une question dont l'id n'existe pas est ajoutée à la fin ;
- une question dont l'id existe REMPLACE l'ancienne (correction d'une question signalée) :
  l'historique des enfants reste rattaché au même id ;
- les énoncés quasi identiques sous un autre id sont signalés (doublons probables) ;
- si le lot est un module complet, les questions du module absentes du lot sont listées
  (le LLM a pu renuméroter : risque R6) mais conservées ;
- le numéro de version du module augmente de 1 ;
- le module n'est réécrit que si le résultat est VALIDE (validate.py).

Code de sortie : 0 si la fusion est valide, 1 sinon.
"""

import argparse
import copy
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from common import ModuleIllisible, normalize_text, read_module
from validate import afficher, texte_llm, valider_donnees

# Deux énoncés sont « quasi identiques » s'ils se ressemblent à 90 % ou plus ET
# contiennent les mêmes nombres. Sans la condition sur les nombres, « 347 par 8 »
# et « 348 par 8 » seraient signalés : en maths, ce sont deux vraies questions.
SEUIL_RESSEMBLANCE = 0.9


def lire_lot(path):
    """Renvoie (questions du lot, vrai si le lot est un module complet)."""
    data, _ = read_module(path)
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ModuleIllisible('le lot doit contenir une liste "questions": [ … ].')
    return data["questions"], "lesson" in data


def _nombres(texte):
    return re.findall(r"\d+(?:[.,]\d+)?", texte)


def quasi_identiques(a, b):
    """Vrai si deux énoncés sont probablement la même question."""
    if _nombres(a) != _nombres(b):
        return False
    na, nb = normalize_text(a), normalize_text(b)
    return na == nb or SequenceMatcher(None, na, nb).ratio() >= SEUIL_RESSEMBLANCE


def fusionner(module, questions_lot, lot_complet=False):
    """Renvoie (nouveau module, bilan) sans toucher au module d'origine.

    bilan = {"ajoutees": [id], "remplacees": [id], "doublons": [(id, id)], "absentes": [id]}
    """
    resultat = copy.deepcopy(module)
    questions = resultat["questions"]
    position = {q.get("id"): i for i, q in enumerate(questions)}
    bilan = {"ajoutees": [], "remplacees": [], "doublons": [], "absentes": []}

    vus_dans_le_lot = set()
    for q in questions_lot:
        qid = q.get("id") if isinstance(q, dict) else None
        if qid in vus_dans_le_lot:
            # Même id deux fois dans le lot : on garde les deux pour que
            # validate.py signale l'id en double, au lieu d'en perdre une.
            questions.append(q)
            continue
        vus_dans_le_lot.add(qid)
        if qid in position:
            questions[position[qid]] = q
            bilan["remplacees"].append(qid)
        else:
            # Une question sans id est ajoutée quand même : validate.py la signalera.
            position[qid] = len(questions)
            questions.append(q)
            bilan["ajoutees"].append(qid)

    # Doublons : chaque question ajoutée comparée à toutes les autres. Les
    # questions remplacées ne sont pas comparées (même id, c'est voulu).
    for qid in bilan["ajoutees"]:
        q = questions[position[qid]]
        if not isinstance(q, dict) or not isinstance(q.get("prompt"), str):
            continue
        for autre in questions:
            if autre is q or not isinstance(autre, dict) or not isinstance(autre.get("prompt"), str):
                continue
            paire = tuple(sorted([str(qid), str(autre.get("id"))]))
            if paire not in bilan["doublons"] and quasi_identiques(q["prompt"], autre["prompt"]):
                bilan["doublons"].append(paire)

    if lot_complet:
        ids_lot = {q.get("id") for q in questions_lot if isinstance(q, dict)}
        bilan["absentes"] = [q["id"] for q in module["questions"] if q["id"] not in ids_lot]

    if isinstance(resultat.get("version"), int):
        resultat["version"] += 1
    return resultat, bilan


def afficher_bilan(bilan):
    print(f"Questions ajoutées : {len(bilan['ajoutees'])}")
    if bilan["remplacees"]:
        print(f"Questions remplacées (même id) : {', '.join(map(str, bilan['remplacees']))}")
    if bilan["doublons"]:
        print(f"\n⚠ {len(bilan['doublons'])} doublon(s) probable(s) (énoncés quasi identiques) :")
        for a, b in bilan["doublons"]:
            print(f"  - {a} ≈ {b}")
        print("  Supprime l'une des deux dans le module si c'est bien la même question.")
    if bilan["absentes"]:
        print(f"\n⚠ {len(bilan['absentes'])} question(s) du module absente(s) du lot (conservées) : "
              f"{', '.join(bilan['absentes'])}")
        print("  Le LLM a peut-être changé des id : vérifie qu'il n'y a pas de doublons.")
    print()


def main():
    parser = argparse.ArgumentParser(description="Fusionne un lot de questions dans un module.")
    parser.add_argument("module", help="fichier du module (modules/<id>.json)")
    parser.add_argument("lot", help="fichier du lot renvoyé par le LLM")
    parser.add_argument("--essai", action="store_true", help="tout vérifier sans écrire le module")
    args = parser.parse_args()

    try:
        module, _ = read_module(args.module)
        questions_lot, lot_complet = lire_lot(args.lot)
    except (ModuleIllisible, OSError) as e:
        print(f"✘ Fichier illisible : {e}")
        sys.exit(1)

    nouveau, bilan = fusionner(module, questions_lot, lot_complet)
    afficher_bilan(bilan)
    rapport = valider_donnees(nouveau)
    afficher(args.module, rapport)

    if not rapport.valide:
        print("\nModule NON modifié. Texte à renvoyer au LLM (pour le lot) :\n")
        print(texte_llm(rapport))
        sys.exit(1)
    if args.essai:
        print("\nEssai : module non modifié (relancer sans --essai pour écrire).")
    else:
        Path(args.module).write_text(json.dumps(nouveau, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
        print(f"\n✔ Module réécrit : {args.module} (version {nouveau.get('version')}).")
        print("  Ensuite : python tools/build_index.py, relire quelques questions, commit.")
    sys.exit(0)


if __name__ == "__main__":
    main()
