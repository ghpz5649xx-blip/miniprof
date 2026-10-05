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
- Aucune requête vers un tiers, aucun compte, aucun suivi.
- Données lourdes en fichiers (`modules/*.json`), progression légère en `localStorage`
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
- `modules/` : un fichier JSON par module ; `index.json` généré par `tools/build_index.py`.
- `tools/` : outils Python (validate, merge, prompt, analyse, build_index) ; `common.py` partagé.
- `tools/tests/` : unittest + `fixtures/`.
- `index.html`, `css/style.css`, `js/` : l'app. `js/app.js` (routage par hash), `ui.js`
  (`el()`, `richText()`), `storage.js` (localStorage protégé), `profiles.js`, `loader.js`,
  `check-module.js`, `open-module.js` (chargement + contrôle d'un module pour un écran),
  `answers.js` (comparaison tolérante des réponses), `question-view.js` (affichage et correction
  d'une question, partagé entraînement / évaluation, bouton « signaler »), `events.js` (journal
  des tentatives par profil, format compact), `flags.js` (questions signalées), `stats.js`
  (calculs du bilan), `backup.js` (export, restauration, rappel), `screens/` (un fichier par écran : `profiles`, `library`, `module-home`,
  `lesson`, `practice-setup`, `practice`, `exam-setup` (réglage + composition de l'évaluation),
  `exam`, `exam-result`, `report` (bilan), `backup` (sauvegarde)).
  Aperçu d'un module local : id réservé `_apercu` (`open-module.js`), rien n'est enregistré.
- `docs/` : `prompt-nouveau.md` (généré par `prompt.py`), `ux.md` (référence UX), `besoins.md`, `recette.md`, `risques.md`,
  `plan-modules-html.md` (plan des étapes 8 à 10, pas encore réalisé), `plan-iphone.md` (abandonné).
- `reference/` : prototype d'origine, **ne plus le relire** (résumé dans `docs/ux.md`), sauf
  `circuit_electrique.html`, point de départ de l'étape 9.

## Commandes
```bash
source .venv/bin/activate                     # venv local (pip install -r tools/requirements.txt)
python tools/validate.py modules/<id>.json    # --llm : texte pour le LLM ; --nettoyer
python tools/build_index.py                   # régénère modules/index.json (modules valides)
python tools/prompt.py --mode nouveau          # ou --mode lot <module> ; merge.py <module> <lot> ; analyse.py <export>
python -m unittest discover tools/tests -v    # tests
python3 -m http.server 8000                   # tester l'app (file:// ne marche pas)
```

## Règles à garder synchronisées
- `normalize_text()` (`tools/common.py`) ≡ `normalizeText()` (`js/answers.js`) : cas partagés
  dans `tools/tests/fixtures/normalisation.json` (Python : `test_normalisation.py` ; JS : recette 3.15).
- Champs obligatoires du schéma ≡ `REQUIRED`, `REQUIRED_QUESTION`, `TYPES_CONNUS`, `BLOCS_CONNUS` de
  `js/check-module.js` (test automatique `test_sync.py`, qui interdit aussi `innerHTML`).
- La validation complète est dans `validate.py` ; l'app ne fait qu'un contrôle défensif.
- `tools/analyse.py` ≡ app : `COLONNES` ≡ ordre des cases de `js/events.js`, `est_en_baisse()` ≡ `js/stats.js`.

## Conventions
- Ids stables (module, compétence, question) : ne jamais renuméroter.
- Fichier de module nommé `<id>.json`.
- Petits fichiers, noms explicites, pas d'abstraction prématurée.

## Façon de travailler
- On n'attaque une évolution que sur demande du parent. Elle est découpée en **unités
  vérifiables** ; plusieurs unités peuvent tenir dans une session.
- Une unité est **finie** quand :
  1. `python -m unittest discover tools/tests -v` passe ;
  2. les contrôles concernés passent (`validate.py`, `build_index.py`, puis `check_html.py` après
     l'étape 8) et `modules/index.json` est régénéré ;
  3. la recette est faite dans le navigateur (`python3 -m http.server 8000`, outils Chrome quand
     ils sont disponibles), y compris un test de non-régression (profil, module JSON, bilan), et
     elle est écrite dans `docs/recette.md` ;
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
- Plan validé, **pas encore réalisé** : `docs/plan-modules-html.md` (modules HTML générés, miniprof
  en carnet de suivi ; le moteur JSON reste).
- Étapes 8 et 9 ensemble (le contrat ne se vérifie qu'avec le vrai module circuit) ; étape 10 à
  part (vérification sur l'iPhone du parent). Les changements de contraintes prévus (JS généré
  accepté dans `modules/*.html`, contrôlé par `tools/check_html.py`) s'ajoutent quand l'étape 8
  est faite.
- `docs/plan-iphone.md` : abandonné (gardé pour le pourquoi).
