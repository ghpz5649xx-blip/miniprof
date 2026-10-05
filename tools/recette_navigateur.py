"""Recette automatique dans un vrai navigateur (Chrome sans fenêtre).

Usage :
    python tools/recette_navigateur.py            # affiche OK / ECHEC, code 1 si un ECHEC

Pourquoi : l'app est en JS sans npm, donc sans outil de test JS. Plutôt que de
cliquer à la main, on ouvre une page de recette (tools/recette/modules-html.html)
servie à la racine du site : elle pilote les pages, lit le localStorage et
renvoie ses résultats à ce petit serveur (POST /__resultat).

Couvre le contrat des modules HTML (js/suivi.js, bilan, bibliothèque) et une
non-régression légère de l'app. Ne remplace pas la recette sur l'iPhone.
Chrome : chemin macOS par défaut, ou variable d'environnement CHROME.
"""

import http.server
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = Path(__file__).resolve().parent / "recette" / "modules-html.html"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
DELAI = 90  # secondes avant d'abandonner

resultat = {"texte": ""}


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
        resultat["texte"] = self.rfile.read(n).decode("utf-8")
        self.send_response(204)
        self.end_headers()


def main():
    if not Path(CHROME).exists():
        sys.exit(f"Chrome introuvable : {CHROME} (variable d'environnement CHROME)")
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Serveur)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    adresse = f"http://127.0.0.1:{serveur.server_port}/__recette.html"

    with tempfile.TemporaryDirectory() as profil:
        chrome = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             f"--user-data-dir={profil}", "--remote-debugging-port=0", adresse],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            fin = time.time() + DELAI
            while "FIN" not in resultat["texte"] and time.time() < fin:
                time.sleep(0.5)
        finally:
            chrome.terminate()
            chrome.wait(timeout=10)
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
