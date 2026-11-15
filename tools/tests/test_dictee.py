"""Tests du gabarit des dictées (docs/gabarit-dictee.html) et de tools/couverture_dictee.py."""

import shutil
import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent.parent
sys.path.insert(0, str(TESTS.parent))

from check_html import verifier_texte  # noqa: E402
from couverture_dictee import comparer, lire_mots  # noqa: E402
from tirage import tirer  # noqa: E402

GABARIT = ROOT / "docs" / "gabarit-dictee.html"
MODULE = ROOT / "modules" / "francais-cm1-dictee-7-sans-famille.html"


class TestGabaritDictee(unittest.TestCase):
    def test_respecte_le_contrat(self):
        rapport = verifier_texte(GABARIT.read_text(encoding="utf-8"), "francais-cm1-gabarit-dictee.html")
        self.assertEqual(rapport.erreurs, [])

    @unittest.skipUnless(shutil.which("node"), "node introuvable")
    def test_tirage_sans_erreur(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            page = Path(d) / "francais-cm1-gabarit-dictee.html"
            page.write_text(GABARIT.read_text(encoding="utf-8"), encoding="utf-8")
            r, echec = tirer(page, tirages=200, exemples=1)
        self.assertIsNone(echec)
        self.assertEqual(r["erreurs"], {})
        self.assertEqual(r["avertissements"], {})
        self.assertEqual(r["niveaux"], [1, 2])  # 1 = QCM, 2 = écriture


@unittest.skipUnless(shutil.which("node"), "node introuvable")
class TestCouverture(unittest.TestCase):
    def test_dictee_7_a_ses_24_mots(self):
        mots = lire_mots(MODULE)
        self.assertEqual(len(mots), 24)
        self.assertEqual(comparer(mots, [w["m"] for w in mots]), [])

    def test_mot_manquant_et_en_trop(self):
        mots = lire_mots(GABARIT)
        liste = [w["m"] for w in mots][1:] + ["nourriture"]
        pb = comparer(mots, liste)
        self.assertTrue(any("absent de la page" in p and "nourriture" in p for p in pb))
        self.assertTrue(any("absent de la liste" in p for p in pb))

    def test_mot_incomplet(self):
        mots = lire_mots(GABARIT)
        mots[0]["tip"] = ""
        self.assertTrue(any("tip" in p for p in comparer(mots, [w["m"] for w in mots])))


if __name__ == "__main__":
    unittest.main()
