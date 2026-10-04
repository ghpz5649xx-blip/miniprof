"""Tests de analyse.py sur une petite sauvegarde (fixtures/export.json)."""

import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))

from analyse import charger, evaluations, est_en_baisse, graphiques, par_competence, plus_ratees  # noqa: E402

EXPORT = TESTS / "fixtures" / "export.json"


class TestAnalyse(unittest.TestCase):
    def setUp(self):
        self.df = charger(EXPORT)

    def test_chargement(self):
        self.assertEqual(len(self.df), 35)
        self.assertEqual(set(self.df["enfant"]), {"Léa", "Tom"})

    def test_par_competence(self):
        s = par_competence(self.df).set_index(["enfant", "competence"])
        # calcul : 25 essais d'entraînement (20 justes) + 1 juste en évaluation
        self.assertEqual(s.loc[("Léa", "calcul"), "essais"], 26)
        self.assertEqual(s.loc[("Léa", "calcul"), "reussite"], 81)
        self.assertTrue(s.loc[("Léa", "calcul"), "en_baisse"])
        self.assertTrue(s.loc[("Léa", "preuve"), "a_travailler"])   # 33 %
        self.assertFalse(s.loc[("Tom", "vocabulaire"), "a_travailler"])

    def test_regle_en_baisse_comme_l_app(self):
        self.assertFalse(est_en_baisse([True] * 4 + [False] * 10))   # moins de 5 avant
        self.assertTrue(est_en_baisse([True] * 5 + [False] * 10))
        self.assertFalse(est_en_baisse([True] * 10))

    def test_plus_ratees_et_evaluations(self):
        self.assertEqual(plus_ratees(self.df).iloc[0]["question"], "q015")
        ev = evaluations(self.df)
        self.assertEqual(ev[["note", "total", "niveau"]].values.tolist(), [[2, 3, "mixte"]])

    def test_graphiques(self):
        with tempfile.TemporaryDirectory() as tmp:
            fichiers = graphiques(self.df, tmp)
            self.assertEqual(len(fichiers), 5)  # Léa : 3 graphiques ; Tom : 2 (pas d'évaluation)
            self.assertTrue(all(Path(f).stat().st_size > 0 for f in fichiers))


if __name__ == "__main__":
    unittest.main()
