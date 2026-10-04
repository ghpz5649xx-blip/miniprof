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
        # Un ancien index ne doit pas être pris pour un module.
        (self.tmp / "index.json").write_text('{"modules": []}', encoding="utf-8")
        self.index, self.ecartes = construire_index(self.tmp)

    def test_seul_le_module_valide_est_indexe(self):
        self.assertEqual([m["file"] for m in self.index["modules"]], ["minimal.json"])

    def test_champs_de_l_index(self):
        m = self.index["modules"][0]
        source = json.loads((FIXTURES / "minimal.json").read_text(encoding="utf-8"))
        self.assertEqual(m["id"], source["id"])
        self.assertEqual(m["title"], source["title"])
        self.assertEqual(m["questions"], len(source["questions"]))
        for champ in ("version", "subject", "level", "description"):
            self.assertIn(champ, m)

    def test_ecartes_avec_raison(self):
        noms = dict(self.ecartes)
        self.assertEqual(sorted(noms), ["casse.json", "mauvais-nom.json"])
        self.assertIn("erreur", noms["casse.json"])
        self.assertIn("minimal.json", noms["mauvais-nom.json"])

    def test_vrai_dossier_modules(self):
        index, ecartes = construire_index(TESTS.parent.parent / "modules")
        self.assertEqual(ecartes, [])
        self.assertGreaterEqual(len(index["modules"]), 1)


if __name__ == "__main__":
    unittest.main()
