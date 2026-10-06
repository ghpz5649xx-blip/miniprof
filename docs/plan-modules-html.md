# miniprof : des modules HTML générés par le LLM, miniprof en « carnet de suivi »

> **Le plan en cours.** État : étapes 8, 9, 10 faites ; gabarit + `tirage.py` faits ;
> **étape 12 en cours** (unité 1 « brouillon » faite, unités 2 à 4 à faire). Résumé dans le
> `README.md`, « Où en est le projet ».

## Contexte
Ce matin, une page HTML autonome (`reference/circuit_electrique.html`, 73 Ko) produite par Claude
à partir de 4 photos a suffi pour faire réviser une leçon, envoyée par SMS depuis le travail. Ce
fichier est un **programme** : un solveur de circuit (`solve()`), des schémas SVG calculés
(`drawCircuit`), des générateurs de questions aléatoires (`genSerie`, `genCourt`…) et un labo
interactif. Le format JSON de miniprof (questions fixes) ne pourra jamais exprimer cela. L'ancien plan
`docs/plan-iphone.md` (étapes 8 à 11, 400 à 500 lignes de JS dont un validateur en double) donnerait
un résultat **moins bon** que le pipeline de ce matin. (Ce plan, abandonné, a été retiré le
2026-10-06 ; il reste lisible dans l'historique Git.)

Ce que miniprof apporte et que la page seule n'a pas : le **suivi dans la durée**, par enfant et sur
plusieurs modules (`js/events.js`, `js/stats.js`, `screens/report.js`, sauvegarde, `tools/analyse.py`).

**Nouvelle direction (décidée)** :
- Le LLM produit des modules **HTML autonomes**, comme ce matin.
- miniprof devient le carnet de suivi : chaque page HTML charge un petit contrat `js/suivi.js` qui
  écrit les réponses dans le journal d'événements existant. Ça marche parce que les pages sont
  servies par le **même site** GitHub Pages et partagent donc le même localStorage.
- **Publication depuis le téléphone avec Claude Code** (app iOS ou claude.ai/code) ouvert sur le
  dépôt : photos → `modules/<id>.html` → contrôle Python → commit → GitHub Pages → URL par SMS.
- **Coexistence** : les modules JSON et tout leur moteur continuent de fonctionner. On ne supprime
  rien.
- **Sécurité** : on accepte le JS généré sur le même site, avec des garde-fous automatiques.

Ce qui est abandonné : les étapes 8 à 11 de l'ancien `docs/plan-iphone.md` (modules de 30 questions,
copier-coller du JSON, validateur JS, test de 5 questions dans l'app).

## Le contrat (ce qu'une page HTML doit respecter)
1. **Fiche du module** dans la page, lue par `build_index.py` :
   `<script type="application/json" id="miniprof-module">{ "id", "title", "subject", "level",
   "description", "skills": [{ "id", "label" }] }</script>`. Mêmes champs que l'index actuel.
   Le fichier s'appelle `<id>.html`.
2. **Script de suivi** : `<script type="module" src="../js/suivi.js"></script>`. Il expose
   `window.miniprof` (la page générée reste un script classique, plus simple à écrire pour le
   LLM ; elle n'appelle `miniprof` qu'au moment d'une réponse, quand le module est chargé) :
   - `miniprof.profil()` : prénom du profil courant, ou `null` ;
   - `miniprof.reponse({ competence, juste, mode: "e"|"v", difficulte, question, reponse, duree,
     evaluation })`, qui appelle `addEvents()` de `js/events.js` avec le format actuel (aucun
     changement de format, donc `analyse.py`, `stats.js` et la sauvegarde marchent tels quels) ;
     `question` = nom du générateur (ex. `serie`), puisque les questions sont tirées au hasard ;
   - `miniprof.debutEvaluation(niveau)` : renvoie l'identifiant `"<date>/<niveau>"` commun aux
     réponses d'une évaluation (même convention que `events.js`) ;
   - un bandeau ajouté en haut de page : « Tu es Léa · changer » (lien `../#/`), ou « Choisis ton
     profil pour que tes résultats soient gardés » s'il n'y a pas de profil. La page reste
     utilisable sans profil, mais rien n'est enregistré.
   - Si `miniprof` est absent (page ouverte ailleurs), la page doit fonctionner quand même : la
     page appelle `window.miniprof && miniprof.reponse(...)`.
3. **Interdits** (vérifiés par le contrôle Python) : `fetch`, `XMLHttpRequest`, `import(`, toute
   URL `http(s)://` (Google Fonts compris : polices système), `localStorage`/`sessionStorage`
   (seul `suivi.js` y touche), `<iframe>`, `<link rel="stylesheet" href=…>` externe.

## Étapes (recette dans `docs/recette.md`) ; 8 et 9 ensemble, 10 à part

### Étape 8 : le contrat de suivi ✔ (fait le 2026-10-05)
- Nouveau `js/suivi.js` (environ 60 à 80 lignes) : réutilise `currentProfile()` (`js/profiles.js`),
  `addEvents()` / `maintenant()` (`js/events.js`), `el()` (`js/ui.js`) pour le bandeau.
- `tools/build_index.py` : parcourt aussi `modules/*.html`, extrait la fiche (regex sur
  `id="miniprof-module"` + `json.loads`), applique le contrôle, ajoute l'entrée avec
  `"kind": "html"`, `"file": "<id>.html"` (les entrées JSON reçoivent `"kind": "json"`).
- Nouveau `tools/check_html.py` (avec `common.py`) : fiche présente et complète, nom du fichier
  = id, ids de compétences uniques, `suivi.js` chargé, liste des interdits. Sortie lisible par le
  LLM (comme `validate.py --llm`), pour que Claude Code corrige lui-même.
- `js/screens/library.js` : une carte `kind: "html"` pointe vers `modules/<file>` au lieu de
  `#/module/<id>`.
- `js/screens/report.js` : pour un module HTML, « Retour » et « Travailler ce point » mènent à la
  page HTML (pas d'écran d'entraînement par niveau).
- Tests : `tools/tests/test_check_html.py` + fixtures (`fixtures/html/` : une page valide, une
  page par interdit) ; `test_build_index` couvre une page HTML ; `test_sync.py` vérifie que
  `suivi.js` respecte l'ordre des cases (il passe par `addEvents`, donc rien à recopier).
- `CLAUDE.md` : nouvelle contrainte « modules HTML : JS généré accepté, contrôlé par
  `check_html.py` », arborescence, commandes.

### Étape 9 : premier module HTML (le circuit électrique) ✔ (fait le 2026-10-05)
Réalisé : `modules/sciences-6e-circuit-electrique.html` (niveau 6e, choisi par le parent).
Ajouts en cours de route : une **CSP obligatoire** dans chaque page (`connect-src 'none'`, vérifiée
par `check_html.py`), parce qu'une recherche de texte ne suffit pas à bloquer le réseau ; et
`tools/recette_navigateur.py`, une recette automatique dans Chrome sans fenêtre.
- Adapter `reference/circuit_electrique.html` → `modules/sciences-6e-circuit-electrique.html` : ajouter la fiche et `suivi.js`, remplacer `store`/`record()` par
  `miniprof.reponse(...)`, retirer Google Fonts et l'accès direct à `localStorage`. Son écran
  « Bilan » renvoie vers `../#/module/<id>/bilan`. On garde le reste tel quel.
- `python tools/check_html.py modules/…html`, puis `build_index.py`.
- Recette : profil Léa, quelques réponses en entraînement et une évaluation dans la page, puis le
  bilan miniprof les montre (par compétence, dernières évaluations) ; export, puis
  `analyse.py` les lit.

### Étape 10 : le pipeline Claude Code depuis le téléphone ✔ (fait le 2026-10-06)
Réalisé : skill `.claude/skills/nouveau-module/SKILL.md` (photos → `modules/<id>.html` →
contrôles → commit → push → URL), `docs/module-html.md` complété (règles pédagogiques validées
par le parent, pièges vus sur le circuit), `docs/parent-iphone.md`, risque R11 (photos), test
`test_skill_nouveau_module` (`test_sync.py`). Premier module fait depuis l'iPhone :
`anglais-6e-zootopia-animaux`.
Constats et décisions :
- Le skill vérifie la syntaxe du JS par `node --check` : une erreur de syntaxe donne une page
  blanche sur l'iPhone et `check_html.py` ne la voit pas.
- Dans l'app iOS, `/nouveau-module` n'est pas proposé au premier message (le dépôt n'est pas
  encore copié dans la session) : on tape la commande en entier, elle marche.
- La session partie de `main` a poussé **directement sur `main`**, contrairement à la
  documentation de Claude Code (une branche par session). Le skill gère les deux cas.
- Session dans le cloud : `test_json_casse` dépendait de la version de Python (rendu
  indépendant) ; `recette_navigateur.py` n'y renvoyait rien (Chromium en root sans
  `--no-sandbox`) : le script cherche maintenant Chromium sur Linux et dit pourquoi le navigateur
  s'est arrêté. Cette recette teste l'app, pas le nouveau module : en local, elle reste
  obligatoire seulement quand le code de l'app change.
- Dépôt gardé public (GitHub Pages gratuit) : voir R11.
Recette 10.3 à 10.8 faite le 6 octobre 2026 (`docs/recette.md`).

### Étape 12 : validation des modules par le parent (brouillon + fiche de contrôle)
Demande du parent (6 octobre 2026) : un profil PARENT ouvert par l'énigme du Sphinx, la liste des
modules pas encore validés, et pour chacun les objectifs et quelques exercices avec leurs
réponses en face, pour valider vite. Après analyse, le parent a retenu :
- **Une fiche de contrôle produite par le vrai code** : c'est le cœur de la valeur, et la seule
  parade en amont à R3 (réponse fausse du LLM). Pour un module HTML, les questions viennent de
  générateurs JS : la fiche tire des questions avec ces générateurs (mode `#controle` de la page),
  au lieu d'un résumé écrit à part, qui pourrait être juste alors que le générateur est faux.
  Pour un module JSON : toutes les questions avec leurs réponses (écran `#/controle/<id>`).
- **Un statut brouillon** (`modules/brouillons.json`) : avant, un module poussé apparaissait
  tout de suite dans la bibliothèque des enfants, avant la relecture. Un brouillon est caché
  dans la bibliothèque, mais son URL marche et il reste dans le bilan. Pourquoi un fichier à part
  plutôt qu'un champ du module : le schéma refuse les champs inconnus, et un seul fichier marche
  pour les deux sortes de modules.
- **Valider = demander à Claude Code** (`/nouveau-module valide <id>`), qui retire l'id et pousse.
  Un bouton dans l'app ne peut rien changer chez les enfants : il n'y a pas de serveur.
- **Pas d'énigme ni de profil PARENT** : le site est statique et le dépôt public, donc la réponse
  serait lisible dans le JS (et les enfants la connaissent). Un profil n'existe que sur un
  appareil : un rôle parent ne protégerait rien et obligerait à migrer `miniprof.v1.profiles`.
  L'écran `#/parents` est caché, pas protégé, comme l'aperçu d'un module.
Unités : 1. brouillon (`build_index.py`, bibliothèque) ; 2. écran `#/parents` et fiche de
contrôle JSON ; 3. mode `#controle` des modules HTML (contrat, `check_html.py`, recette) ;
4. skill `/nouveau-module` et `docs/parent-iphone.md`. Recette : `docs/recette.md`, étape 12.

## Limites acceptées (écrites dans `docs/risques.md`, R3 et R10)
- Les pages HTML ne sont pas lisibles par le mainteneur : elles sont **jetables** (on les
  régénère au lieu de les corriger). Le code à maintenir reste petit et lisible : `suivi.js`,
  `check_html.py`, une vingtaine de lignes dans `library` et `report`.
- Pas de bouton « signaler » dans les pages HTML (questions générées). On le remplace par une
  demande de correction à Claude Code.
- Les compétences d'un module HTML sont libres : le bilan regroupe par module, pas entre modules.

## Vérification
- `python -m unittest discover tools/tests -v` (check_html, build_index, sync).
- `python tools/check_html.py modules/*.html` : 0 erreur ; une fixture par interdit est refusée.
- `python3 -m http.server 8000` : bibliothèque → circuit (page HTML) → réponses → `#/bilan`
  montre les compétences du circuit à côté des modules JSON ; les modules JSON marchent toujours.
- Sur l'iPhone (GitHub Pages) : de bout en bout, avec une vraie leçon envoyée depuis Claude Code
  mobile, jusqu'à l'URL envoyée par SMS et au bilan rempli (recette 10.3 à 10.8).
