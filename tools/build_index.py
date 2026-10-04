"""Régénère modules/index.json, la liste des modules lue par l'app.

Usage :
    python tools/build_index.py            # dossier modules/ du dépôt
    python tools/build_index.py autre/dossier

Pourquoi un index : la bibliothèque et le bilan de l'app affichent titre, matière, niveau
et compétences sans télécharger chaque module (100 à 200 questions chacun). Le module complet n'est lu
qu'à son ouverture.

Seuls les modules VALIDES (validate.py) et bien nommés (<id>.json) sont indexés :
un module cassé ne doit jamais arriver jusqu'aux enfants.
"""

import argparse
import json
import sys
from pathlib import Path

from validate import valider_fichier

ROOT = Path(__file__).resolve().parent.parent
NOM_INDEX = "index.json"
# Ordre d'affichage des classes (l'ordre alphabétique mettrait 3e avant CE1).
ORDRE_NIVEAUX = ["CP", "CE1", "CE2", "CM1", "CM2", "6e", "5e", "4e", "3e"]


def construire_index(dossier):
    """Renvoie (index, ecartes) ; ecartes = liste de (nom de fichier, raison)."""
    modules, ecartes = [], []
    for path in sorted(Path(dossier).glob("*.json")):
        if path.name == NOM_INDEX:
            continue
        rapport = valider_fichier(path)
        if not rapport.valide:
            ecartes.append((path.name, f"{len(rapport.erreurs)} erreur(s) : {rapport.erreurs[0]}"))
            continue
        data = rapport.data
        if path.stem != data["id"]:
            ecartes.append((path.name, f"le fichier doit s'appeler « {data['id']}.json »"))
            continue
        modules.append({
            "id": data["id"],
            "file": path.name,
            "version": data["version"],
            "title": data["title"],
            "subject": data["subject"],
            "level": data["level"],
            "description": data["description"],
            "questions": len(data["questions"]),
            # Libellés des compétences : le bilan « tous modules » de l'app les
            # affiche sans avoir à télécharger chaque module.
            "skills": [{"id": s["id"], "label": s["label"]} for s in data["skills"]],
        })
    modules.sort(key=lambda m: (m["subject"], ORDRE_NIVEAUX.index(m["level"]), m["title"]))
    # Pas de date de génération : l'index ne change que si un module change,
    # ce qui évite des commits « vides » de index.json.
    return {"modules": modules}, ecartes


def main():
    parser = argparse.ArgumentParser(description="Régénère l'index des modules.")
    parser.add_argument("dossier", nargs="?", default=str(ROOT / "modules"),
                        help="dossier des modules (défaut : modules/)")
    args = parser.parse_args()

    index, ecartes = construire_index(args.dossier)
    cible = Path(args.dossier) / NOM_INDEX
    cible.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✔ {len(index['modules'])} module(s) indexé(s) dans {cible}")
    for m in index["modules"]:
        print(f"  - {m['file']} ({m['level']}, {m['questions']} questions)")
    if ecartes:
        print(f"\n✘ {len(ecartes)} fichier(s) écarté(s) (lancer validate.py dessus) :")
        for nom, raison in ecartes:
            print(f"  - {nom} : {raison}")
    # Code 1 si un fichier est écarté : on le remarque avant de pousser.
    sys.exit(1 if ecartes else 0)


if __name__ == "__main__":
    main()
