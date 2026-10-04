"""Analyse la progression des enfants à partir d'une sauvegarde de l'app.

Usage :
    python tools/analyse.py exports/miniprof-2026-10-04.export.json
    python tools/analyse.py export.json --sortie exports/analyse   # dossier des graphiques

La sauvegarde vient de l'écran « Sauvegarde » de l'app (bouton « Exporter mes données »).
Format (voir js/backup.js) :
    {"format": "miniprof-sauvegarde", "version": 1, "exported_at": <s>,
     "profiles": [{"id", "name"}], "events": {<id profil>: [ligne, ...]}, "flags": [...]}
Une ligne d'événement est un tableau court (voir js/events.js), colonnes dans cet ordre :
    date (s), module, question, compétence, difficulté, mode ("e" entraînement /
    "v" évaluation), juste (1/0), durée (s), réponse, évaluation (clé commune ou null)

Affiche dans le terminal, par enfant : réussite et temps moyen par compétence, compétences
en baisse, questions les plus ratées, notes des évaluations. Enregistre des graphiques PNG.
Le dossier de sortie par défaut est sous exports/, ignoré par Git (données personnelles).
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # pas de fenêtre : on enregistre seulement des fichiers PNG
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

COLONNES = ["date", "module", "question", "competence", "difficulte", "mode", "juste",
            "duree", "reponse", "evaluation"]

# Même règle « en baisse » que l'app (js/stats.js) : les 10 derniers essais d'une compétence
# ont un taux de réussite inférieur de plus de 15 points aux essais précédents, avec au moins
# 5 essais de chaque côté. À garder synchronisé avec stats.js.
ESSAIS_RECENTS = 10
BAISSE_POINTS = 15
MIN_POUR_BAISSE = 5
SEUIL_FAIBLE = 60  # % : en dessous, compétence « à travailler »


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------

def charger(path):
    """Lit la sauvegarde et renvoie un DataFrame : une ligne par réponse, triée par date."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != "miniprof-sauvegarde":
        raise ValueError("ce fichier n'est pas une sauvegarde miniprof")
    prenoms = {p["id"]: p["name"] for p in data.get("profiles", [])}

    lignes = []
    for profil, evenements in data.get("events", {}).items():
        for ligne in evenements:
            # Défensif, comme l'app : une ligne abîmée est ignorée.
            if isinstance(ligne, list) and len(ligne) >= 8:
                complete = (list(ligne) + [None, None])[:len(COLONNES)]
                lignes.append([prenoms.get(profil, profil)] + complete)

    df = pd.DataFrame(lignes, columns=["enfant"] + COLONNES)
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df["juste"] = df["juste"] == 1
    # Tri stable : les réponses d'une même évaluation (même date) gardent leur ordre.
    return df.sort_values("date", kind="stable").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Calculs
# ---------------------------------------------------------------------------

def est_en_baisse(justes):
    """`justes` : suite de booléens dans l'ordre chronologique."""
    justes = list(justes)
    recents, avant = justes[-ESSAIS_RECENTS:], justes[:-ESSAIS_RECENTS]
    if len(recents) < MIN_POUR_BAISSE or len(avant) < MIN_POUR_BAISSE:
        return False
    taux = lambda xs: sum(xs) / len(xs) * 100  # noqa: E731
    return taux(avant) - taux(recents) > BAISSE_POINTS


def par_competence(df):
    """Par enfant, module et compétence : essais, réussite (%), temps moyen (s), en baisse."""
    groupes = df.groupby(["enfant", "module", "competence"], sort=False)
    resultat = groupes.agg(
        essais=("juste", "size"),
        reussite=("juste", "mean"),
        temps_moyen=("duree", "mean"),
    )
    resultat["reussite"] = (resultat["reussite"] * 100).round(0)
    resultat["temps_moyen"] = resultat["temps_moyen"].round(1)
    resultat["en_baisse"] = groupes["juste"].apply(est_en_baisse)
    resultat["a_travailler"] = (resultat["reussite"] < SEUIL_FAIBLE) | resultat["en_baisse"]
    return resultat.reset_index()


def plus_ratees(df, n=10):
    """Les `n` questions les plus ratées par enfant (au moins un échec)."""
    stats = df.groupby(["enfant", "module", "question"]).agg(
        essais=("juste", "size"), echecs=("juste", lambda s: int((~s).sum())))
    stats = stats[stats["echecs"] > 0].reset_index()
    stats = stats.sort_values(["enfant", "echecs", "essais"], ascending=[True, False, True])
    return stats.groupby("enfant").head(n).reset_index(drop=True)


def evolution_hebdo(df):
    """Réussite (%) par enfant, compétence et semaine (lundi de la semaine)."""
    semaine = df["date"].dt.to_period("W").dt.start_time.rename("semaine")
    resultat = df.groupby(["enfant", "competence", semaine])["juste"].mean() * 100
    return resultat.round(0).rename("reussite").reset_index()


def evaluations(df):
    """Une ligne par évaluation : enfant, module, date, niveau, note, total."""
    ev = df[(df["mode"] == "v") & df["evaluation"].notna()]
    if ev.empty:
        return pd.DataFrame(columns=["enfant", "module", "date", "niveau", "note", "total"])
    resultat = ev.groupby(["enfant", "module", "evaluation"], sort=False).agg(
        date=("date", "min"), note=("juste", "sum"), total=("juste", "size")).reset_index()
    # Clé d'évaluation "<début>/<niveau>" (voir js/events.js).
    resultat["niveau"] = resultat["evaluation"].str.split("/").str[1]
    return resultat.drop(columns="evaluation").sort_values("date").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Graphiques
# ---------------------------------------------------------------------------

def graphiques(df, sortie):
    """Enregistre les PNG dans `sortie` et renvoie la liste des fichiers créés."""
    sortie = Path(sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    fichiers = []
    scores = par_competence(df)
    hebdo = evolution_hebdo(df)
    notes = evaluations(df)

    for enfant in df["enfant"].unique():
        # 1. Réussite par compétence (barres horizontales, rouge si à travailler).
        s = scores[scores["enfant"] == enfant]
        fig, ax = plt.subplots(figsize=(8, 0.5 * len(s) + 1.5))
        couleurs = ["#b3261e" if t else "#2e7d4f" for t in s["a_travailler"]]
        # Deux modules peuvent avoir une compétence de même id : on préfixe alors le module.
        noms = s["competence"] if s["module"].nunique() == 1 else s["module"] + " · " + s["competence"]
        ax.barh(noms, s["reussite"], color=couleurs)
        ax.set_xlim(0, 100)
        ax.axvline(SEUIL_FAIBLE, color="grey", linestyle="--", linewidth=1)
        ax.set_xlabel("Réussite (%)")
        ax.set_title(f"{enfant} : réussite par compétence (rouge = à travailler)")
        ax.invert_yaxis()
        fichiers.append(_enregistrer(fig, sortie / f"{enfant}-competences.png"))

        # 2. Évolution par semaine, une courbe par compétence.
        h = hebdo[hebdo["enfant"] == enfant]
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for competence, lignes in h.groupby("competence"):
            ax.plot(lignes["semaine"], lignes["reussite"], marker="o", label=competence)
        ax.set_ylim(0, 105)
        ax.set_ylabel("Réussite (%)")
        ax.set_title(f"{enfant} : réussite par semaine")
        ax.legend(fontsize=8)
        fig.autofmt_xdate()
        fichiers.append(_enregistrer(fig, sortie / f"{enfant}-evolution.png"))

        # 3. Notes des évaluations (sur 10 ramenées en %).
        n = notes[notes["enfant"] == enfant]
        if not n.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(n["date"], n["note"] / n["total"] * 100, marker="o")
            ax.set_ylim(0, 105)
            ax.set_ylabel("Note (%)")
            ax.set_title(f"{enfant} : notes des évaluations")
            fig.autofmt_xdate()
            fichiers.append(_enregistrer(fig, sortie / f"{enfant}-evaluations.png"))
    return fichiers


def _enregistrer(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Affichage
# ---------------------------------------------------------------------------

def afficher(df):
    pd.set_option("display.width", 120)
    scores = par_competence(df)
    ratees = plus_ratees(df)
    notes = evaluations(df)
    for enfant in df["enfant"].unique():
        print(f"\n=== {enfant} : {int((df['enfant'] == enfant).sum())} réponses ===")
        s = scores[scores["enfant"] == enfant].drop(columns="enfant")
        print("\nPar compétence :")
        print(s.to_string(index=False))
        a_travailler = s[s["a_travailler"]]["competence"].tolist()
        print("\nÀ travailler : " + (", ".join(a_travailler) if a_travailler else "rien de particulier"))
        r = ratees[ratees["enfant"] == enfant].drop(columns="enfant")
        print("\nQuestions les plus ratées :")
        print(r.to_string(index=False) if not r.empty else "aucune")
        n = notes[notes["enfant"] == enfant]
        if not n.empty:
            print("\nÉvaluations :")
            print(n.drop(columns="enfant").to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description="Analyse une sauvegarde miniprof.")
    parser.add_argument("export", help="fichier exporté depuis l'app (.export.json)")
    parser.add_argument("--sortie", default="exports/analyse", help="dossier des graphiques PNG")
    args = parser.parse_args()

    try:
        df = charger(args.export)
    except (OSError, ValueError) as e:
        print(f"✘ Sauvegarde illisible : {e}")
        sys.exit(1)
    if df.empty:
        print("Aucune réponse dans cette sauvegarde.")
        sys.exit(0)

    afficher(df)
    fichiers = graphiques(df, args.sortie)
    print(f"\n✔ {len(fichiers)} graphique(s) dans {args.sortie}/")


if __name__ == "__main__":
    main()
