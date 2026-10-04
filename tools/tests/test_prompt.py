"""Tests de prompt.py (prompt pour le LLM, généré depuis le schéma)."""

import json
import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))

from common import load_schema  # noqa: E402
from prompt import EXEMPLE, exemple_court, prochain_id, prompt_lot, prompt_nouveau  # noqa: E402
from validate import valider_donnees  # noqa: E402

MODULE = json.loads(EXEMPLE.read_text(encoding="utf-8"))
SCHEMA = load_schema()


class TestPrompt(unittest.TestCase):
    def test_exemple_court_valide(self):
        # L'exemple montré au LLM doit lui-même respecter le schéma et les règles.
        exemple = exemple_court(MODULE)
        rapport = valider_donnees(exemple)
        self.assertEqual(rapport.erreurs, [])
        self.assertEqual({q["type"] for q in exemple["questions"]}, {"number", "choice", "text"})

    def test_prompt_nouveau(self):
        exemple = exemple_court(MODULE)
        texte = prompt_nouveau(SCHEMA, exemple)
        self.assertIn('"$defs"', texte)               # le schéma est inclus
        self.assertIn("VÉRIFIE CHAQUE CALCUL", texte)
        # l'exemple aussi (écrit en JSON, d'où json.dumps pour les guillemets et \n)
        premier = json.dumps(exemple["questions"][0]["prompt"], ensure_ascii=False)
        self.assertIn(premier, texte)

    def test_prompt_lot(self):
        texte = prompt_lot(SCHEMA, exemple_court(MODULE), MODULE)
        self.assertIn("à partir de q038", texte)
        self.assertIn('{"questions": [ … ]}', texte)
        for q in MODULE["questions"]:
            self.assertIn(q["id"] + " [", texte)

    def test_prochain_id(self):
        self.assertEqual(prochain_id([{"id": "q009"}, {"id": "q120"}, {"id": "autre"}]), "q121")
        self.assertEqual(prochain_id([]), "q001")


if __name__ == "__main__":
    unittest.main()
