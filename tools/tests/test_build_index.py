"""Tests de build_index.py : seuls les modules valides et bien nommés sont indexés."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))  # pour importer build_index

from build_index import construire_index  # noqa: E402

FIXTURES = TESTS / "fixtures"


class TestBuildIndex(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copy(FIXTURES / "minimal.json", self.tmp / "minimal.json")       # valide
        shutil.copy(FIXTURES / "casse.json", self.tmp / "casse.json")           # invalide
        shutil.copy(FIXTURES / "minimal.json", self.tmp / "mauvais-nom.json")   # id ≠ nom
        page = FIXTURES / "html" / "mini-cm1-test.html"
        shutil.copy(page, self.tmp / page.name)                                  # module HTML valide
        (self.tmp / "page-cassee.html").write_text("<p>pas de fiche</p>", encoding="utf-8")
        # Un ancien index ne doit pas être pris pour un module.
        (self.tmp / "index.json").write_text('{"modules": []}', encoding="utf-8")
        self.index, self.ecartes = construire_index(self.tmp)

    def test_seuls_les_modules_valides_sont_indexes(self):
        self.assertEqual(sorted(m["file"] for m in self.index["modules"]),
                         ["mini-cm1-test.html", "minimal.json"])

    def module(self, fichier):
        return next(m for m in self.index["modules"] if m["file"] == fichier)

    def test_champs_de_l_index(self):
        m = self.module("minimal.json")
        self.assertEqual(m["kind"], "json")
        source = json.loads((FIXTURES / "minimal.json").read_text(encoding="utf-8"))
        self.assertEqual(m["id"], source["id"])
        self.assertEqual(m["title"], source["title"])
        self.assertEqual(m["questions"], len(source["questions"]))
        for champ in ("version", "subject", "level", "description"):
            self.assertIn(champ, m)
        # Utilisé par le bilan de l'app (js/screens/report.js).
        self.assertEqual(m["skills"], [{"id": s["id"], "label": s["label"]} for s in source["skills"]])

    def test_module_html(self):
        # La bibliothèque ouvre la page (kind) ; le bilan lit les compétences de la fiche.
        m = self.module("mini-cm1-test.html")
        self.assertEqual(m["kind"], "html")
        self.assertEqual(m["id"], "mini-cm1-test")
        self.assertEqual([s["id"] for s in m["skills"]], ["un", "deux"])
        for champ in ("title", "subject", "level", "description"):
            self.assertIn(champ, m)

    def test_ecartes_avec_raison(self):
        noms = dict(self.ecartes)
        self.assertEqual(sorted(noms), ["casse.json", "mauvais-nom.json", "page-cassee.html"])
        self.assertIn("erreur", noms["casse.json"])
        self.assertIn("minimal.json", noms["mauvais-nom.json"])

    def test_vrai_dossier_modules(self):
        index, ecartes = construire_index(TESTS.parent.parent / "modules")
        self.assertEqual(ecartes, [])
        self.assertGreaterEqual(len(index["modules"]), 1)


if __name__ == "__main__":
    unittest.main()
