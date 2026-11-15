#!/usr/bin/env python3
"""Couverture d'un module de dictée : chaque mot de la liste est-il dans le module, et complet ?

Usage : python tools/couverture_dictee.py modules/<id>.html "mot1,mot2,mot3"
        python tools/couverture_dictee.py modules/<id>.html --liste mots.txt   (un mot par ligne)

Pourquoi : un module de dictée doit poser TOUS les mots à apprendre (plan P006 : 5 mots n'avaient
jamais été travaillés avec l'ancienne méthode). La liste vient d'une relecture des photos ; ce
contrôle compare cette liste à celle de la page, mot par mot, et vérifie que chaque mot a sa
devinette, son astuce et ses fautes prévues. Il lit le bloc /*DATA*/ … /*FIN DATA*/ de la page.
Code de sortie : 0 si tout est couvert, 1 sinon, 2 si la page ne se lit pas.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

NODE = r"""
const fs=require('fs'),vm=require('vm');
const h=fs.readFileSync(process.argv[1],'utf8');
const a=h.indexOf('/*DATA*/'),b=h.indexOf('/*FIN DATA*/');
if(a<0||b<0){console.log(JSON.stringify({erreur:'bloc /*DATA*/ … /*FIN DATA*/ introuvable'}));process.exit(0);}
const mots=vm.runInNewContext(h.slice(a,b)+';({NOMS,VERBES,MOTS})');
console.log(JSON.stringify(mots));
"""


def lire_mots(page):
    """Renvoie la liste des mots (dicts) de la page, ou lève ValueError."""
    node = shutil.which("node")
    if not node:
        raise ValueError("node introuvable")
    r = subprocess.run([node, "-e", NODE, str(page)], capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise ValueError(r.stderr.strip()[:300] or "lecture impossible")
    data = json.loads(r.stdout)
    if "erreur" in data:
        raise ValueError(data["erreur"])
    return [w for famille in ("NOMS", "VERBES", "MOTS") for w in data.get(famille, [])]


def norme(s):
    return " ".join(str(s).lower().replace("’", "'").split())


def comparer(mots_page, liste):
    """Renvoie la liste des problèmes (vide = tout est couvert)."""
    problemes = []
    page = {norme(w.get("m", "")): w for w in mots_page}
    attendus = [norme(m) for m in liste if norme(m)]
    for m in attendus:
        if m not in page:
            problemes.append(f"mot de la liste absent de la page : « {m} »")
    for m in page:
        if m not in attendus:
            problemes.append(f"mot de la page absent de la liste : « {m} »")
    ids = [w.get("id") for w in mots_page]
    for i in set(ids):
        if ids.count(i) > 1:
            problemes.append(f"identifiant en double : « {i} »")
    for w in mots_page:
        for champ in ("id", "dev", "tip"):
            if not str(w.get(champ, "")).strip():
                problemes.append(f"« {w.get('m')} » : champ « {champ} » vide")
        if not w.get("faux"):
            problemes.append(f"« {w.get('m')} » : aucune faute prévue (faux)")
    return problemes


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    page = Path(argv[1])
    if argv[2] == "--liste":
        liste = Path(argv[3]).read_text(encoding="utf-8").splitlines()
    else:
        liste = argv[2].split(",")
    try:
        mots = lire_mots(page)
    except (ValueError, OSError, json.JSONDecodeError, subprocess.SubprocessError) as e:
        print(f"Page illisible : {e}")
        return 2
    problemes = comparer(mots, liste)
    if problemes:
        print(f"{page.name} : couverture incomplète")
        for p in problemes:
            print("  ✗", p)
        return 1
    print(f"{page.name} : les {len(mots)} mots de la liste sont couverts, chacun avec devinette, astuce et fautes prévues.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
