"""Recette automatique dans un vrai navigateur (Chrome sans fenêtre).

Usage :
    python tools/recette_navigateur.py            # affiche OK / ECHEC, code 1 si un ECHEC

Pourquoi : l'app est en JS sans npm, donc sans outil de test JS. Plutôt que de
cliquer à la main, on ouvre une page de recette (tools/recette/modules-html.html)
servie à la racine du site : elle pilote les pages, lit le localStorage et
renvoie ses résultats à ce petit serveur (POST /__resultat).

Couvre le contrat des modules HTML (js/suivi.js, bilan, bibliothèque) et une
non-régression légère de l'app. Ne remplace pas la recette sur l'iPhone.
Chrome : variable d'environnement CHROME, sinon chemin macOS, sinon chromium /
google-chrome trouvé dans le PATH (session Claude Code dans le cloud, Linux).
"""

import http.server
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = Path(__file__).resolve().parent / "recette" / "modules-html.html"
CHROME_MAC = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DELAI = 90  # secondes avant d'abandonner

resultat = {"texte": ""}
verrou = threading.Lock()


class Serveur(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *args):
        pass  # pas de journal de chaque fichier servi

    def do_GET(self):
        if self.path == "/__recette.html":
            corps = PAGE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        texte = self.rfile.read(n).decode("utf-8")
        # Chaque envoi reprend tous les précédents, mais le serveur les traite en parallèle :
        # un envoi plus ancien peut arriver après « FIN » et l'effacer (recette bloquée 90 s).
        # On garde donc toujours le plus long.
        with verrou:
            if len(texte) >= len(resultat["texte"]):
                resultat["texte"] = texte
        self.send_response(204)
        self.end_headers()


def trouver_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    if Path(CHROME_MAC).exists():
        return CHROME_MAC
    for nom in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        if shutil.which(nom):
            return shutil.which(nom)
    return None


def main():
    chemin = trouver_chrome()
    if not chemin or not Path(chemin).exists():
        sys.exit("Chrome introuvable : installer Chrome ou Chromium, ou donner son chemin dans la "
                 "variable d'environnement CHROME.")
    options = ["--headless=new", "--disable-gpu", "--no-first-run", "--no-proxy-server"]
    # En root (conteneur Linux du cloud), Chrome refuse de démarrer avec son bac à sable :
    # sans cette option il quitte aussitôt, et on ne recevait « aucun résultat ».
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        options.append("--no-sandbox")
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Serveur)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    adresse = f"http://127.0.0.1:{serveur.server_port}/__recette.html"

    # Messages de Chrome gardés dans un fichier : affichés seulement s'il s'arrête tout seul.
    with tempfile.TemporaryDirectory() as profil, tempfile.TemporaryFile() as erreurs:
        chrome = subprocess.Popen(
            [chemin, *options, f"--user-data-dir={profil}", "--remote-debugging-port=0", adresse],
            stdout=subprocess.DEVNULL, stderr=erreurs)
        try:
            fin = time.time() + DELAI
            while "FIN" not in resultat["texte"] and time.time() < fin and chrome.poll() is None:
                time.sleep(0.5)
        finally:
            arret_tout_seul = chrome.poll() is not None
            chrome.terminate()
            chrome.wait(timeout=10)
        if arret_tout_seul and "FIN" not in resultat["texte"]:
            erreurs.seek(0)
            fin_journal = erreurs.read().decode("utf-8", "replace").strip().splitlines()[-10:]
            print(f"✘ Chrome s'est arrêté sans finir la recette ({chemin}) :")
            print("\n".join(fin_journal) or "(aucun message)")
            serveur.shutdown()
            sys.exit(1)
    serveur.shutdown()

    texte = resultat["texte"].replace("\nFIN", "").strip()
    print(texte or "Aucun résultat reçu.")
    lignes = texte.splitlines()
    echecs = [l for l in lignes if l.startswith("ECHEC")]
    if "FIN" not in resultat["texte"]:
        print(f"\n✘ Recette interrompue (pas de FIN après {DELAI} s).")
        sys.exit(1)
    nb_ok = sum(1 for l in lignes if l.startswith("OK"))
    print(f"\n{'✘' if echecs else '✔'} {nb_ok} OK, {len(echecs)} échec(s).")
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
