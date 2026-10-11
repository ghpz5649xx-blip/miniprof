# P001 — Questions à écrire

- **Statut** : exécuté le 12 oct. 2026 ; feed-back possible jusqu'au 26 oct. 2026, puis clos.
- **Origine** : retour du sponsor sur la dictée 5 (CM1) : le module, tout en choix (QCM), n'a pas
  corrigé « son » au lieu de « sont ». Reconnaître le bon mot n'apprend pas à l'écrire.

## Besoin
Pour l'orthographe, la conjugaison et la dictée, l'enfant **écrit** le mot ou le groupe de mots
au lieu de le choisir parmi des propositions.

## Périmètre et décisions
- Nouveau type de question `W()` dans le gabarit (`docs/gabarit-module.html`) : champ de saisie ;
  clavier de l'iPhone sans suggestions ni correction automatique (`autocorrect`, `autocomplete`,
  `spellcheck` coupés, `autocapitalize="none"`) ; correction stricte sur les lettres, les accents,
  le trait d'union ; souple sur les majuscules, les espaces en trop et la forme de l'apostrophe.
- Chaque faute prévue a son pourquoi (homophones : son / sont, on / ont, a / à, et / est) ; une
  faute non prévue reçoit « regarde les accents » ou « relis ton mot lettre par lettre ».
- 3 essais en entraînement avant la correction ; la réponse tapée est échappée au corrigé.
- Le choix (`Q()`) reste pour reconnaître une notion (nature d'un mot…).
- Règle écrite dans le skill `/nouveau-module` et dans `docs/module-html.md`.

## Livré
- Gabarit, `tools/tirage.py` (vérifie aussi les questions à écrire ; refuse une faute prévue égale
  à une bonne réponse), test `test_question_a_ecrire`.
- Dictée 5 refaite : noms, mots, avoir et être à écrire ; nature des mots en choix ; mêmes
  compétences, historique conservé.

## Vérifié (recette)
- Tests, `check_html.py`, `tirage.py` (30 000 questions, 0 erreur), recette navigateur 28 OK.
- Chromium : « son » refusé avec la bonne explication, « Sont » accepté ; HTML tapé affiché comme
  du texte.
- iPhone (sponsor, 12 oct.) : le clavier ne propose rien.

## Tâches du sponsor
- Aucune. Mesure de l'effet sur « son / sont » à la prochaine revue d'usage.

## Feed-back
(aucun pour l'instant)
