# Expérience utilisateur de référence

Résumé du prototype `reference/division-euclidienne.html` (lu une seule fois, à ne plus relire).
Ce document décrit **ce que l'enfant voit et vit** ; l'app finale reproduit ces comportements,
mais avec un contenu lu dans un fichier de module au lieu d'être écrit dans le code.

## Principes généraux

- Une seule page, écrans successifs. Chaque écran (sauf l'accueil) a une **barre du haut** avec
  un bouton « ← Retour » et le titre de l'écran.
- Colonne centrale étroite (≈ 640 px max), gros boutons (≥ 48 px de haut), cartes arrondies.
- Thème clair / sombre automatique, couleurs pédagogiques constantes (dividende bleu, diviseur
  orange, quotient vert, reste rose). *Dans l'app finale : couleurs de thème conservées, mais
  pas de couleurs par notion (le contenu est générique).*
- **Entrée** dans un champ = clic sur le bouton principal de l'écran.
- Le focus est placé automatiquement dans le premier champ de saisie.
- Animations courtes (fondu des messages), désactivées si `prefers-reduced-motion`.
- Les messages de feedback sont des encadrés colorés : vert (réussi), rouge (erreur),
  bleu (correction / info), orange (indice / consigne).

## Accueil

- Bandeau titre du module + « Salut <prénom> ! Apprends, entraîne-toi, puis teste-toi. »
- Si aucun prénom : champ « Comment t'appelles-tu ? » + OK. *(App finale : remplacé par le
  choix de profil enfant.)*
- Quatre grandes cartes-boutons :
  1. **Apprendre** — « L'histoire de Nolan et ses 341 cartes, pas à pas »
  2. **S'entraîner** — « Des questions à volonté, avec indices et corrections »
  3. **Évaluation** — « 10 questions, sans aide, avec une note à la fin » + dernière note
  4. **Bilan** — « Ce qui est réussi, ce qu'il reste à travailler »

## Apprendre

- Suite d'étapes, affichage « Étape n sur N » + titre de l'étape.
- Types d'étapes observés :
  - **Histoire** : texte d'accroche (Nolan partage 341 cartes entre 19 coéquipiers), schéma de
    la division posée avec « ? », légende du vocabulaire (dividende, diviseur, quotient, reste).
    Bouton « C'est parti ».
  - **Table à compléter** : 9 champs (1 × 19 … 9 × 19), bouton « Vérifier » ; cases justes en
    vert, fausses en rouge, astuce (« d'une ligne à la suivante, on ajoute 19 »). Quand tout est
    juste, le bouton devient « Continuer ».
  - **Mini-étapes guidées** (cœur pédagogique) : une intro, puis une phrase à trous à la fois
    (« 10 × 19 = ▢ »). L'enfant tape la réponse, « Valider ».
    - Juste → la ligne passe dans la liste des étapes réussies (affichée avec la réponse en
      gras et ✓), l'étape suivante apparaît.
    - Faux → encadré orange « Pas encore. » + indice propre à l'étape ; la saisie est
      sélectionnée pour être corrigée. Pas de limite d'essais.
    - Saisie non numérique → « Écris un nombre entier. »
    - Fin de la série → encadré vert de conclusion (+ schéma), bouton « Continuer ».
  - **À retenir** : récapitulatif de la règle (dividende = diviseur × quotient + reste ;
    reste < diviseur), boutons « Je m'entraîne » et « Accueil ».
- La leçon raconte un **cheminement de pensée** : décomposer (10 × 19 puis 7 × 19), vérifier
  (preuve), puis une variante surprise (342 cartes → reste 0 : « Nolan a de la ruse »).

## S'entraîner

- **Écran de réglage** : choix du niveau (puces « Niveau 1 … 4 », avec sous-titre décrivant la
  difficulté) et de la compétence (« Tout mélangé » ou une compétence). Bouton « Commencer ».
- **Écran de question** :
  - En tête : « Niveau n : X réussies du premier coup sur Y ».
  - Carte avec l'énoncé, puis soit des champs numériques étiquetés (ex. « quotient », « reste »),
    soit des boutons de choix (QCM, sélection surlignée).
  - Boutons « Valider » et « Un indice ».
  - **Indice** : encadré orange (peut contenir une table de multiplication, une astuce).
  - Réponse incomplète → consigne orange (« Remplis toutes les cases… » / « Choisis une
    réponse. »), sans compter d'essai.
  - **1er essai faux** → encadré rouge « Pas tout à fait. » + **diagnostic ciblé** selon
    l'erreur (ex. « Ton reste (25) n'est pas plus petit que le diviseur (19)… ») ; boutons
    « Réessayer », « Un indice », « Voir la correction ».
  - **2e essai faux** ou « Voir la correction » → encadré bleu « Correction » avec explication
    pas à pas ; champs marqués vert/rouge, QCM verrouillé avec la bonne réponse surlignée ;
    bouton « Question suivante ».
  - **Juste** → encadré vert avec un encouragement tiré au hasard (« Bravo ! », « Bien joué ! »,
    « Exact ! »…), mention « Tu as trouvé après une correction » si 2e essai ; bouton
    « Question suivante ».
  - **Montée de niveau** : après 5 réussites du premier coup d'affilée (et niveau < 4), message
    « Tu enchaînes 5 réussites : tu peux passer au niveau suivant » + bouton « Niveau suivant ».
  - Seul le **premier essai** compte dans les statistiques.
- Retour → écran de réglage.

## Évaluation

- **Écran de réglage** : « Prête pour l'évaluation ? 10 questions, sans indice. Tu vois les
  corrections à la fin. Prends un brouillon et un stylo. » Choix du niveau : « Mixte (du
  facile au difficile) » ou niveau 1 à 4. Bouton « Lancer l'évaluation ».
- Composition : 10 questions réparties sur toutes les compétences ; en mixte, difficulté
  croissante (2, 2, 2, 3, 3, 3, 3, 4, 4, 4).
- **Écran de question** : barre de progression en pastilles (faites / en cours / à venir),
  « Question n sur 10 », pas d'indice, pas de correction. Bouton « Valider et continuer »
  (dernier : « Valider et terminer »). Réponse incomplète → consigne, on reste sur la question.
- Retour pendant l'évaluation → abandon, retour au réglage.
- **Résultat** :
  - Grande note « 7 / 10 », message selon la note (≥ 9 excellent, ≥ 7 très bien, ≥ 5 bon début,
    sinon « pas de panique : reprends Apprendre »), temps passé (min s).
  - « Par compétence » : barre de progression par compétence (rouge < 50 %, orange < 80 %,
    vert sinon) avec score x/y.
  - « Les corrections » : une ligne dépliable par question (✓/✗ + compétence), contenant
    l'énoncé, « Ta réponse », « Bonne réponse » (si faux) et l'explication.
  - Boutons « Travailler : <compétence la plus faible> » (si pas 100 %), « Recommencer »,
    « Accueil ».

## Bilan

- Phrase de synthèse : « N questions traitées, dont M réussies du premier coup (P %) ».
- « Réussite par compétence » : barre + pourcentage, ou « pas encore travaillé ».
- « Dernières évaluations » : 10 dernières, date + niveau + note.
- Mention « Les résultats sont enregistrés dans le navigateur de cet appareil. »
- Bouton « Effacer les résultats » avec **confirmation en deux clics** (le libellé devient
  « Confirmer : tout effacer »).

## Ce que l'app finale change volontairement

| Prototype | App finale |
|---|---|
| Questions générées au hasard par du code | Banque statique de questions lue dans le module JSON |
| Diagnostic d'erreur calculé par du code | `common_errors` facultatif dans chaque question + message générique sinon |
| Niveaux définis par des plages de nombres | `difficulty` 1 à 4 de chaque question |
| Un prénom unique | Plusieurs profils enfants |
| Compteurs agrégés en stockage | Événements bruts, tout est recalculé |
| HTML écrit dans les textes | Texte échappé, seulement `**gras**` et retours à la ligne |
| Schéma coloré de division posée | Pas de schéma graphique en v1 |
| Google Fonts | Polices système (aucune requête externe) |
| Bilan global | Bilan par enfant, tous modules, avec « Travailler ce point » |
