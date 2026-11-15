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
        page = FIXTURES / "html" / "mini-cm1-test.html"
        shutil.copy(page, self.tmp / page.name)                                  # module valide
        shutil.copy(page, self.tmp / "mauvais-nom.html")                         # id ≠ nom du fichier
        (self.tmp / "page-cassee.html").write_text("<p>pas de fiche</p>", encoding="utf-8")
        # Un ancien index ne doit pas être pris pour un module.
        (self.tmp / "index.json").write_text('{"modules": []}', encoding="utf-8")
        self.index, self.ecartes = construire_index(self.tmp)

    def test_seuls_les_modules_valides_sont_indexes(self):
        self.assertEqual(sorted(m["file"] for m in self.index["modules"]), ["mini-cm1-test.html"])

    def module(self, fichier):
        return next(m for m in self.index["modules"] if m["file"] == fichier)

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
        self.assertEqual(sorted(noms), ["mauvais-nom.html", "page-cassee.html"])
        self.assertIn("erreur", noms["page-cassee.html"])

    def test_vrai_dossier_modules(self):
        index, ecartes = construire_index(TESTS.parent.parent / "modules")
        self.assertEqual(ecartes, [])
        self.assertGreaterEqual(len(index["modules"]), 1)


class TestBrouillons(unittest.TestCase):
    """modules/brouillons.json : modules publiés mais pas encore relus par le parent."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        page = FIXTURES / "html" / "mini-cm1-test.html"
        shutil.copy(page, self.tmp / page.name)
        # un second module valide, sous un autre id
        autre = page.read_text(encoding="utf-8").replace("mini-cm1-test", "mini-cm1-autre")
        (self.tmp / "mini-cm1-autre.html").write_text(autre, encoding="utf-8")

    def brouillons(self, contenu):
        (self.tmp / "brouillons.json").write_text(contenu, encoding="utf-8")

    def test_sans_fichier_aucun_brouillon(self):
        index, ecartes = construire_index(self.tmp)
        self.assertEqual(ecartes, [])
        self.assertFalse(any("brouillon" in m for m in index["modules"]))

    def test_brouillon_marque(self):
        self.brouillons('{"brouillons": ["mini-cm1-test"]}')
        index, ecartes = construire_index(self.tmp)
        self.assertEqual(ecartes, [])  # brouillons.json n'est pas pris pour un module
        marques = {m["id"]: m.get("brouillon", False) for m in index["modules"]}
        self.assertEqual(marques, {"mini-cm1-test": True, "mini-cm1-autre": False})

    def test_id_inconnu_signale(self):
        self.brouillons('{"brouillons": ["fantome"]}')
        _, ecartes = construire_index(self.tmp)
        self.assertEqual(len(ecartes), 1)
        self.assertEqual(ecartes[0][0], "brouillons.json")
        self.assertIn("fantome", ecartes[0][1])

    def test_format_casse_signale(self):
        self.brouillons('["mini-cm1-test"]')
        index, ecartes = construire_index(self.tmp)
        self.assertEqual([nom for nom, _ in ecartes], ["brouillons.json"])
        self.assertFalse(any("brouillon" in m for m in index["modules"]))


if __name__ == "__main__":
    unittest.main()
