"""Tests de analyse.py sur une petite sauvegarde (fixtures/export.json)."""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))

from analyse import afficher, afficher_signalements, charger, charger_signalements, deuxiemes_chances, evaluations, est_en_baisse, graphiques, par_competence, plus_ratees  # noqa: E402

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

    def test_signalements(self):
        sig = charger_signalements(EXPORT)
        # 2 signalements avec copie + 1 ancien flag (q020) sans copie ; q021 n'est pas répété
        self.assertEqual(len(sig), 3)
        self.assertEqual([s["date"] for s in sig], sorted((s["date"] for s in sig), reverse=True))
        html = sig[0]
        self.assertEqual((html["enfant"], html["question"], html["commentaire"]),
                         ("Tom", None, "51 = 5 + 1 = 6, pas 9"))
        self.assertEqual(html["choix"], ["Oui", "Non"])
        ancien = next(s for s in sig if s["question"] == "q020")
        self.assertEqual((ancien["enfant"], ancien["enonce"]), ("Léa", ""))

    def test_signalements_ancien_fichier(self):
        # un fichier d'avant P003 n'a pas de « signalements » : seuls les flags sortent
        with tempfile.TemporaryDirectory() as tmp:
            chemin = Path(tmp) / "ancien.export.json"
            data = json.loads(EXPORT.read_text(encoding="utf-8"))
            del data["signalements"]
            chemin.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(len(charger_signalements(chemin)), 2)

    def test_affichage_des_signalements(self):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            afficher_signalements(charger_signalements(EXPORT))
        texte = sortie.getvalue()
        self.assertIn("Signalements : 3", texte)
        self.assertIn("Commentaire : 51 = 5 + 1 = 6, pas 9", texte)
        self.assertIn("Commentaire : (aucun)", texte)

    def test_graphiques(self):
        with tempfile.TemporaryDirectory() as tmp:
            fichiers = graphiques(self.df, tmp)
            self.assertEqual(len(fichiers), 5)  # Léa : 3 graphiques ; Tom : 2 (pas d'évaluation)
            self.assertTrue(all(Path(f).stat().st_size > 0 for f in fichiers))



class TestDeuxiemeChance(unittest.TestCase):
    """Plan P012 : les lignes "r" (deuxième chance du parcours) ne comptent pas dans la réussite."""

    def setUp(self):
        m = "francais-cm1-dictee-5-avoir-etre"
        lignes = [
            [100, m, "parcours/avoir", "avoir", 1, "e", 1, 3, "as", None],
            [110, m, "parcours/avoir", "avoir", 1, "e", 0, 4, "a", None],
            [120, m, "parcours/avoir", "avoir", 1, "r", 1, 5, "as", None],
            [130, m, "parcours/avoir", "avoir", 1, "e", 0, 4, "on", None],
            [140, m, "parcours/avoir", "avoir", 1, "r", 0, 5, "a", None],
            [150, m, "parcours/avoir", "avoir", 1, "e", 0, 4, "a", None],   # page quittée
        ]
        data = {"format": "miniprof-sauvegarde", "version": 1, "exported_at": 200,
                "profiles": [{"id": "p1", "name": "Tom"}], "events": {"p1": lignes}, "flags": []}
        self.tmp = tempfile.TemporaryDirectory()
        chemin = Path(self.tmp.name) / "e.export.json"
        chemin.write_text(json.dumps(data), encoding="utf-8")
        self.df = charger(chemin)

    def tearDown(self):
        self.tmp.cleanup()

    def test_reussite_sur_le_premier_essai(self):
        s = par_competence(self.df).set_index("competence")
        self.assertEqual(s.loc["avoir", "essais"], 4)
        self.assertEqual(s.loc["avoir", "reussite"], 25)

    def test_deuxiemes_chances(self):
        c = deuxiemes_chances(self.df).iloc[0]
        self.assertEqual((c["erreurs"], c["chances"], c["sauvees"], c["sauvees_pct"]), (3, 2, 1, 50))

    def test_affichage(self):
        with contextlib.redirect_stdout(io.StringIO()) as sortie:
            afficher(self.df)
        self.assertIn("Deuxième chance", sortie.getvalue())
        self.assertIn("Tom : 4 réponses", sortie.getvalue())


if __name__ == "__main__":
    unittest.main()
