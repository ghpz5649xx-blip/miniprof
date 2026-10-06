# Besoins — user stories et critères d'acceptation

> Référence figée de l'app v1 (étapes 1 à 7, modules JSON). Les besoins suivants sont dans
> le plan en cours (`docs/plan-modules-html.md`). Pas à relire pour suivre le projet.

Acteurs : **Parent** (mainteneur, crée les modules, suit la progression) et **Enfant**.
Étape de livraison indiquée entre crochets.

## A. Création de modules (parent, outils Python)

**A1 — Valider un module** [étape 1]
En tant que parent, je veux valider un fichier JSON produit par le LLM pour savoir s'il est
utilisable avant de le publier.
- `python tools/validate.py fichier.json` affiche « VALIDE » ou « INVALIDE » avec la liste des
  erreurs, chacune avec son chemin (ex. `questions[3].fields[0].answer (question q004)`).
- Les messages sont en français et compréhensibles sans connaître JSON Schema.
- Les avertissements (répartition, nombre de questions) n'empêchent pas la validation.
- La répartition compétence × difficulté est affichée.
- Code de sortie 0 si valide, 1 sinon.

**A2 — Corriger avec le LLM** [étape 1]
En tant que parent, je veux un texte prêt à recopier au LLM pour qu'il corrige ses erreurs.
- `--llm` produit : la liste des erreurs + « Corrige uniquement ces erreurs, sans changer les
  id, puis renvoie le JSON complet ».
- Si le JSON est entouré de texte ou de balises ```` ```json ````, l'outil le lit quand même ;
  `--nettoyer` réécrit le fichier en JSON propre.
- Une clé en double ou un JSON mal formé est signalé avec la ligne et la colonne.

**A3 — Générer le prompt** [étape 7]
En tant que parent, je veux un prompt prêt à coller dans le LLM, généré depuis le schéma.
- `python tools/prompt.py --mode nouveau` et `--mode lot <module.json>`.
- Le prompt inclut le schéma, les règles pédagogiques, l'obligation de vérifier les calculs,
  un exemple court ; en mode lot, la liste des compétences et des énoncés existants.
- Il est copié dans le presse-papiers (macOS) et écrit dans `docs/`.

**A4 — Fusionner un lot** [étape 7]
En tant que parent, je veux ajouter 40 à 60 questions à un module existant.
- `python tools/merge.py module.json lot.json` ajoute les nouvelles questions, remplace celles
  dont l'id existe, signale les énoncés quasi identiques, puis relance la validation.
- Le module n'est réécrit que si le résultat est valide.

**A5 — Publier un module** [étape 2]
En tant que parent, je veux qu'un module déposé dans `modules/` apparaisse dans l'app.
- `python tools/build_index.py` régénère `modules/index.json` (uniquement les modules valides).
- Après commit + push, le module apparaît dans la bibliothèque.

## B. Utilisation (enfant)

**B1 — Choisir son profil** [étape 2]
- L'accueil affiche un gros bouton par enfant (prénom) ; un clic ouvre sa bibliothèque.
- On peut créer un profil (prénom seul, 20 caractères max) ; changer de profil en 1 clic.

**B2 — Bibliothèque** [étape 2]
- Les modules de `modules/index.json` sont listés par matière avec titre et niveau.
- Un module illisible n'empêche pas les autres de s'afficher ; un message clair s'affiche à
  son ouverture.

**B3 — Apprendre** [étape 3]
- Les blocs de la leçon s'affichent un par un (« Étape n sur N »).
- Exemple résolu : chaque étape montre la pensée et son « pourquoi ».
- Mini-étapes : l'enfant complète une phrase à la fois ; si c'est faux, l'indice s'affiche ;
  si c'est juste, l'étape reste visible cochée et la suivante apparaît ; à la fin, la
  conclusion s'affiche.
- Fin de leçon : bouton « Je m'entraîne ».

**B4 — S'entraîner** [étape 4]
- Choix du niveau (1 à 4) et de la compétence (ou « Tout mélangé »).
- Questions tirées de la banque, sans répéter les 10 dernières, jamais une question signalée.
- « Un indice » affiche l'indice de la question.
- 1er essai faux : message ciblé (`common_errors`) ou générique, puis Réessayer / Indice /
  Voir la correction. 2e essai faux : correction affichée.
- Après 5 réussites du premier coup d'affilée : « Niveau suivant » proposé.
- « Revoir la méthode » ouvre la leçon de la compétence de la question.
- Nombres : virgule ou point acceptés, négatifs acceptés, espaces ignorés.
- Texte : casse, accents, espaces superflus et ponctuation finale ignorés.

**B5 — Évaluation** [étape 5]
- Choix « Mixte » ou niveau 1 à 4 ; 10 questions réparties sur les compétences.
- Ni indice ni correction pendant l'évaluation ; barre de progression.
- Résultat : note /10, temps, réussite par compétence, corrections dépliables (énoncé, ta
  réponse, bonne réponse, explication), bouton « Travailler : <compétence la plus faible> ».

**B6 — Signaler une question** [étape 6]
- Le bouton « Cette question me semble fausse » enregistre le signalement localement.
- La question n'est plus tirée (entraînement et évaluation) jusqu'à son rétablissement.

## C. Suivi (parent et enfant)

**C1 — Enregistrer chaque tentative** [étape 6]
- Chaque réponse (premier essai en entraînement, chaque question en évaluation) crée un
  événement : date, module, question, compétence, difficulté, mode, juste/faux, durée, réponse.
- Aucun compteur agrégé n'est stocké.

**C2 — Bilan** [étape 6]
- Par enfant : réussite par compétence (tous modules, puis par module), 10 dernières
  évaluations, compétences « à travailler » (< 60 % ou en baisse de plus de 15 points).
- « Travailler ce point » lance l'entraînement sur la compétence.
- Un enfant ne voit que son propre bilan.

**C3 — Sauvegarder et restaurer** [étape 7]
- Export : un fichier JSON contenant profils, événements et signalements.
- Import : contrôle, résumé, confirmation dans la page, puis remplacement des données.
- Au-delà de 70 % du quota, ou sans export depuis 14 jours, un rappel s'affiche.

**C4 — Analyser la progression** [étape 7]
- `python tools/analyse.py export.json` calcule par enfant et par compétence : taux de
  réussite, évolution, temps moyen, questions les plus ratées, compétences en baisse.
- Graphiques PNG enregistrés dans un dossier de sortie.

**C5 — Prévisualiser un module** [étape 7]
- Le parent charge un fichier JSON local : le module s'ouvre en mémoire, avec un bandeau
  « Aperçu — non enregistré », et aucun événement n'est enregistré.

## D. Exigences transverses

- **Sécurité** : aucun texte de module n'est interprété comme du HTML (`<b>` s'affiche
  littéralement) ; seuls `**gras**` et les retours à la ligne sont mis en forme.
- **Confidentialité** : aucune requête vers un autre domaine que celui de l'app (vérifiable dans
  l'onglet Réseau du navigateur).
- **Mobile** : utilisable sur un téléphone de 360 px de large, zones tactiles ≥ 48 px.
- **Accessibilité** : contrastes suffisants en clair et en sombre ; animations désactivées
  si `prefers-reduced-motion`.
- **Ids stables** : réimporter une version corrigée d'un module conserve l'historique.
