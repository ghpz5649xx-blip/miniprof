"""Tests de check_html.py : le contrat des modules HTML (docs/module-html.md)."""

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))  # pour importer check_html

from check_html import verifier_fichier, verifier_texte, texte_llm  # noqa: E402

PAGE = TESTS / "fixtures" / "html" / "mini-cm1-test.html"
NOM = PAGE.name
VALIDE = PAGE.read_text(encoding="utf-8")


def avec(ajout):
    """La page valide, avec `ajout` glissé dans son script."""
    return VALIDE.replace("<script>\n", "<script>\n" + ajout + "\n", 1)


class TestCheckHtml(unittest.TestCase):
    def test_page_valide(self):
        rapport = verifier_fichier(PAGE)
        self.assertEqual(rapport.erreurs, [])
        self.assertEqual(rapport.fiche["id"], "mini-cm1-test")
        self.assertIn("Aucune erreur", texte_llm(rapport))

    def test_interdits(self):
        # Chaque ligne ajoutée doit être refusée (une erreur au moins, avec son numéro de ligne).
        for ajout in [
            "fetch('/x');",
            "new XMLHttpRequest();",
            "import('./x.js');",
            "localStorage.setItem('a', 1);",
            "sessionStorage.clear();",
            "document.cookie = 'a=1';",
            "var s = 'https://fonts.googleapis.com/css';",
            "new Worker('w.js');",
            "navigator.sendBeacon('/x');",
        ]:
            with self.subTest(ajout=ajout):
                erreurs = verifier_texte(avec(ajout), NOM).erreurs
                self.assertTrue(erreurs, "aurait dû être refusé")
                self.assertTrue(all(e.startswith("ligne ") for e in erreurs), erreurs)

    def test_balises_interdites(self):
        for balise in ['<iframe src="x.html"></iframe>', '<img src="//exemple.org/a.png">']:
            with self.subTest(balise=balise):
                self.assertTrue(verifier_texte(VALIDE.replace("<body>", "<body>" + balise), NOM).erreurs)

    def test_namespace_svg_autorise(self):
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', VALIDE)  # la page valide en contient un

    def test_suivi_obligatoire(self):
        sans_script = VALIDE.replace('<script type="module" src="../js/suivi.js"></script>', "")
        self.assertIn("suivi : charger", " ".join(verifier_texte(sans_script, NOM).erreurs))
        sans_appel = VALIDE.replace("window.miniprof.reponse(", "window.miniprof.autre(")
        self.assertIn("miniprof.reponse", " ".join(verifier_texte(sans_appel, NOM).erreurs))

    def test_csp_obligatoire(self):
        sans_csp = VALIDE.replace("connect-src 'none'; ", "")
        self.assertIn("sécurité", " ".join(verifier_texte(sans_csp, NOM).erreurs))

    def test_nom_du_fichier(self):
        self.assertIn("mini-cm1-test.html", " ".join(verifier_texte(VALIDE, "autre.html").erreurs))

    def test_fiche(self):
        cas = {
            "fiche absente": (VALIDE.replace('id="miniprof-module"', 'id="autre"'), "exactement un"),
            "JSON invalide": (VALIDE.replace('"level": "CM1",', '"level": "CM1"'), "JSON invalide"),
            "niveau inconnu": (VALIDE.replace('"CM1"', '"CM9"'), "fiche.level"),
            "matière inconnue": (VALIDE.replace('"sciences"', '"physique"'), "fiche.subject"),
            "id invalide": (VALIDE.replace('"id": "mini-cm1-test"', '"id": "Mini Test"'), "fiche.id"),
            "titre manquant": (VALIDE.replace('"title": "Module HTML minimal",', ""), "fiche.title"),
            "compétence en double": (VALIDE.replace('"id": "deux"', '"id": "un"'), "en double"),
            "compétence sans libellé": (VALIDE.replace(', "label": "Deuxième compétence"', ""), "fiche.skills[1]"),
        }
        for nom, (texte, attendu) in cas.items():
            with self.subTest(cas=nom):
                erreurs = " ".join(verifier_texte(texte, NOM).erreurs)
                self.assertIn(attendu, erreurs)

    def test_texte_llm(self):
        texte = texte_llm(verifier_texte(avec("fetch('/x');"), NOM))
        self.assertIn("contrat miniprof", texte)
        self.assertIn("fetch", texte)

    def test_vrais_modules_html(self):
        for page in sorted((TESTS.parent.parent / "modules").glob("*.html")):
            with self.subTest(page=page.name):
                self.assertEqual(verifier_fichier(page).erreurs, [])


if __name__ == "__main__":
    unittest.main()
