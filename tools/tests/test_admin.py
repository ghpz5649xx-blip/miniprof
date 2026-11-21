"""Tests de admin.py : lecture et réécriture du pilotage, synchro Git, accès réservé au Mac."""

import datetime
import http.client
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))  # pour importer admin

import admin  # noqa: E402

ROOT = TESTS.parent.parent
AUJOURDHUI = datetime.date(2026, 11, 21)

PILOTAGE = """# Pilotage

Intro.

## Tâches du sponsor

Règle des tâches.

- **19 oct. 2026** — Exporter les données. **Bloque P012**.
- **Quand tu veux** — Relire le README.

## Consignes pour Claude

Règle des consignes.
"""

INDEX = """# Index des plans

| N° | Date | Titre | Statut | Mots-clés | Résumé | Fiche |
|---|---|---|---|---|---|---|
| P001 | 12 oct. 2026 | Questions à écrire | exécuté | saisie | résumé | `plans/P001-questions-a-ecrire.md` |

## Idées (sans fiche)

Intro des idées.

- **Revue d'usage** (depuis le 12 oct. 2026, priorité haute) : exports des enfants.
"""


def git(dossier, *args):
    return subprocess.run(["git", *args], cwd=dossier, capture_output=True, text=True, check=True).stdout


class TestLectureEcriture(unittest.TestCase):
    def test_fichiers_du_depot_relus_et_reecrits_a_l_identique(self):
        # Le format des vrais fichiers doit rester lisible par l'écran : sinon il refuserait d'écrire.
        for fichier, section in [(admin.PILOTAGE, admin.SECTION_TACHES), (admin.PILOTAGE, admin.SECTION_CONSIGNES),
                                 (admin.INDEX, admin.SECTION_IDEES)]:
            texte = (ROOT / fichier).read_text(encoding="utf-8")
            route = next(r for r, (f, s, _) in admin.ECRITURES.items() if (f, s) == (fichier, section))
            lignes = admin.ECRITURES[route][2]
            if section == admin.SECTION_TACHES:
                liste = admin.lire_taches(texte, AUJOURDHUI)
            elif section == admin.SECTION_CONSIGNES:
                liste = admin.lire_consignes(texte)
            else:
                liste = admin.lire_idees(texte)
            self.assertEqual(admin.remplacer_section(texte, section, lignes(liste)), texte, fichier)

    def test_taches_et_echeance(self):
        taches = admin.lire_taches(PILOTAGE, AUJOURDHUI)
        self.assertEqual([t["echeance"] for t in taches], ["19 oct. 2026", "Quand tu veux"])
        self.assertEqual([t["echue"] for t in taches], [True, False])
        self.assertIn("**Bloque P012**", taches[0]["texte"])  # le gras du texte est gardé

    def test_ajout_retrait_report_sans_toucher_au_reste(self):
        taches = [{"echeance": "1 déc. 2026", "texte": "Exporter les données."},
                  {"echeance": "Quand tu veux", "texte": "Nouvelle\ntâche  sur deux lignes"}]
        texte = admin.remplacer_section(PILOTAGE, admin.SECTION_TACHES, admin.lignes_taches(taches))
        self.assertIn("- **1 déc. 2026** — Exporter les données.\n", texte)
        self.assertIn("- **Quand tu veux** — Nouvelle tâche sur deux lignes\n", texte)
        self.assertNotIn("Relire le README", texte)
        self.assertTrue(texte.startswith("# Pilotage\n\nIntro.\n\n## Tâches du sponsor\n\nRègle des tâches.\n\n- "))
        self.assertTrue(texte.endswith("## Consignes pour Claude\n\nRègle des consignes.\n"))

    def test_consigne_ajoutee_en_fin_de_fichier(self):
        texte = admin.remplacer_section(PILOTAGE, admin.SECTION_CONSIGNES,
                                        admin.lignes_consignes([{"date": "21 nov. 2026", "texte": "Feed-back P013 : bien"}]))
        self.assertTrue(texte.endswith("Règle des consignes.\n\n- **21 nov. 2026** — Feed-back P013 : bien\n"))
        self.assertEqual(admin.lire_consignes(texte), [{"date": "21 nov. 2026", "texte": "Feed-back P013 : bien"}])

    def test_idees_ordre_et_priorite(self):
        idees = admin.lire_idees(INDEX) + [{"titre": "Nouvelle", "depuis": "21 nov. 2026", "priorite": "basse",
                                            "description": "à voir"}]
        idees.reverse()
        texte = admin.remplacer_section(INDEX, admin.SECTION_IDEES, admin.lignes_idees(idees))
        self.assertEqual([i["titre"] for i in admin.lire_idees(texte)], ["Nouvelle", "Revue d'usage"])
        self.assertIn("| P001 |", texte)  # le tableau des plans n'est pas touché
        with self.assertRaises(admin.ErreurFormat):
            admin.lignes_idees([{"titre": "x", "depuis": "y", "priorite": "urgente", "description": "z"}])

    def test_plans_lus(self):
        self.assertEqual(admin.lire_plans(INDEX, AUJOURDHUI),
                         [{"id": "P001", "date": "12 oct. 2026", "titre": "Questions à écrire", "statut": "exécuté",
                           "archive": False}])

    def test_plans_archives(self):
        # Fini, ou exécuté et délai de feed-back passé ; « exécuté en partie » reste actif.
        cas = [("clos", "6 oct. 2026", True),
               ("abandonné (14 oct. 2026)", "6 oct. 2026", True),
               ("archivé (21 nov. 2026 : fusionné dans P012)", "11 oct. 2026", True),
               ("intégré dans P012", "11 oct. 2026", True),
               ("exécuté (feed-back jusqu'au 26 oct.)", "12 oct. 2026", True),
               ("exécuté (feed-back jusqu'au 29 nov.)", "15 nov. 2026", False),
               ("exécuté en partie (15 nov. 2026)", "7 oct. 2026", False),
               ("à mûrir (basse)", "6 oct. 2026", False),
               ("en cours", "12 oct. 2026", False)]
        for statut, date_plan, attendu in cas:
            self.assertEqual(admin.est_archive(statut, date_plan, AUJOURDHUI), attendu, statut)
        # Délai qui passe le 31 décembre : l'année suivante.
        self.assertFalse(admin.est_archive("exécuté (feed-back jusqu'au 5 janv.)", "22 déc. 2026",
                                           datetime.date(2027, 1, 2)))

    def test_ligne_ecrite_a_la_main_illisible_bloque_l_ecriture(self):
        # Sinon l'écran, qui ne l'a pas affichée, l'effacerait sans prévenir.
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        casse = PILOTAGE.replace("- **Quand tu veux** —", "- Quand tu veux :")
        (tmp / "pilotage.md").write_text(casse, encoding="utf-8")
        with self.assertRaises(admin.ErreurFormat):
            admin.ecrire(tmp, "/api/taches", [])
        self.assertEqual((tmp / "pilotage.md").read_text(encoding="utf-8"), casse)

    def test_gras_interdit_dans_l_echeance(self):
        with self.assertRaises(admin.ErreurFormat):
            admin.lignes_taches([{"echeance": "**demain**", "texte": "x"}])

    def test_dates(self):
        self.assertEqual(admin.lire_date_fr("1 déc. 2026"), datetime.date(2026, 12, 1))
        self.assertIsNone(admin.lire_date_fr("Quand tu veux"))
        self.assertIsNone(admin.lire_date_fr("31 févr. 2026"))
        self.assertEqual(admin.date_fr(datetime.date(2026, 8, 3)), "3 août 2026")


class TestImages(unittest.TestCase):
    def test_chemin_image(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        (tmp / "plans" / "images").mkdir(parents=True)
        (tmp / "plans" / "images" / "schema.png").write_bytes(b"png")
        (tmp / "secret.txt").write_text("non", encoding="utf-8")
        self.assertEqual(admin.chemin_image(tmp, "plans/images/schema.png"),
                         (tmp / "plans" / "images" / "schema.png").resolve())
        self.assertIsNone(admin.chemin_image(tmp, "secret.txt"))
        self.assertIsNone(admin.chemin_image(tmp, "plans/../../schema.png"))


class TestSansInnerHTML(unittest.TestCase):
    def test_ecran_d_admin_sans_html_injecte(self):
        # Les fiches et le pilotage sont affichés nœud par nœud, comme le texte des modules dans l'app.
        interdit = ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write")
        for p in (TESTS.parent / "admin").iterdir():
            code = "\n".join(ligne.split("//")[0] for ligne in p.read_text(encoding="utf-8").splitlines())
            self.assertFalse([m for m in interdit if m in code], p.name)


class TestSynchro(unittest.TestCase):
    """Sur un vrai dépôt temporaire, avec un dépôt nu comme origin."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.origin = self.tmp / "origin.git"
        self.depot = self.tmp / "depot"
        git(self.tmp, "init", "-q", "--bare", "-b", "main", str(self.origin))
        git(self.tmp, "clone", "-q", str(self.origin), str(self.depot))
        for cle, valeur in [("user.name", "test"), ("user.email", "test@example.invalid"), ("commit.gpgsign", "false")]:
            git(self.depot, "config", cle, valeur)
        git(self.depot, "checkout", "-q", "-b", "main")
        (self.depot / "plans").mkdir()
        (self.depot / "pilotage.md").write_text(PILOTAGE, encoding="utf-8")
        (self.depot / "plans" / "index.md").write_text(INDEX, encoding="utf-8")
        (self.depot / "app.js").write_text("// travail\n", encoding="utf-8")
        git(self.depot, "add", ".")
        git(self.depot, "commit", "-q", "-m", "départ")
        git(self.depot, "push", "-q", "origin", "main")

    def test_commit_et_push_des_seuls_fichiers_du_pilotage(self):
        (self.depot / "app.js").write_text("// travail en cours de l'agent\n", encoding="utf-8")
        admin.ecrire(self.depot, "/api/consignes", [{"date": "21 nov. 2026", "texte": "Corriger X"}])
        ok, message = admin.synchroniser(self.depot, "Pilotage : consigne ajoutée")
        self.assertTrue(ok, message)
        self.assertEqual(git(self.origin, "log", "-1", "--format=%s", "main").strip(), "Pilotage : consigne ajoutée")
        self.assertEqual(git(self.origin, "show", "--name-only", "--format=", "main").split(), ["pilotage.md"])
        # Le travail de l'agent reste sur le disque, non committé.
        self.assertEqual((self.depot / "app.js").read_text(encoding="utf-8"), "// travail en cours de l'agent\n")
        self.assertIn("app.js", git(self.depot, "status", "--porcelain"))

    def test_pas_sur_main_rien_n_est_committe(self):
        git(self.depot, "checkout", "-q", "-b", "essai")
        admin.ecrire(self.depot, "/api/consignes", [{"date": "21 nov. 2026", "texte": "Corriger X"}])
        ok, _ = admin.synchroniser(self.depot, "Pilotage : test")
        self.assertFalse(ok)
        self.assertEqual(git(self.depot, "log", "-1", "--format=%s").strip(), "départ")

    def test_origin_injoignable_commit_garde_en_local(self):
        git(self.depot, "remote", "set-url", "origin", str(self.tmp / "absent.git"))
        admin.ecrire(self.depot, "/api/consignes", [{"date": "21 nov. 2026", "texte": "Corriger X"}])
        ok, message = admin.synchroniser(self.depot, "Pilotage : test")
        self.assertFalse(ok)
        self.assertIn("pas envoyé", message)
        self.assertEqual(git(self.depot, "log", "-1", "--format=%s").strip(), "Pilotage : test")


class TestServeur(unittest.TestCase):
    def setUp(self):
        self.serveur = admin.creer_serveur(ROOT, 0)
        self.port = self.serveur.server_address[1]
        threading.Thread(target=self.serveur.serve_forever, daemon=True).start()
        self.addCleanup(self.serveur.server_close)
        self.addCleanup(self.serveur.shutdown)

    def requete(self, methode, chemin, hote=None, corps=None, type_=None):
        connexion = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        entetes = {"Host": hote or f"127.0.0.1:{self.port}"}
        if type_:
            entetes["Content-Type"] = type_
        connexion.request(methode, chemin, body=corps, headers=entetes)
        reponse = connexion.getresponse()
        return reponse.status, reponse.read().decode("utf-8")

    def test_ecoute_seulement_sur_le_mac(self):
        self.assertEqual(self.serveur.server_address[0], "127.0.0.1")

    def test_page_et_etat(self):
        statut, page = self.requete("GET", "/")
        self.assertEqual(statut, 200)
        self.assertIn("Admin miniprof", page)
        statut, corps = self.requete("GET", "/api/etat")
        self.assertEqual(statut, 200)
        self.assertIn("taches", json.loads(corps))

    def test_fiche(self):
        statut, corps = self.requete("GET", "/api/fiche?id=P013")
        self.assertEqual(statut, 200)
        self.assertIn("P013", json.loads(corps)["texte"])
        self.assertEqual(self.requete("GET", "/api/fiche?id=../CLAUDE")[0], 404)

    def test_hote_etranger_refuse(self):
        self.assertEqual(self.requete("GET", "/api/etat", hote="pirate.example:80")[0], 403)
        self.assertEqual(self.requete("POST", "/api/taches", hote="pirate.example:80",
                                      corps="{}", type_="application/json")[0], 403)

    def test_lecteur_markdown_servi(self):
        statut, corps = self.requete("GET", "/markdown.js")
        self.assertEqual(statut, 200)
        self.assertIn("export function afficherMarkdown", corps)

    def test_images_du_depot_seulement(self):
        # Ni sortie du dépôt, ni fichier qui ne soit pas une image.
        for chemin in ["/fichier/../../../../etc/passwd", "/fichier/%2e%2e/%2e%2e/etc/passwd",
                       "/fichier/pilotage.md", "/fichier/plans/absente.png"]:
            self.assertEqual(self.requete("GET", chemin)[0], 404, chemin)

    def test_post_sans_json_refuse(self):
        # Un formulaire d'un autre site ne peut envoyer que du texte ou un formulaire, pas du JSON.
        self.assertEqual(self.requete("POST", "/api/taches", corps="liste=[]", type_="text/plain")[0], 403)


if __name__ == "__main__":
    unittest.main()
