# miniprof

App web d'entraînement et d'évaluation pour 2 enfants (CE2/CM1 et 6e/5e), en français.
Un seul mainteneur, à l'aise en Python, **faible en JS** : il doit pouvoir lire et corriger le code.

## Contraintes (non négociables)
- 100 % statique (GitHub Pages) : HTML + CSS + JS vanilla en modules ES. Pas de framework,
  pas de build, pas de npm, pas de serveur, pas de PWA, polices système.
- **Pas d'asynchrone** sauf `readJson()` dans `js/loader.js` (seule fonction async).
  Pas de worker, service worker, IndexedDB.
- **Sécurité** : le contenu d'un module n'est pas fiable. Jamais d'`innerHTML` avec du texte
  de module ; tout passe par `richText()` / `textContent`. Mise en forme : `**gras**`, `\n`.
- Aucune requête vers un tiers, aucun compte, aucun suivi.
- Données lourdes en fichiers (`modules/*.json`), progression légère en `localStorage`
  (événements compacts, tout est recalculé, pas de compteurs stockés).
- JS simple et plat, commentaires en français qui expliquent le **pourquoi**.

## Arborescence
- `schema/module.schema.json` : **source de vérité** du format de module.
- `modules/` : un fichier JSON par module ; `index.json` généré par `tools/build_index.py`.
- `tools/` : outils Python (validate, merge, prompt, analyse, build_index) ; `common.py` partagé.
- `tools/tests/` : unittest + `fixtures/`.
- `index.html`, `css/style.css`, `js/` : l'app. `js/app.js` (routage par hash), `ui.js`
  (`el()`, `richText()`), `storage.js` (localStorage protégé), `profiles.js`, `loader.js`,
  `check-module.js`, `open-module.js` (chargement + contrôle d'un module pour un écran),
  `answers.js` (comparaison tolérante des réponses), `question-view.js` (affichage et correction
  d'une question, partagé entraînement / évaluation), `screens/` (un fichier par écran :
  `profiles`, `library`, `module-home`, `lesson`, `practice-setup`, `practice`, `exam-setup`
  (réglage + composition de l'évaluation), `exam`, `exam-result`).
- `docs/` : `ux.md` (référence UX), `besoins.md`, `recette.md`, `risques.md`.
- `reference/` : prototype d'origine, **ne plus le relire** (résumé dans `docs/ux.md`).

## Commandes
```bash
source .venv/bin/activate                     # venv local (pip install -r tools/requirements.txt)
python tools/validate.py modules/<id>.json    # --llm : texte pour le LLM ; --nettoyer
python tools/build_index.py                   # régénère modules/index.json (modules valides)
python -m unittest discover tools/tests -v    # tests
python3 -m http.server 8000                   # tester l'app (file:// ne marche pas)
```

## Règles à garder synchronisées
- `normalize_text()` (`tools/common.py`) ≡ `normalizeText()` (`js/answers.js`) : cas partagés
  dans `tools/tests/fixtures/normalisation.json` (Python : `test_normalisation.py` ; JS : recette 3.15).
- Champs obligatoires du schéma ≡ `REQUIRED`, `REQUIRED_QUESTION`, `TYPES_CONNUS`, `BLOCS_CONNUS` de
  `js/check-module.js` (test automatique `test_sync.py`, qui interdit aussi `innerHTML`).
- La validation complète est dans `validate.py` ; l'app ne fait qu'un contrôle défensif.

## Conventions
- Ids stables (module, compétence, question) : ne jamais renuméroter.
- Fichier de module nommé `<id>.json`.
- Une étape par session, recette dans `docs/recette.md`, commit clair à la fin.
- Petits fichiers, noms explicites, pas d'abstraction prématurée. Signaler toute demande qui
  ajoute de la complexité de maintenance.
