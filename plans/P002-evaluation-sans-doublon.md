# P002 — Évaluation sans question en double

- **Statut** : exécuté le 12 oct. 2026 ; feed-back possible jusqu'au 26 oct. 2026, puis clos.
- **Origine** : le sponsor a vu deux fois la même question dans une évaluation.

## Besoin
Une évaluation ne pose jamais deux fois la même question.

## Périmètre et décisions
- Cause : chaque question était tirée au hasard sans regarder les précédentes.
- `tirerSansDoublon()` dans le gabarit et les 5 modules HTML : une question déjà sortie (même
  énoncé, mêmes choix, même réponse) est retirée (jusqu'à 30 essais). Un énoncé générique
  (« Lequel est l'intrus ? ») peut revenir avec d'autres mots : ce n'est pas un doublon.

## Vérifié (recette)
- Chromium, 15 évaluations par module (75 en tout) : 11 doublons avant, 0 après ; pas d'erreur JS.
- `check_html.py`, `tirage.py`, tests, recette navigateur 28 OK.

## Tâches du sponsor
- Aucune.

## Feed-back
(aucun pour l'instant)
