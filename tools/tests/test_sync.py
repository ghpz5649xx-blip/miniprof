"""Règles qui doivent rester synchronisées entre l'app (JS) et les outils (Python).

- REQUIRED / REQUIRED_QUESTION / TYPES_CONNUS / BLOCS_CONNUS de js/check-module.js ≡ schéma
  (risque R5 : dérive entre le contrôle de l'app et validate.py) ;
- normalize_text() ≡ normalizeText() de js/answers.js : voir test_normalisation.py et les cas
  partagés de fixtures/normalisation.json ;
- aucun innerHTML dans le JS de l'app (risque R7 : injection de contenu de module) ;
- js/suivi.js (modules HTML) écrit seulement par addEvents() de js/events.js : l'ordre des
  cases d'un événement reste défini à un seul endroit ;
- le skill /nouveau-module et docs/parent-iphone.md ne citent que des fichiers qui existent, et
  le skill lance les trois contrôles avant de publier (une session mobile le suit à la lettre).
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
JS = ROOT / "js"
SCHEMA = json.loads((ROOT / "schema" / "module.schema.json").read_text(encoding="utf-8"))


def liste_js(nom):
    """Lit `const <nom> = [ "a", "b" ];` dans js/check-module.js."""
    source = (JS / "check-module.js").read_text(encoding="utf-8")
    m = re.search(r"const " + nom + r" = \[(.*?)\];", source, re.DOTALL)
    if not m:
        raise AssertionError(f"const {nom} = [...] introuvable dans js/check-module.js")
    return re.findall(r'"([^"]+)"', m.group(1))


class TestSynchronisation(unittest.TestCase):
    def test_champs_obligatoires_du_module(self):
        self.assertEqual(liste_js("REQUIRED"), SCHEMA["required"],
                         "mettre à jour REQUIRED dans js/check-module.js")

    def test_champs_obligatoires_d_une_question(self):
        self.assertEqual(liste_js("REQUIRED_QUESTION"), SCHEMA["$defs"]["question"]["required"],
                         "mettre à jour REQUIRED_QUESTION dans js/check-module.js")

    def test_types_de_question(self):
        self.assertEqual(liste_js("TYPES_CONNUS"),
                         SCHEMA["$defs"]["question"]["properties"]["type"]["enum"])

    def test_types_de_bloc(self):
        self.assertEqual(liste_js("BLOCS_CONNUS"),
                         SCHEMA["$defs"]["bloc"]["properties"]["type"]["enum"])

    def test_aucun_innerhtml(self):
        interdit = re.compile(r"innerHTML|outerHTML|insertAdjacentHTML|document\.write")
        fautifs = []
        for p in JS.rglob("*.js"):
            for n, ligne in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                # Les commentaires peuvent citer la règle : on ne regarde que le code.
                code = ligne.split("//")[0]
                if interdit.search(code):
                    fautifs.append(f"{p.relative_to(ROOT)}:{n}")
        self.assertEqual(fautifs, [], "HTML injecté interdit : utiliser el() / richText()")

    def test_suivi_passe_par_events(self):
        source = (JS / "suivi.js").read_text(encoding="utf-8")
        self.assertIn('import { addEvents, maintenant } from "./events.js"', source)
        code = "\n".join(l.split("//")[0] for l in source.splitlines())
        self.assertNotRegex(code, r"localStorage|writeKey", "suivi.js doit passer par addEvents()")

    def test_skill_nouveau_module(self):
        skill = (ROOT / ".claude" / "skills" / "nouveau-module" / "SKILL.md").read_text(encoding="utf-8")
        for commande in ("tools/check_html.py", "tools/build_index.py", "unittest discover tools/tests"):
            self.assertIn(commande, skill)
        # Étape 12 allégée (comité n° 1, D5) : un nouveau module part en brouillon, « valide <id> » le publie.
        for etape in ("modules/brouillons.json", "## 7. Valider un module", "tools/tirage.py"):
            self.assertIn(etape, skill)
        guide = (ROOT / "docs" / "parent-iphone.md").read_text(encoding="utf-8")
        cites = set(re.findall(r"(?:tools|docs|modules|schema|js)/[\w./-]+\.(?:py|md|json|html|js)", skill + guide))
        cites.add(".claude/skills/nouveau-module/SKILL.md")
        absents = sorted(c for c in cites if not (ROOT / c).exists())
        self.assertEqual(absents, [], "fichiers cités par le skill ou le guide parent introuvables")


if __name__ == "__main__":
    unittest.main()
