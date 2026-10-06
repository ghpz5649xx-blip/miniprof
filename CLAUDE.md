# miniprof

App web d'entraînement et d'évaluation pour 2 enfants (CE2/CM1 et 6e/5e), en français.
Le parent (à l'aise en Python, peu en JS) doit pouvoir **lire** le code (pas forcément le
corriger) : c'est aussi ce qui permet à la session Claude suivante de reprendre.

## Gouvernance (décidée par le sponsor le 6 octobre 2026)
- **Deux acteurs.** **Claude** : chef de projet, architecte fonctionnel, développeur, PMO,
  testeur, responsable de production, support. **Le parent** : sponsor et client ; profil chef
  de projet / BA. Claude le tutoie et l'appelle par son prénom dans la conversation ; dans le
  dépôt (public), il est « le sponsor », sans nom (décision D4 du comité n° 1 en attente).
- **Comité de pilotage** : une session que le sponsor ouvre (message « comité »). Support :
  `pilotage.md` à la racine, que **Claude met à jour à la fin de chaque session** pour la
  suivante, et que le sponsor lit avant. Claude déroule l'ordre du jour et **tient le temps**
  (30 minutes, un temps par point ; à l'échéance : trancher, reporter ou prolonger).
- **Toute session se conclut** par les décisions du sponsor et les actions (porteur,
  échéance), écrites dans `pilotage.md` (relevé des décisions, tableau des actions), puis
  commit et push.
- **Pour chaque décision à prendre**, le support donne le contexte, les options avec leur coût
  et ce qu'on perd, et la recommandation de Claude. Le sponsor tranche ; Claude ne tranche pas à
  sa place.
- Entre deux comités, voir « Façon de travailler » (service courant d'un côté, évolutions de
  l'autre ; proposition D3 du comité n° 1).

## Contraintes (non négociables)
- 100 % statique (GitHub Pages) : HTML + CSS + JS vanilla en modules ES. Pas de framework,
  pas de build, pas de npm, pas de serveur, pas de PWA, polices système.
- **Asynchrone limité à la lecture de fichiers** (site : `readJson()`, appareil :
  `readJsonFile()`), dans `js/loader.js` ; appelants en `.then/.catch` + garde d'adresse.
  Stockage, calculs, affichage synchrones. Pas de worker, service worker, IndexedDB.
- **Sécurité** : le contenu d'un module n'est pas fiable. Jamais d'`innerHTML` avec du texte
  de module ; tout passe par `richText()` / `textContent`. Mise en forme : `**gras**`, `\n`.
- **Modules HTML** (`modules/<id>.html`) : exception assumée, du JS généré par un LLM tourne sur
  le site. Il est accepté seulement s'il respecte le contrat de `docs/module-html.md` (CSP sans
  réseau, aucun accès direct au stockage, écriture par `js/suivi.js`), vérifié par
  `tools/check_html.py`. Ces pages sont jetables : on les régénère au lieu de les corriger.
- Aucune requête vers un tiers, aucun compte, aucun suivi.
- Données lourdes en fichiers (`modules/*.json`, `modules/*.html`), progression légère en `localStorage`
  (événements compacts, tout est recalculé, pas de compteurs stockés).
- **Données des enfants** : ne jamais casser la progression enregistrée (`miniprof.v1.*`). Tout
  changement de format = nouvelle clé ou migration, avec un test. Un push arrive directement sur
  les appareils des enfants.
- **Vie privée** : le dépôt est public (GitHub Pages gratuit). Jamais de photos, de prénoms réels
  ni d'exports dans le dépôt (voir `.gitignore`) ; les photos d'une leçon restent dans la conversation.
- JS simple et plat, commentaires en français qui expliquent le **pourquoi** (lisible par le
  parent et par la session suivante).

## Arborescence
- `pilotage.md` : support des comités de pilotage (état, décisions, actions) ; seul doc que lit
  le sponsor.
- `schema/module.schema.json` : **source de vérité** du format de module.
- `modules/` : un fichier par module, JSON (joué par l'app) ou HTML (page autonome, contrat
  `docs/module-html.md`) ; `index.json` généré par `tools/build_index.py` (`"kind": "json" | "html"`) ;
  `brouillons.json` : modules publiés mais pas encore relus par le parent (cachés aux enfants,
  `"brouillon": true` dans l'index).
- `tools/` : outils Python (validate, check_html, tirage, merge, prompt, analyse, build_index,
  recette_navigateur) ; `common.py` partagé ; `recette/` : page de recette automatique.
- `tools/tests/` : unittest + `fixtures/` (`fixtures/html/` : module HTML minimal).
- `index.html`, `css/style.css`, `js/` : l'app. `js/app.js` (routage par hash), `ui.js`
  (`el()`, `richText()`), `storage.js` (localStorage protégé), `profiles.js`, `loader.js`,
  `check-module.js`, `open-module.js` (chargement + contrôle d'un module pour un écran),
  `answers.js` (comparaison tolérante des réponses), `question-view.js` (affichage et correction
  d'une question, partagé entraînement / évaluation, bouton « signaler »), `events.js` (journal
  des tentatives par profil, format compact), `flags.js` (questions signalées), `stats.js`
  (calculs du bilan), `backup.js` (export, restauration, rappel), `screens/` (un fichier par écran : `profiles`, `library`, `module-home`,
  `lesson`, `practice-setup`, `practice`, `exam-setup` (réglage + composition de l'évaluation),
  `exam`, `exam-result`, `report` (bilan), `backup` (sauvegarde)). `suivi.js` : chargé par les
  modules HTML, expose `window.miniprof` et écrit leurs réponses par `addEvents()`.
  Aperçu d'un module local : id réservé `_apercu` (`open-module.js`), rien n'est enregistré.
- `docs/` (carte et usage : `README.md`, « Les docs ») : `plan-modules-html.md` (plan en cours),
  `recette.md` (en tête : ce qui reste à vérifier par le parent), `parent-iphone.md` (créer un
  module depuis l'iPhone), `module-html.md` (contrat des modules HTML), `gabarit-module.html`
  (moteur commun à copier), `risques.md` ; références figées de l'app v1 : `besoins.md`, `ux.md`.
  `prompt-nouveau.md` et `prompt-lot-*.md` sont générés par `prompt.py` et non versionnés.
- `.claude/skills/nouveau-module/SKILL.md` : skill `/nouveau-module` (photos → module HTML publié).
- `.claude/settings.json` + `.claude/hooks/synchro.sh` : au démarrage de chaque session,
  `git pull --ff-only` sur `main` ; affiche un avertissement en cas d'échec, sans rien forcer.
- `reference/` : prototype d'origine, **ne plus le relire** (résumé dans `docs/ux.md`).
  `circuit_electrique.html` : page d'origine du module circuit, gardée pour comparaison.

## Commandes
```bash
source .venv/bin/activate                     # venv local (pip install -r tools/requirements.txt)
python tools/validate.py modules/<id>.json    # --llm : texte pour le LLM ; --nettoyer
python tools/check_html.py modules/<id>.html  # contrat d'un module HTML ; --llm : texte pour le LLM
python tools/tirage.py modules/<id>.html      # tire des milliers de questions (node), cherche les ambiguïtés
python tools/build_index.py                   # régénère modules/index.json (modules valides)
python tools/prompt.py --mode nouveau          # ou --mode lot <module> ; merge.py <module> <lot> ; analyse.py <export>
python -m unittest discover tools/tests -v    # tests
python tools/recette_navigateur.py            # recette auto dans Chrome/Chromium sans fenêtre (CHROME=…)
python3 -m http.server 8000                   # tester l'app (file:// ne marche pas)
```
Site publié (GitHub Pages, branche `main`, racine) : https://ghpz5649xx-blip.github.io/miniprof/
— un push publie en une minute environ.

## Règles à garder synchronisées
- `normalize_text()` (`tools/common.py`) ≡ `normalizeText()` (`js/answers.js`) : cas partagés
  dans `tools/tests/fixtures/normalisation.json` (Python : `test_normalisation.py` ; JS : recette 3.15).
- Champs obligatoires du schéma ≡ `REQUIRED`, `REQUIRED_QUESTION`, `TYPES_CONNUS`, `BLOCS_CONNUS` de
  `js/check-module.js` (test automatique `test_sync.py`, qui interdit aussi `innerHTML`).
- La validation complète est dans `validate.py` ; l'app ne fait qu'un contrôle défensif.
- Le skill `/nouveau-module` lance `check_html.py`, `build_index.py` et les tests, et ne cite que
  des fichiers qui existent (`test_sync.py`) : le mettre à jour si une commande change.
- `js/suivi.js` n'écrit que par `addEvents()` de `js/events.js` (`test_sync.py`). La fiche d'un
  module HTML reprend `subject` et `level` du schéma (`check_html.py` les lit dans le schéma).
- `tools/analyse.py` ≡ app : `COLONNES` ≡ ordre des cases de `js/events.js`, `est_en_baisse()` ≡ `js/stats.js`.

## Conventions
- Ids stables (module, compétence, question) : ne jamais renuméroter.
- Fichier de module nommé `<id>.json` ou `<id>.html`.
- Petits fichiers, noms explicites, pas d'abstraction prématurée.

## Façon de travailler
- **Challenger chaque demande d'évolution avant de la découper** : reformuler le besoin (quel
  problème, pour quel enfant), dire si l'existant le couvre déjà ou si plus léger suffit (module
  HTML, doc, simple réglage), annoncer le coût (fichiers et règles à synchroniser, recette iPhone)
  et les risques (données des enfants, contraintes). Une seule fois, en quelques lignes ; le
  parent tranche. Ne s'applique pas à la création de modules (`/nouveau-module`).
- **Rester synchronisé avec `origin/main`** (le parent travaille depuis l'iPhone et le Mac,
  plusieurs sessions peuvent pousser en parallèle) : mise à jour en début de session par le hook
  `synchro.sh` (si son message signale un échec, prévenir le parent), puis
  `git pull --rebase origin main` juste avant chaque push et relancer les tests. En cas de
  conflit, s'arrêter et demander au parent.
- On n'attaque une évolution que sur **décision du sponsor, inscrite dans `pilotage.md`**.
  Une idée nouvelle (la sienne ou celle de Claude) va à l'ordre du jour du comité suivant, au
  lieu d'être réalisée dans la conversation où elle naît. Le **service courant** n'attend pas un
  comité : `/nouveau-module`, correction d'un module, réponse à une question, `git revert` en
  cas d'incident. Une évolution décidée est découpée en **unités vérifiables** ; plusieurs
  unités peuvent tenir dans une session.
- Une unité est **finie** quand :
  1. `python -m unittest discover tools/tests -v` passe ;
  2. les contrôles concernés passent (`validate.py`, `check_html.py`, `build_index.py`) et
     `modules/index.json` est régénéré ;
  3. la recette est faite dans le navigateur : `tools/recette_navigateur.py` (à compléter quand
     une évolution le permet), plus ce qui demande de regarder l'écran ; elle est écrite dans
     `docs/recette.md` ;
  4. les docs touchées sont à jour (arborescence, « Règles à garder synchronisées », plan),
     ainsi que `pilotage.md` (faits marquants, actions, décisions) ;
  5. commit clair, puis **push**.
- **S'arrêter et demander au parent**, sans pousser : changement d'une contrainte non négociable,
  choix pédagogique ou d'UX visible par les enfants, changement du format de stockage, recette
  qui doit se faire sur l'iPhone, ou point qui demande son jugement (contenu d'un module).
- Si un problème apparaît après un push : `git revert` et push tout de suite, puis analyse.
- Toute décision non évidente est écrite avec son **pourquoi** dans le doc concerné (plan,
  `risques.md`, commentaire), pas seulement dans le message de commit.
- Signaler au parent ce qui ajoute du travail manuel de son côté ou un risque pour les données
  des enfants.
- **Docs sobres** : le sponsor suit le projet par `pilotage.md` seulement (état, décisions,
  actions, ce qu'il doit vérifier) ; les autres docs sont des annexes. Pas de nouveau fichier
  dans `docs/` sans son accord : compléter un doc existant. Un plan fini ou abandonné est retiré (l'historique Git le
  garde) une fois son « pourquoi » reporté dans le plan suivant ou `risques.md`.

## Prochaines étapes
- État, décisions et actions : `pilotage.md`. Prochain rendez-vous : comité n° 1 (gouvernance,
  suite de l'étape 12 : décision D5). Ne pas avancer l'étape 12 avant cette décision.
- Créer un module : le parent passe par `/nouveau-module` depuis l'iPhone
  (`docs/parent-iphone.md`) ; les sessions dans le cloud suivent le même `CLAUDE.md`.
