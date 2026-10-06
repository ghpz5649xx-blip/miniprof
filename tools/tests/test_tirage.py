"""Tests de tirage.py et du gabarit des modules HTML (docs/gabarit-module.html)."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent.parent
sys.path.insert(0, str(TESTS.parent))  # pour importer check_html et tirage

from check_html import verifier_texte  # noqa: E402
from tirage import tirer  # noqa: E402

GABARIT = ROOT / "docs" / "gabarit-module.html"
TEXTE = GABARIT.read_text(encoding="utf-8")


class TestGabarit(unittest.TestCase):
    def test_gabarit_respecte_le_contrat(self):
        # Une session copie le gabarit dans modules/ : il doit déjà passer check_html.
        rapport = verifier_texte(TEXTE, "autre-6e-gabarit.html")
        self.assertEqual(rapport.erreurs, [])


@unittest.skipUnless(shutil.which("node"), "node introuvable")
class TestTirage(unittest.TestCase):
    def tirer_texte(self, texte):
        with tempfile.TemporaryDirectory() as d:
            page = Path(d) / "autre-6e-gabarit.html"
            page.write_text(texte, encoding="utf-8")
            return tirer(page, tirages=200, exemples=2)

    def test_gabarit_sans_erreur(self):
        r, echec = tirer(GABARIT, tirages=200, exemples=2)
        self.assertIsNone(echec)
        self.assertEqual(r["erreurs"], {})
        self.assertEqual(r["avertissements"], {})
        self.assertEqual(r["tirages"], 2 * 2 * 200)  # 2 compétences, 2 niveaux
        self.assertIn("exemple, niveau 1", r["exemples"])

    def test_choix_en_double_detecte(self):
        # Sans le filtre x!==s, le distracteur s+0 vaut la bonne réponse : deux bonnes réponses.
        texte = TEXTE.replace("const faux=[s+1,", "const faux=[s+0,s+1,").replace("x!==s&&", "")
        r, _ = self.tirer_texte(texte)
        self.assertTrue(any("bonne réponse est en double" in k or "même valeur" in k for k in r["erreurs"]))

    def test_undefined_detecte(self):
        r, _ = self.tirer_texte(TEXTE.replace("`<p>${a} + ${b} = <b>${s}</b>.</p>`", "`<p>${a.x}</p>`"))
        self.assertTrue(any("undefined" in k for k in r["erreurs"]))

    def test_generateur_qui_plante(self):
        r, _ = self.tirer_texte(TEXTE.replace("function genComparer(level){", "function genComparer(level){null.x;"))
        self.assertTrue(any("plante" in k for k in r["erreurs"]))

    def test_page_sans_point_de_tirage(self):
        r, _ = self.tirer_texte(TEXTE.replace("if(window.__miniprofTirage)", "if(false)"))
        self.assertTrue(any("__miniprofTirage" in k for k in r["erreurs"]))

    def test_erreur_de_syntaxe(self):
        r, echec = self.tirer_texte(TEXTE.replace("function genComparer(level){", "function genComparer(level){{"))
        self.assertIsNone(r)
        self.assertIn("ne se charge pas", echec)


if __name__ == "__main__":
    unittest.main()
