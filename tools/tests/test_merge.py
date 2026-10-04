"""Tests de merge.py (fusion d'un lot de questions dans un module)."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))

from merge import fusionner, lire_lot, quasi_identiques  # noqa: E402
from validate import valider_donnees  # noqa: E402

FIXTURES = TESTS / "fixtures"
MINIMAL = json.loads((FIXTURES / "minimal.json").read_text(encoding="utf-8"))


class TestFusion(unittest.TestCase):
    def setUp(self):
        # Le lot de test est entouré de texte et de ```json, comme une réponse de LLM.
        self.lot, self.complet = lire_lot(FIXTURES / "lot.json")

    def test_ajout_remplacement_version(self):
        nouveau, bilan = fusionner(MINIMAL, self.lot)
        self.assertEqual(bilan["ajoutees"], ["q4", "q5"])
        self.assertEqual(bilan["remplacees"], ["q2"])
        self.assertEqual([q["id"] for q in nouveau["questions"]], ["q1", "q2", "q3", "q4", "q5"])
        self.assertEqual(nouveau["questions"][1]["prompt"], "Combien font 10 + 6 ?")
        self.assertEqual(nouveau["version"], MINIMAL["version"] + 1)
        self.assertEqual(MINIMAL["questions"][1]["prompt"], "Combien font 10 + 5 ?",
                         "le module d'origine ne doit pas être modifié")
        self.assertTrue(valider_donnees(nouveau).valide)
        self.assertFalse(self.complet)

    def test_doublon_signale(self):
        # q5 « Calcule 2 + 3 ! » ≈ q1 « Calcule 2 + 3. »
        _, bilan = fusionner(MINIMAL, self.lot)
        self.assertEqual(bilan["doublons"], [("q1", "q5")])

    def test_nombres_differents_pas_doublon(self):
        self.assertFalse(quasi_identiques("Effectue 347 par 8.", "Effectue 348 par 8."))
        self.assertTrue(quasi_identiques("Effectue 347 par 8.", "Effectue  347 par 8 !"))

    def test_id_en_double_dans_le_lot(self):
        lot = [self.lot[0], dict(self.lot[0], prompt="Calcule 7 + 7.")]
        nouveau, _ = fusionner(MINIMAL, lot)
        self.assertFalse(valider_donnees(nouveau).valide)

    def test_lot_complet_questions_absentes(self):
        _, bilan = fusionner(MINIMAL, [MINIMAL["questions"][0]], lot_complet=True)
        self.assertEqual(bilan["absentes"], ["q2", "q3"])


class TestEcriture(unittest.TestCase):
    def lancer(self, lot_texte):
        """Lance merge.py sur une copie de minimal.json ; renvoie (code, module relu)."""
        with tempfile.TemporaryDirectory() as tmp:
            module = Path(tmp) / "minimal.json"
            shutil.copy(FIXTURES / "minimal.json", module)
            lot = Path(tmp) / "lot.json"
            lot.write_text(lot_texte, encoding="utf-8")
            r = subprocess.run([sys.executable, str(TESTS.parent / "merge.py"), str(module), str(lot)],
                               capture_output=True, text=True)
            return r.returncode, json.loads(module.read_text(encoding="utf-8"))

    def test_lot_valide_ecrit(self):
        code, module = self.lancer((FIXTURES / "lot.json").read_text(encoding="utf-8"))
        self.assertEqual(code, 0)
        self.assertEqual(len(module["questions"]), 5)

    def test_lot_invalide_n_ecrit_rien(self):
        lot = {"questions": [{"id": "q9", "skill": "inconnu", "difficulty": 1, "type": "text",
                              "prompt": "?", "accepted": ["x"], "hint": "h", "explanation": "e"}]}
        code, module = self.lancer(json.dumps(lot))
        self.assertEqual(code, 1)
        self.assertEqual(module, MINIMAL)


if __name__ == "__main__":
    unittest.main()
