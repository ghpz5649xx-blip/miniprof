# miniprof

App web d'entraînement et d'évaluation pour 2 enfants (CE2/CM1 et 6e/5e), en français.
Mainteneur : Claude Code. Le parent (à l'aise en Python, peu en JS) décide des besoins, de la
pédagogie et de l'UX, et fait la recette finale sur l'iPhone. Il doit pouvoir **lire** le code
(pas forcément le corriger) : c'est aussi ce qui permet à la session Claude suivante de reprendre.

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
- `schema/module.schema.json` : **source de vérité** du format de module.
- `modules/` : un fichier par module, JSON (joué par l'app) ou HTML (page autonome, contrat
  `docs/module-html.md`) ; `index.json` généré par `tools/build_index.py` (`"kind": "json" | "html"`).
- `tools/` : outils Python (validate, check_html, merge, prompt, analyse, build_index,
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
- `docs/` : `module-html.md` (contrat des modules HTML), `prompt-nouveau.md` (généré par
  `prompt.py`), `ux.md` (référence UX), `besoins.md`, `recette.md`, `risques.md`,
  `plan-modules-html.md` (étapes 8 à 10 faites), `plan-iphone.md` (abandonné),
  `parent-iphone.md` (créer un module depuis l'iPhone).
- `.claude/skills/nouveau-module/SKILL.md` : skill `/nouveau-module` (photos → module HTML publié).
- `reference/` : prototype d'origine, **ne plus le relire** (résumé dans `docs/ux.md`).
  `circuit_electrique.html` : page d'origine du module circuit, gardée pour comparaison.

## Commandes
```bash
source .venv/bin/activate                     # venv local (pip install -r tools/requirements.txt)
python tools/validate.py modules/<id>.json    # --llm : texte pour le LLM ; --nettoyer
python tools/check_html.py modules/<id>.html  # contrat d'un module HTML ; --llm : texte pour le LLM
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
- On n'attaque une évolution que sur demande du parent. Elle est découpée en **unités
  vérifiables** ; plusieurs unités peuvent tenir dans une session.
- Une unité est **finie** quand :
  1. `python -m unittest discover tools/tests -v` passe ;
  2. les contrôles concernés passent (`validate.py`, `check_html.py`, `build_index.py`) et
     `modules/index.json` est régénéré ;
  3. la recette est faite dans le navigateur : `tools/recette_navigateur.py` (à compléter quand
     une évolution le permet), plus ce qui demande de regarder l'écran ; elle est écrite dans
     `docs/recette.md` ;
  4. les docs touchées sont à jour (arborescence, « Règles à garder synchronisées », plan) ;
  5. commit clair, puis **push**.
- **S'arrêter et demander au parent**, sans pousser : changement d'une contrainte non négociable,
  choix pédagogique ou d'UX visible par les enfants, changement du format de stockage, recette
  qui doit se faire sur l'iPhone, ou point qui demande son jugement (contenu d'un module).
- Si un problème apparaît après un push : `git revert` et push tout de suite, puis analyse.
- Toute décision non évidente est écrite avec son **pourquoi** dans le doc concerné (plan,
  `risques.md`, commentaire), pas seulement dans le message de commit.
- Signaler au parent ce qui ajoute du travail manuel de son côté ou un risque pour les données
  des enfants.

## Prochaines étapes
- `docs/plan-modules-html.md` : étapes 8 à 10 faites. 10.6 et 10.8 faites avec l'enfant de 6e
  (iPhone 8, 6 octobre 2026). Reste la recette 10.7 (corriger un module depuis l'iPhone) et
  11.3 (création de profil sur l'iPhone). Aucune autre évolution demandée.
- Créer un module : le parent passe par `/nouveau-module` depuis l'iPhone
  (`docs/parent-iphone.md`) ; les sessions dans le cloud suivent le même `CLAUDE.md`.
- `docs/plan-iphone.md` : abandonné (gardé pour le pourquoi).
