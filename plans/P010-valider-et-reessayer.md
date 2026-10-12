# P010 — Valider et Réessayer

- **Statut** : exécuté le 12 oct. 2026 ; feed-back possible jusqu'au 26 oct. 2026, puis clos.
- **Origine** : retour du sponsor après la session du fils (CM1, dictée 5), 12 oct. 2026.

## Besoin
(I) Le bouton « Valider » ne s'affiche que lorsque l'élève a proposé une réponse.
(II) En entraînement, « Réessayer » efface la dernière proposition et fait disparaître « Valider »
jusqu'à ce que l'élève propose autre chose.

## Décisions
- **Une proposition** = un mot tapé (non vide), un choix, ou un dessin non vide (circuit).
- Après une erreur, le bouton principal devient « Réessayer ». Il vide le champ ou le choix. Si
  l'élève retape ou rechoisit sans cliquer « Réessayer », « Valider » revient tout de suite.
- Le message d'erreur reste affiché pendant la nouvelle tentative (il aide à corriger).
- Dessin (circuit) : « Réessayer » n'efface pas le dessin (corriger un schéma vaut mieux que le
  refaire) ; « Valider » reste visible tant que le schéma n'est pas vide.
- Même comportement en évaluation (« Valider et continuer » caché tant qu'il n'y a pas de réponse).
- La touche Entrée ne valide pas quand « Valider » est caché.
- Hors périmètre : la répétition des questions, traitée par le plan suivant (tirage par
  compétence fine).

## Livré
- Gabarit `docs/gabarit-module.html` et les 5 modules HTML (mêmes fonctions `boutons()`,
  `surProposition()`, `reessayer()`). Les modules JSON ne changent pas.

## Vérifié (recette)
- Tests (77), `check_html.py` et `tirage.py` sur les 5 modules, recette navigateur 55 OK.
- Chromium (dictée 5, Paddington, tables, circuit) : « Valider » caché au départ, visible après
  saisie ou choix, caché de nouveau si le champ est vidé ; « Réessayer » vide le champ ; retaper
  fait revenir « Valider » ; dessin et évaluation corrects ; aucune erreur JS.

## Tâches du sponsor
- Sur l'iPhone, dans une dictée : taper un mot faux, appuyer sur « Réessayer », vérifier que le
  champ est vide, que « Valider » a disparu et que le clavier reste ouvert.

## Feed-back
(aucun pour l'instant)
