# P013 — Profondeur des questions des modules (répétition)

- **Statut** : première réflexion enregistrée le 14 oct. 2026 ; **à mûrir** (plan d'étude à lancer).
  Un seul plan ouvert à la fois : P012 l'est déjà.
- **Origine** : sponsor, 14 oct. 2026. Reproche régulier des enfants : les questions se répètent.
  Même cause racine que P011 (« est » une fois sur deux en Être niveau 2) ; P011 traite le choix
  de la compétence, P013 traite la **diversité des questions elles-mêmes**.
- **Sortie attendue** : une analyse chiffrée, puis un plan d'exécution (jamais du code d'emblée).

## Hypothèse de diagnostic (à mesurer)
1. **Espace trop étroit** : peu de questions distinctes par compétence et niveau (conjugaison
   être/avoir ≈ 2 verbes × 6 personnes × quelques temps).
2. **Tirage sans mémoire** : même un espace correct se répète.

Mesure sans rien changer : (a) extension de `tools/tirage.py` pour compter les questions
*distinctes* par module, compétence et niveau ; (b) dans les exports des enfants
(`tools/analyse.py`), taux de répétition vécu (même question et même énoncé dans une fenêtre
de N réponses).

## Pistes de remède (de la moins chère à la plus chère)
| # | Piste | Remarque |
|---|---|---|
| A | **Anti-répétition** dans le moteur du gabarit : ne pas retirer une question vue récemment | Change la grammaire du gabarit → plan avec go. Mémoire dérivée du journal d'événements (pas de nouveau format) ou nouvelle clé `miniprof.v1.*` |
| B | **Élargir l'espace** : plus de phrases, de lexique, de contextes ; surtout **varier le type de tâche** (compléter, repérer l'erreur, transformer, choisir l'auxiliaire, dictée de phrase) | Même verbe, tâche différente = profondeur perçue ; vaut pour la conjugaison |
| C | **Paliers de difficulté** : monter vers des questions en contexte (texte court, homophone, accord du participe) | Lien avec P012 / P011 |
| D | **Plafond assumé** : quand une compétence est épuisée, passer à l'étape suivante du parcours plutôt que répéter | Lien avec P012 (rappel espacé) |

## Recommandation
Mesurer d'abord, puis A + B ciblés sur les deux modules les plus joués (Dictée 5 CM1, Le verbe 6e) ;
C et D dans la suite de P012. Ne pas toucher aux données des enfants.

## Étapes
1. Environnement : `pip install -r tools/requirements.txt` (sans `jsonschema`, les contrôles et
   8 tests sur 22 échouent) ; état des lieux : `check_html` et `tirage` sur les 8 modules.
2. Mesure de diversité et de répétition vécue (voir plus haut).
3. Grille de qualité par module : diversité, niveau, exactitude face à `programmes/`.
4. Décision du sponsor sur A/B/C/D, puis plan d'exécution.

## Décisions à prendre par le sponsor
- A change le gabarit commun : l'instruire comme plan avec go séparé ?
- Quels modules en premier (proposition : Dictée 5 CM1, Le verbe 6e) ?
