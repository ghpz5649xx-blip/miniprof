## Objectif

Construis une petite application web d'entraînement et d'évaluation pour mes 2 enfants
(primaire/collège), en français, toutes matières. Priorités : **maintenance minimale pour
un seul mainteneur**, **hébergement gratuit**, **zéro serveur à surveiller**.

Le fichier `reference/division-euclidienne.html` est un prototype fonctionnel d'un seul
« module ». Il sert de référence pour l'**expérience utilisateur** (écrans Apprendre /
S'entraîner / Évaluation / Bilan, indices, corrections, niveaux, feedback). Ne le copie pas
tel quel : son contenu (questions, générateurs aléatoires, textes) est écrit en dur dans le
code, alors que dans l'app finale chaque module est un **fichier de données**. Lis-le une
fois, résume les écrans et comportements dans `docs/ux.md`, et ne le relis plus ensuite.

## Mon profil (pour calibrer tes réponses)

- Je code en **Python** (Django, gRPC/Kafka, SQLite) et je manipule **pandas** au quotidien,
  matplotlib un peu. Je suis à l'aise avec Git/GitHub (je gère moi-même dépôt et
  déploiement). Je suis **faible en JavaScript** : je dois pouvoir lire et corriger le code
  de l'app. Préfère un JS simple, plat, bien commenté (le « pourquoi », en français), sans
  syntaxe exotique.
- Retour d'expérience à respecter : sur un projet précédent, stocker de la donnée lourde
  dans SQLite a créé des goulots d'étranglement. Principe retenu : **données volumineuses
  en fichiers, métadonnées légères en base/stockage clé-valeur.**
- **Pas d'asynchrone** sauf si c'est incontournable : pas de workers, pas de service worker,
  pas d'IndexedDB, pas de file d'événements. Le seul appel asynchrone toléré est le
  chargement des fichiers de modules, isolé dans **une seule fonction** commentée.
- Mon métier : risk manager, ancien business analyst et chef de projet. Je sais exprimer un
  besoin et faire une recette. Parle-moi en termes fonctionnels, propose des critères
  d'acceptation, et laisse-moi tester chaque étape (voir « Méthode »).

## Choix d'architecture (à challenger en mode plan, sans l'imposer par défaut)

Ma recommandation de départ :
- **Application front 100 % statique** (HTML + CSS + JavaScript vanilla en modules ES, aucun
  framework, aucune étape de build, aucune dépendance npm) hébergée sur **GitHub Pages**.
  Raison : gratuit durablement, rien à patcher côté serveur, pas de base à gérer.
- **Pas de Django / Flask / serveur** en v1. Si tu penses qu'un backend Python est justifié,
  dis-le dans le plan avec le coût de maintenance et l'option d'hébergement gratuite
  réaliste ; sinon, reste en statique.
- **Outillage Python en ligne de commande** dans `tools/`, hors de l'app, pour tout ce qui
  est manipulation de données (là où je suis efficace) : validation et fusion de modules,
  analyse de la progression avec pandas/matplotlib. Dépendances séparées
  (`tools/requirements.txt`), l'app n'en dépend pas.

Répartition des données (principe « lourd en fichiers, léger en stockage local ») :
- **Modules** (lourds : leçon + 100 à 200 questions) = **fichiers JSON dans `modules/`** du
  dépôt, listés dans `modules/index.json`. Ajouter un module = déposer un fichier + commit +
  push. Rien n'est stocké dans le navigateur.
- **Progression** (légère) = `localStorage`, par profil enfant, sous forme d'**événements
  compacts** (tableaux courts plutôt qu'objets verbeux). Surveille la taille : au-delà de
  ~70 % du quota, affiche un rappel d'export. Offre l'export complet en un fichier JSON et
  l'import de sauvegarde. Aucune synchronisation entre appareils.

## Cas d'usage central

1. Je photographie cours, exercices et contrôles (1 à 10 photos).
2. Je les envoie avec un prompt pré-rempli à un LLM gratuit, qui renvoie un **JSON** au
   format strict.
3. Je valide le fichier avec l'outil Python, je le place dans `modules/`, je pousse sur
   GitHub ; le module apparaît dans l'app.
4. Les enfants s'entraînent et passent des évaluations ; l'app enregistre les réponses et
   montre progression et marge de progression par compétence.

## Contraintes techniques

- Mobile-first (téléphone/tablette), accessibilité de base (contrastes, grandes zones
  tactiles, `prefers-reduced-motion`). Pas de PWA.
- Aucun compte, aucun suivi, aucune donnée envoyée à un tiers. Les photos ne transitent
  jamais par l'app.
- Sécurité : le contenu d'un module est une donnée non fiable. **Jamais de HTML ni de JS
  issu du JSON injecté dans la page** ; échapper tout le texte. Mise en forme autorisée :
  `**gras**`, retours à la ligne, symboles unicode (× ÷ − ² √ ≤ ≥). Pas de `innerHTML` avec
  du contenu de module.

## Le format de module (cœur du projet)

Un module = un fichier JSON, `schema_version: 1`. **Source de vérité unique** :
`schema/module.schema.json` (JSON Schema). Le validateur Python, le prompt pour le LLM et
les tests en découlent.

```json
{
  "schema_version": 1,
  "id": "maths-6e-division-euclidienne",
  "version": 1,
  "title": "Division euclidienne",
  "subject": "maths",
  "level": "CM2",
  "description": "…",
  "skills": [
    { "id": "calcul", "label": "Poser la division" },
    { "id": "probleme", "label": "Résoudre un problème" }
  ],
  "lesson": [
    { "type": "text", "skill": "calcul", "title": "…", "body": "…" },
    { "type": "worked_example", "skill": "calcul", "title": "…",
      "steps": [ { "thought": "Je cherche le plus grand multiple de 8 ≤ 347…",
                   "why": "…" } ] },
    { "type": "guided_steps", "skill": "calcul", "title": "…", "intro": "…",
      "steps": [ { "prompt": "10 × 19 = ?", "answer": 190, "hint": "…" } ] }
  ],
  "questions": [
    { "id": "q001", "skill": "calcul", "difficulty": 1, "type": "number",
      "prompt": "Effectue la division euclidienne de 347 par 8.",
      "fields": [ { "key": "q", "label": "quotient", "answer": 43 },
                  { "key": "r", "label": "reste", "answer": 3 } ],
      "hint": "…", "explanation": "347 = 8 × 43 + 3 …" },
    { "id": "q002", "skill": "probleme", "difficulty": 2, "type": "choice",
      "prompt": "…", "choices": [ { "id": "a", "label": "…" }, { "id": "b", "label": "…" } ],
      "answer": "b", "hint": "…", "explanation": "…" },
    { "id": "q003", "skill": "…", "difficulty": 1, "type": "text",
      "prompt": "…", "accepted": ["réponse 1", "variante 2"], "hint": "…", "explanation": "…" }
  ],
  "source_note": "Ce que le LLM a lu dans les photos / ce qui était illisible (facultatif)"
}
```

Règles de conception :
- **Leçon « Apprendre » obligatoire** : pour chaque compétence / type d'exercice, le
  **cheminement de pensée pas à pas** (exemple résolu commenté avec le « pourquoi » de chaque
  étape, puis mini-étapes guidées où l'enfant complète, comme l'histoire de Nolan dans la
  référence). Lien « Revoir la méthode » depuis une question d'entraînement.
- Types de questions v1 : `number` (un ou plusieurs champs), `choice` (QCM), `text` (réponse
  courte, comparaison tolérante : casse, accents, espaces). Un type = un petit fichier,
  registre simple, pour en ajouter facilement.
- **Banque statique de 100 à 200 questions par module**, réparties par compétence et par
  difficulté (1 à 4). Pas de générateurs aléatoires en v1. Un LLM gratuit perdant en qualité
  au-delà de ~60 questions par réponse, le module se construit en **lots de 40 à 60
  questions**, fusionnés par l'outil Python (voir plus bas).
- Chaque question a un `hint` (entraînement uniquement) et une `explanation` (correction).
- `id` de module, de compétence et de question **stables** : réimporter une version
  corrigée ne doit pas effacer l'historique d'un enfant.
- **Signalement d'erreur** : un bouton « Cette question me semble fausse » (enfant ou
  parent) enregistre le signalement localement, retire la question des tirages suivants, et
  les signalements sont inclus dans l'export de sauvegarde (le LLM peut se tromper, la
  qualité des corrections est un risque réel).

## Outils Python (`tools/`)

1. `validate.py <module.json> [--llm]` : valide contre le schéma **et** les règles
   sémantiques (ids uniques, compétences référencées existantes, au moins une bonne
   réponse, QCM cohérents, bonne réponse présente dans les choix, difficultés 1 à 4,
   répartition par compétence). Messages en français avec le chemin de l'erreur. Avec
   `--llm`, produit un texte à recopier au LLM : « Ton JSON a ces erreurs : … corrige-le et
   renvoie le JSON complet ». Doit aussi extraire le JSON si le LLM l'a entouré de texte ou
   de balises ```json.
2. `merge.py <module.json> <lot.json>` : ajoute les nouvelles questions, met à jour celles
   dont l'`id` existe, signale les énoncés quasi identiques (doublons), puis relance la
   validation.
3. `prompt.py [--mode nouveau|lot]` : génère depuis le schéma le **prompt à coller dans le
   LLM** (voir ci-dessous) et copie dans le presse-papiers ou écrit dans `docs/`.
4. `analyse.py <export.json>` : charge l'export de progression dans **pandas**, calcule par
   enfant et par compétence : taux de réussite, évolution dans le temps, temps moyen,
   questions les plus ratées, compétences en baisse ; graphiques matplotlib sauvegardés en
   PNG. Code simple et commenté : c'est mon terrain, je le ferai évoluer moi-même.
5. Côté app, une validation **minimale et défensive** suffit (structure requise, types) avec
   un message d'erreur clair ; la validation complète de référence est dans `validate.py`.
   Dis-moi explicitement où les deux se recouvrent, pour que je maîtrise le risque de
   divergence.

## Prompt de génération pour le LLM gratuit

Généré automatiquement depuis le schéma (`prompt.py`), jamais écrit à la main. Il doit :
expliquer la tâche (analyser photos de cours, exercices, contrôles), imposer de **ne
renvoyer que du JSON valide** conforme au schéma (inclus), fixer les règles pédagogiques
(vocabulaire du niveau, indices qui guident sans donner la réponse, explications courtes,
difficulté progressive, ne jamais inventer un contenu absent des photos, signaler dans
`source_note` ce qui est illisible), imposer de **vérifier chaque calcul** avant de
répondre, et inclure un exemple court. Deux modes : (1) « nouveau module » = métadonnées +
compétences + leçon pas à pas + premier lot de 40 à 60 questions ; (2) « lot suivant » =
40 à 60 questions supplémentaires, sans leçon, avec la liste des compétences et des
énoncés déjà présents pour éviter les répétitions.

## Fonctionnalités de l'app v1

1. **Profils** (2 enfants, prénom, sans mot de passe, changement rapide).
2. **Bibliothèque** : liste des modules lus depuis `modules/index.json`.
3. Par module : **Apprendre**, **S'entraîner** (indices, niveau qui monte après une série de
   réussites, comme dans la référence), **Évaluation** (N questions réparties par
   compétence, sans aide, note finale + corrections).
4. **Enregistrement de chaque tentative** (événement compact : date, enfant, module,
   question, compétence, difficulté, mode, juste/faux, durée, réponse). Pas de compteurs
   agrégés : tout se recalcule depuis les événements.
5. **Bilan** par enfant : réussite par compétence, évolution des dernières évaluations,
   compétences à travailler (faibles ou en baisse), bouton « Travailler ce point ». Vue claire
   pour le parent, simple pour l'enfant.
6. **Sauvegarde** : export / import de toutes les données en un JSON (format lisible par
   `analyse.py`).
7. **Aperçu d'un module** : charger un fichier JSON local pour le tester **en mémoire
   seulement** avant de le committer (non persistant).

## Méthode de travail

- Commence en **mode plan**. Avant tout code : (a) pose-moi tes questions, (b) propose
  l'arborescence, le schéma JSON, le découpage en étapes, et **un court registre de risques**
  (`docs/risques.md` : perte de données locales, JSON invalide du LLM, réponse fausse dans
  une question, dépassement de quota de stockage, dérive entre validateur app et Python) avec
  la parade prévue pour chacun. J'attends ma validation.
- Rédige les besoins sous forme de **user stories avec critères d'acceptation**
  (`docs/besoins.md`), et fournis pour chaque étape une **checklist de recette**
  (`docs/recette.md`) : scénarios que je teste moi-même à la main, résultat attendu.
- **Une étape par session**, petite et vérifiable. Étapes suggérées : 1) schéma + `validate.py`
  + module d'exemple converti depuis la référence (~30 questions) ; 2) squelette app,
  profils, chargement des modules ; 3) Apprendre ; 4) S'entraîner ; 5) Évaluation ;
  6) enregistrement, Bilan, signalement d'erreur ; 7) export/import, `merge.py`, `prompt.py`,
  `analyse.py` ; 8) déploiement GitHub Pages (je m'en occupe, donne-moi juste la
  configuration attendue).
- À la fin de chaque étape : ce qui marche, comment le tester, commit Git clair.
- Tests automatiques minimaux : `python tools/validate.py` sur les modules d'exemple, plus
  les cas d'erreur du validateur. Pas d'infrastructure lourde.
- Maintiens un `CLAUDE.md` court (< 60 lignes : objectif, contraintes, arborescence,
  commandes, conventions) et un `README.md` pour moi (ajouter un module, sauvegarder,
  analyser la progression).
- Code simple plutôt qu'astucieux : petits fichiers, noms explicites, pas d'abstraction
  prématurée. Ne relis pas inutilement les gros fichiers, ne modifie pas ce qui n'est pas
  demandé, et préviens-moi si une demande ajoute de la complexité de maintenance.

=== FIN ===
