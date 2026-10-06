"""Régénère modules/index.json, la liste des modules lue par l'app.

Usage :
    python tools/build_index.py            # dossier modules/ du dépôt
    python tools/build_index.py autre/dossier

Pourquoi un index : la bibliothèque et le bilan de l'app affichent titre, matière, niveau
et compétences sans télécharger chaque module (100 à 200 questions chacun). Le module complet n'est lu
qu'à son ouverture.

Seuls les modules VALIDES (validate.py) et bien nommés (<id>.json) sont indexés :
un module cassé ne doit jamais arriver jusqu'aux enfants.

Deux sortes de modules (champ "kind" de l'index) :
- "json" : <id>.json, joué par les écrans de l'app ;
- "html" : <id>.html, page autonome générée par un LLM, contrôlée par
  check_html.py ; sa fiche (#miniprof-module) donne titre, niveau, compétences.

Brouillons (modules/brouillons.json, {"brouillons": ["<id>", ...]}) : un module publié mais
pas encore relu par le parent. Il est indexé avec "brouillon": true ; la bibliothèque des
enfants ne l'affiche pas (son URL marche, pour que le parent l'essaie). Le skill
/nouveau-module y ajoute chaque nouveau module et l'en retire sur « valide <id> ». Pourquoi un fichier à
part plutôt qu'un champ du module : le schéma refuse les champs inconnus, et un seul fichier
marche pour les modules JSON comme HTML. Valider un module = retirer son id de la liste.
"""

import argparse
import json
import sys
from pathlib import Path

from check_html import verifier_fichier
from validate import valider_fichier

ROOT = Path(__file__).resolve().parent.parent
NOM_INDEX = "index.json"
NOM_BROUILLONS = "brouillons.json"
# Ordre d'affichage des classes (l'ordre alphabétique mettrait 3e avant CE1).
ORDRE_NIVEAUX = ["CP", "CE1", "CE2", "CM1", "CM2", "6e", "5e", "4e", "3e"]


def construire_index(dossier):
    """Renvoie (index, ecartes) ; ecartes = liste de (nom de fichier, raison)."""
    modules, ecartes = [], []
    for path in sorted(Path(dossier).glob("*.json")):
        if path.name in (NOM_INDEX, NOM_BROUILLONS):
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
            "kind": "json",
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
    for path in sorted(Path(dossier).glob("*.html")):
        rapport = verifier_fichier(path)
        if not rapport.valide:
            ecartes.append((path.name, f"{len(rapport.erreurs)} erreur(s) : {rapport.erreurs[0]}"))
            continue
        fiche = rapport.fiche
        modules.append({
            "id": fiche["id"],
            "kind": "html",
            "file": path.name,
            "title": fiche["title"],
            "subject": fiche["subject"],
            "level": fiche["level"],
            "description": fiche["description"],
            "skills": [{"id": s["id"], "label": s["label"]} for s in fiche["skills"]],
        })
    ids = [m["id"] for m in modules]
    for m in modules:
        if ids.count(m["id"]) > 1:
            ecartes.append((m["file"], f"id « {m['id']} » déjà utilisé par un autre module"))
    modules = [m for m in modules if ids.count(m["id"]) == 1]
    brouillons, erreur = lire_brouillons(dossier)
    if erreur:
        ecartes.append((NOM_BROUILLONS, erreur))
    for id_ in brouillons:
        if id_ not in ids:
            ecartes.append((NOM_BROUILLONS, f"id « {id_} » inconnu (module absent ou écarté)"))
    for m in modules:
        if m["id"] in brouillons:
            m["brouillon"] = True
    modules.sort(key=lambda m: (m["subject"], ORDRE_NIVEAUX.index(m["level"]), m["title"]))
    # Pas de date de génération : l'index ne change que si un module change,
    # ce qui évite des commits « vides » de index.json.
    return {"modules": modules}, ecartes


def lire_brouillons(dossier):
    """Renvoie (liste des ids en brouillon, message d'erreur ou None). Fichier absent = aucun."""
    path = Path(dossier) / NOM_BROUILLONS
    if not path.exists():
        return [], None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [], f"JSON illisible : {e}"
    liste = data.get("brouillons") if isinstance(data, dict) else None
    if not isinstance(liste, list) or not all(isinstance(i, str) for i in liste):
        return [], 'format attendu : {"brouillons": ["<id>", ...]}'
    return liste, None


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
        detail = f"{m['questions']} questions" if m["kind"] == "json" else "page HTML"
        if m.get("brouillon"):
            detail += ", brouillon"
        print(f"  - {m['file']} ({m['level']}, {detail})")
    if ecartes:
        print(f"\n✘ {len(ecartes)} fichier(s) écarté(s) (lancer validate.py ou check_html.py dessus) :")
        for nom, raison in ecartes:
            print(f"  - {nom} : {raison}")
    # Code 1 si un fichier est écarté : on le remarque avant de pousser.
    sys.exit(1 if ecartes else 0)


if __name__ == "__main__":
    main()
