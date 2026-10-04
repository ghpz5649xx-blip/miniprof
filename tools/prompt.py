"""Génère le prompt à coller dans le LLM pour créer ou compléter un module.

Usage :
    python tools/prompt.py --mode nouveau
    python tools/prompt.py --mode lot modules/mon-module.json

Le prompt est écrit dans docs/ (prompt-nouveau.md ou prompt-lot-<id>.md) et copié
dans le presse-papiers (macOS, pbcopy) : il suffit de le coller dans le LLM avec les photos.

Pourquoi un générateur : le prompt contient le schéma (schema/module.schema.json) et un
exemple extrait du module d'exemple. Si le format évolue, on relance l'outil au lieu de
réécrire le prompt à la main. Seules les règles pédagogiques ci-dessous sont du texte fixe.
"""

import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path

from common import ROOT, ModuleIllisible, load_schema, read_module
from validate import repartition

EXEMPLE = ROOT / "modules" / "maths-cm2-division-euclidienne.json"
DOCS = ROOT / "docs"

# Taille d'un lot : au-delà de ~60 questions par réponse, un LLM gratuit perd en qualité.
LOT_MIN, LOT_MAX = 40, 60

REGLES = """\
Règles pédagogiques :
- Utilise le vocabulaire de la classe indiquée, avec des phrases courtes ; tutoie l'enfant.
- N'invente aucun contenu absent des photos : reste sur les notions, méthodes et types
  d'exercices du cours. Note dans "source_note" ce qui était illisible ou incertain.
- Indice ("hint") : il guide (méthode, question à se poser, rappel) sans jamais donner la
  réponse.
- Explication ("explanation") : courte, pas à pas, avec le calcul ou le raisonnement complet.
- Difficulté progressive de 1 (application directe) à 4 (problème en plusieurs étapes ou
  piège classique), avec des questions à chaque niveau pour chaque compétence.
- Varie les énoncés : pas deux questions identiques à un nombre près sans raison.
- "common_errors" (facultatif mais précieux) : les erreurs fréquentes des élèves et un
  message qui explique l'erreur sans donner la réponse.
- Mise en forme autorisée : **gras** et \\n (retour à la ligne). Jamais de HTML ni de
  Markdown d'une autre sorte. Symboles unicode permis : × ÷ − ² √ ≤ ≥.

Exactitude (obligatoire) :
- VÉRIFIE CHAQUE CALCUL avant de répondre : refais chaque opération, et pour une
  division euclidienne vérifie dividende = diviseur × quotient + reste avec reste < diviseur.
- Dans un QCM, une seule bonne réponse ; "answer" est l'id d'un des choix.
- Une erreur de "common_errors" ne doit jamais être égale à la bonne réponse.
- Nombres : "answer" d'une case est un nombre JSON (3.5, pas "3,5").

Format (obligatoire) :
- Réponds UNIQUEMENT avec le JSON, sans texte avant ou après, sans ```.
- Le JSON doit respecter exactement le schéma ci-dessous (pas de champ en plus).
- Les "id" sont stables : ne change jamais un id existant.
"""


# ---------------------------------------------------------------------------
# Exemple court, extrait du module d'exemple
# ---------------------------------------------------------------------------

def _bloc_court(b):
    b = copy.deepcopy(b)
    if "steps" in b:
        b["steps"] = b["steps"][:2]
    return b


def exemple_court(module):
    """Petit module valide : 1 bloc de chaque type, 1 question de chaque type,
    2 étapes au plus par bloc, seulement les compétences utilisées, et au moins
    un bloc de leçon par compétence (règle de validate.py)."""
    blocs = []
    for type_ in ("text", "worked_example", "guided_steps"):
        b = next((b for b in module["lesson"] if b["type"] == type_), None)
        if b:
            blocs.append(_bloc_court(b))
    questions = []
    for type_ in ("number", "choice", "text"):
        du_type = [q for q in module["questions"] if q["type"] == type_]
        # De préférence une question d'une compétence déjà illustrée par la leçon.
        avec_lecon = [q for q in du_type if q["skill"] in {b["skill"] for b in blocs}]
        q = (avec_lecon or du_type or [None])[0]
        if q is None:
            continue
        questions.append(q)
        if q["skill"] not in {b["skill"] for b in blocs}:
            blocs.append(_bloc_court(next(b for b in module["lesson"] if b["skill"] == q["skill"])))
    utilisees = {x["skill"] for x in blocs + questions}
    meta = {k: module[k] for k in ("schema_version", "id", "version", "title", "subject",
                                   "level", "description")}
    return {
        **meta,
        "skills": [s for s in module["skills"] if s["id"] in utilisees],
        "lesson": blocs,
        "questions": questions,
    }


def prochain_id(questions):
    """q038 si le module va jusqu'à q037 (ids de la forme q + nombre)."""
    numeros = [int(m.group(1)) for q in questions if (m := re.fullmatch(r"q(\d+)", q["id"]))]
    return f"q{max(numeros, default=0) + 1:03d}"


def _json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Les deux prompts
# ---------------------------------------------------------------------------

def prompt_nouveau(schema, exemple):
    return f"""\
Tu es un professeur des écoles et de collège. Je t'envoie des photos d'un cours, d'exercices
et de contrôles d'un enfant. Crée un module d'entraînement au format JSON décrit plus bas.

Le module contient :
1. Les métadonnées : "id" (matiere-niveau-sujet, ex. maths-cm2-division-euclidienne),
   "version": 1, titre, matière, classe, description en une ou deux phrases pour l'enfant.
2. "skills" : 2 à 6 compétences travaillées dans le cours.
3. "lesson" : la leçon « Apprendre », qui montre le CHEMINEMENT DE PENSÉE pas à pas. Pour
   chaque compétence : un "worked_example" (chaque étape = ce que je pense/fais + pourquoi),
   puis un "guided_steps" (phrases à trous que l'enfant complète une par une, avec ▢ à
   l'endroit de la réponse et un indice). Des blocs "text" pour les définitions et
   « À retenir ».
4. "questions" : un premier lot de {LOT_MIN} à {LOT_MAX} questions, ids q001, q002…,
   réparties sur toutes les compétences et les 4 niveaux de difficulté.

{REGLES}
Schéma JSON à respecter :
{_json(schema)}

Exemple court (extrait d'un vrai module ; le tien sera plus complet) :
{_json(exemple)}
"""


def prompt_lot(schema, exemple, module):
    competences = "\n".join(f"- {s['id']} : {s['label']}" for s in module["skills"])
    existants = "\n".join(
        f"- {q['id']} [{q['skill']}, niveau {q['difficulty']}] {q['prompt']}".replace("\n", " ")
        for q in module["questions"]
    )
    return f"""\
Tu complètes un module d'entraînement existant : « {module['title']} » ({module['level']}).
Écris {LOT_MIN} à {LOT_MAX} NOUVELLES questions, différentes de celles qui existent déjà
(liste plus bas), en t'appuyant sur les photos du cours si je te les renvoie.

Réponds avec un objet JSON qui contient seulement la liste des questions :
{{"questions": [ … ]}}
- Ids : à partir de {prochain_id(module['questions'])}, puis dans l'ordre (sans trou ni réutilisation).
- "skill" : uniquement les compétences ci-dessous.
- Équilibre la répartition : renforce les compétences et niveaux les moins fournis.

Compétences :
{competences}

Répartition actuelle (compétence × difficulté) :
{repartition(module)}

{REGLES}
Schéma JSON du module (seule la partie "questions" te concerne) :
{_json(schema)}

Exemple de questions (format attendu) :
{_json({"questions": exemple["questions"]})}

Questions déjà présentes (ne pas les répéter, même avec d'autres nombres proches) :
{existants}
"""


def copier(texte):
    """Copie dans le presse-papiers (macOS). Renvoie True si c'est fait."""
    try:
        subprocess.run(["pbcopy"], input=texte.encode("utf-8"), check=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Génère le prompt pour le LLM.")
    parser.add_argument("--mode", choices=["nouveau", "lot"], required=True)
    parser.add_argument("module", nargs="?", help="module à compléter (mode lot)")
    args = parser.parse_args()

    schema = load_schema()
    exemple = exemple_court(json.loads(EXEMPLE.read_text(encoding="utf-8")))

    if args.mode == "nouveau":
        texte = prompt_nouveau(schema, exemple)
        sortie = DOCS / "prompt-nouveau.md"
    else:
        if not args.module:
            parser.error("le mode lot demande le fichier du module : --mode lot modules/<id>.json")
        try:
            module, _ = read_module(args.module)
        except (ModuleIllisible, OSError) as e:
            print(f"✘ Module illisible : {e}")
            sys.exit(1)
        texte = prompt_lot(schema, exemple, module)
        sortie = DOCS / f"prompt-lot-{module['id']}.md"

    sortie.write_text(texte, encoding="utf-8")
    print(f"✔ Prompt écrit dans {sortie.relative_to(ROOT)} ({len(texte)} caractères).")
    if copier(texte):
        print("  Copié dans le presse-papiers : colle-le dans le LLM avec les photos.")
    else:
        print("  Presse-papiers indisponible : ouvre le fichier et copie son contenu.")


if __name__ == "__main__":
    main()
