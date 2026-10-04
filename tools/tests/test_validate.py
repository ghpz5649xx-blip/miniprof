"""Tests du validateur.

Lancer depuis la racine du dépôt :
    python -m unittest discover tools/tests -v

Principe : on part d'un module minimal valide (fixtures/minimal.json), on y introduit
UNE erreur, et on vérifie que le message attendu (en français, avec son chemin) apparaît.
"""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))  # pour importer common et validate

from common import normalize_text  # noqa: E402
from validate import texte_llm, valider_fichier  # noqa: E402

FIXTURES = TESTS / "fixtures"
MODULES = TESTS.parent.parent / "modules"
MINIMAL = json.loads((FIXTURES / "minimal.json").read_text(encoding="utf-8"))


def valider_dict(data, nom="minimal.json"):
    """Écrit le module dans un fichier temporaire et le valide."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / nom
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return valider_fichier(path)


def module_modifie(modification):
    data = copy.deepcopy(MINIMAL)
    modification(data)
    return valider_dict(data)


class ModulesDuDepot(unittest.TestCase):
    def test_tous_les_modules_sont_valides(self):
        fichiers = [p for p in MODULES.glob("*.json") if p.name != "index.json"]
        self.assertTrue(fichiers, "aucun module dans modules/")
        for path in fichiers:
            with self.subTest(module=path.name):
                rapport = valider_fichier(path)
                self.assertEqual(rapport.erreurs, [])

    def test_minimal_est_valide(self):
        self.assertEqual(valider_fichier(FIXTURES / "minimal.json").erreurs, [])


class ErreursDeSchema(unittest.TestCase):
    def assertErreur(self, rapport, *fragments):
        texte = "\n".join(rapport.erreurs)
        for fragment in fragments:
            self.assertIn(fragment, texte)

    def test_champ_obligatoire_manquant(self):
        r = module_modifie(lambda d: d.pop("title"))
        self.assertErreur(r, "(racine)", "champ obligatoire manquant : « title »")

    def test_reponse_texte_au_lieu_de_nombre(self):
        def m(d): d["questions"][0]["fields"][0]["answer"] = "5"
        self.assertErreur(module_modifie(m), "questions[0].fields[0].answer (question q1)", "doit être un nombre")

    def test_difficulte_hors_limites(self):
        def m(d): d["questions"][1]["difficulty"] = 5
        self.assertErreur(module_modifie(m), "questions[1].difficulty", "inférieur ou égal à 4")

    def test_type_de_question_inconnu(self):
        def m(d): d["questions"][0]["type"] = "dessin"
        self.assertErreur(module_modifie(m), "questions[0].type", "valeur non autorisée")

    def test_champ_inconnu(self):
        def m(d): d["questions"][0]["reponse"] = 5
        self.assertErreur(module_modifie(m), "champ inconnu : « reponse »")

    def test_champ_non_prevu_pour_le_type(self):
        def m(d): d["questions"][0]["accepted"] = ["cinq"]
        self.assertErreur(module_modifie(m), "questions[0] (question q1)", "« accepted » non prévu pour le type « number »")

    def test_id_mal_forme(self):
        def m(d): d["id"] = "Mon Module"
        self.assertErreur(module_modifie(m), "id", "format invalide")


class ErreursSemantiques(unittest.TestCase):
    def assertErreur(self, rapport, *fragments):
        texte = "\n".join(rapport.erreurs)
        for fragment in fragments:
            self.assertIn(fragment, texte)

    def test_competence_inconnue(self):
        def m(d): d["questions"][0]["skill"] = "soustraction"
        self.assertErreur(module_modifie(m), "questions[0] (question q1).skill", "« soustraction » absente de skills")

    def test_id_de_question_en_double(self):
        def m(d): d["questions"][1]["id"] = "q1"
        self.assertErreur(module_modifie(m), "l'id « q1 » est utilisé plusieurs fois")

    def test_bonne_reponse_absente_des_choix(self):
        def m(d): d["questions"][1]["answer"] = "z"
        self.assertErreur(module_modifie(m), "questions[1] (question q2).answer", "« z » ne fait pas partie des choix")

    def test_competence_sans_lecon(self):
        def m(d): d["skills"].append({"id": "sous", "label": "Soustraire"})
        self.assertErreur(module_modifie(m), "aucun bloc de leçon pour la compétence « sous »")

    def test_erreur_frequente_egale_a_la_bonne_reponse(self):
        def m(d): d["questions"][0]["common_errors"][0]["when"] = {"s": 5}
        self.assertErreur(module_modifie(m), "common_errors[0].when", "correspond à la bonne réponse")

    def test_erreur_frequente_sur_case_inconnue(self):
        def m(d): d["questions"][0]["common_errors"][0]["when"] = {"x": 1}
        self.assertErreur(module_modifie(m), "case(s) inconnue(s) x")

    def test_texte_erreur_frequente_deja_acceptee(self):
        def m(d): d["questions"][2]["common_errors"] = [{"when": "Somme", "message": "…"}]
        self.assertErreur(module_modifie(m), "« Somme » est une réponse acceptée")

    def test_avertissement_nom_de_fichier(self):
        r = valider_dict(copy.deepcopy(MINIMAL), nom="autre-nom.json")
        self.assertEqual(r.erreurs, [])
        self.assertTrue(any("devrait être « minimal.json »" in w for w in r.avertissements))


class LectureDuFichier(unittest.TestCase):
    def test_json_entoure_de_texte_est_extrait(self):
        r = valider_fichier(FIXTURES / "entoure.txt")
        self.assertTrue(r.extrait)
        self.assertEqual(r.data["id"], "minimal")
        # Lisible par l'outil, mais pas par l'app : on le signale comme erreur.
        self.assertEqual(len(r.erreurs), 1)
        self.assertIn("--nettoyer", r.erreurs[0])

    def test_json_casse(self):
        r = valider_fichier(FIXTURES / "casse.json")
        self.assertIn("ligne 3", r.erreurs[0])
        self.assertIn("virgule en trop", r.erreurs[0])

    def test_cle_en_double(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "double.json"
            path.write_text('{"id": "a", "id": "b"}', encoding="utf-8")
            r = valider_fichier(path)
        self.assertIn("la clé « id » apparaît deux fois", r.erreurs[0])


class TexteLLM(unittest.TestCase):
    def test_message_de_correction(self):
        def m(d): d["questions"][1]["answer"] = "z"
        texte = texte_llm(module_modifie(m))
        self.assertIn("Ton JSON contient les erreurs suivantes", texte)
        self.assertIn("« z » ne fait pas partie des choix", texte)
        self.assertIn("renvoie le JSON complet", texte)

    def test_rien_a_renvoyer_si_valide(self):
        self.assertIn("Aucune erreur", texte_llm(valider_fichier(FIXTURES / "minimal.json")))


class Normalisation(unittest.TestCase):
    def test_casse_accents_espaces_ponctuation(self):
        self.assertEqual(normalize_text("  Le   Quotient. "), "le quotient")
        self.assertEqual(normalize_text("ÉLÉPHANT !"), "elephant")
        self.assertEqual(normalize_text("l’été"), "l'ete")


if __name__ == "__main__":
    unittest.main()
