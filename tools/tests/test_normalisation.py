"""normalize_text() sur les cas partagés avec js/answers.js (fixtures/normalisation.json).

Le même fichier sert à vérifier normalizeText() côté navigateur (docs/recette.md, étape 3) :
ajouter un cas ici, c'est l'ajouter aux deux côtés.
"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import normalize_text  # noqa: E402

CAS = json.loads((Path(__file__).parent / "fixtures" / "normalisation.json").read_text(encoding="utf-8"))


class CasPartages(unittest.TestCase):
    def test_texte(self):
        for entree, attendu in CAS["texte"]:
            with self.subTest(entree=entree):
                self.assertEqual(normalize_text(entree), attendu)


if __name__ == "__main__":
    unittest.main()
