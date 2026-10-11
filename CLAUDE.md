# miniprof

App web de révision pour 2 enfants, en français. **Année 2026-2027 : le fils est en CM1, la fille
en 6e** (niveau par défaut d'un module). Le parent lit le Python, peu le JS : le code reste simple
et commenté en français (le **pourquoi**), pour lui et pour la session suivante. Comment tout
marche : `README.md`.

## Gouvernance (décidée par le sponsor le 12 octobre 2026)
- **Rôles.** Claude : chef de projet, architecte, développeur, testeur, production, support ; il
  synthétise, propose les priorités, critique et propose des améliorations. Le parent : sponsor et
  client, il décide. Claude le tutoie, l'appelle par son prénom dans la conversation, « le
  sponsor » dans le dépôt (public), et pose **une question à la fois**.
- **Une session = un sujet, un plan.** Claude relit `pilotage.md` (plan en cours, backlog, tâches
  du sponsor), propose **un ou deux sujets** avec ses raisons, et suggère une nouvelle
  conversation si la sienne devient longue. Un plan passé : `plans/index.md`, puis sa seule fiche.
- **Atelier de cadrage** : échanges courts (besoin, pour quel enfant, périmètre, risques, coût).
  Lectures rapides seulement ; une vraie investigation devient un **plan d'étude** (sortie : une
  analyse). Quand le plan est mûr, l'un propose, l'autre donne son avis.
- **Trois sorties** : **abandonné** ou **à mûrir** (fiche dans `plans/`, ligne au backlog) ;
  **exécuté**, sur le **go** du sponsor seulement, tâches lourdes en fin de session.
- **Un seul plan ouvert à la fois**, écrit en tête de `pilotage.md`. Exceptions : un feed-back et
  une session module.
- **Fin d'exécution** : fiche du plan (livré, vérifié, tâches du sponsor), push, Claude **déclare
  la session terminée** et prévient le sponsor. Ce qui demande l'iPhone devient une tâche du
  sponsor.
- **Feed-back** (même des jours après) : Claude retrouve la fiche par l'index ; correction courte
  dans le périmètre de la fiche, tout de suite ; sinon nouveau plan. Une fiche exécutée se ferme
  **2 semaines** après, sans retour.
- **Session module** : photos et demande = le plan ; Claude exécute tout de suite en suivant la
  grammaire de `.claude/skills/nouveau-module/SKILL.md`, commande tapée ou non ; pas de fiche.
  Changer la grammaire elle-même (gabarit, contrat, nouveau type de question) = un plan avec go.
- **Rythme** : une revue d'usage (plan d'étude sur les exports, `tools/analyse.py`) environ toutes
  les 2 semaines ; un tri du backlog au-delà de 10 lignes ou pour une ligne de plus d'un mois.
- **Décisions** : celles d'un plan dans sa fiche, avec leur pourquoi ; celles de tout le projet ici.
- **POC** : plan dont la sortie est une démo, dans `poc/<sujet>/`, isolé de l'app, des modules et
  des données ; jamais mis en production tel quel.

## Contraintes (non négociables)
- 100 % statique (GitHub Pages) : HTML + CSS + JS vanilla en modules ES. Pas de framework, de
  build, de npm, de serveur, de PWA ; polices système.
- **Asynchrone limité à la lecture de fichiers** (`js/loader.js`) ; stockage, calculs, affichage
  synchrones. Pas de worker, service worker, IndexedDB.
- **Sécurité** : jamais d'`innerHTML` avec du texte de module (`richText()` / `textContent`).
  Les **modules HTML** (JS généré par un LLM) ne sont acceptés que s'ils respectent le contrat
  `docs/module-html.md`, vérifié par `tools/check_html.py` ; ils sont jetables (on les régénère).
- Aucune requête vers un tiers, aucun compte, aucun suivi.
- **Données des enfants** (`localStorage`, clés `miniprof.v1.*`, événements compacts, tout est
  recalculé) : ne jamais les casser ; tout changement de format = nouvelle clé ou migration, avec
  un test. Un push arrive directement sur leurs appareils.
- **Vie privée** : dépôt public. Jamais de photo, de prénom réel ni d'export dans le dépôt (fiches
  comprises).

## Où sont les choses
- `pilotage.md` : plan en cours, plans en attente de feed-back, backlog, tâches du sponsor (le
  seul fichier que lit le sponsor). `plans/` : une fiche par plan (abandonnés compris) et
  `index.md`, une ligne par plan, à lire en premier.
- Carte complète du dépôt et des docs : `README.md`, « Reprendre le projet ». Repères : l'app
  (`index.html`, `js/`, `js/screens/`) ; les modules (`modules/`, `index.json` généré,
  `brouillons.json`) ; `schema/module.schema.json` (source de vérité des modules JSON) ; les
  outils et leurs tests (`tools/`, `tools/tests/`) ; `docs/gabarit-module.html` (page de départ
  d'un module HTML). `docs/recette.md` et `reference/` sont des archives : ne pas les relire.

## Commandes
```bash
python tools/check_html.py modules/<id>.html  # contrat d'un module HTML (--llm : texte pour le LLM)
python tools/tirage.py modules/<id>.html      # tire des milliers de questions, cherche les ambiguïtés
python tools/validate.py modules/<id>.json    # module JSON
python tools/build_index.py                   # régénère modules/index.json
python -m unittest discover tools/tests -v    # tests
python tools/recette_navigateur.py            # recette auto de l'app (Chrome/Chromium, CHROME=…)
```
`python` introuvable : `python3` ; module manquant : `pip install -r tools/requirements.txt`.
Site : https://ghpz5649xx-blip.github.io/miniprof/ (un push sur `main` publie en une minute).

## Règles à garder synchronisées (vérifiées par `tools/tests/test_sync.py` sauf mention)
- `normalize_text()` (`tools/common.py`) ≡ `normalizeText()` (`js/answers.js`) : cas partagés dans
  `tools/tests/fixtures/normalisation.json`.
- Champs obligatoires du schéma ≡ `REQUIRED`, `REQUIRED_QUESTION`, `TYPES_CONNUS`, `BLOCS_CONNUS`
  de `js/check-module.js` ; pas d'`innerHTML` dans `js/`.
- `js/suivi.js` n'écrit que par `addEvents()` ; le skill `/nouveau-module` lance `check_html.py`,
  `build_index.py`, les tests, et ne cite que des fichiers qui existent.
- `tools/analyse.py` ≡ app : `COLONNES` ≡ cases de `js/events.js`, `est_en_baisse()` ≡ `js/stats.js`
  (non testé : à vérifier à la main).

## Façon de travailler
- **Synchronisé avec `origin/main`** : le hook `synchro.sh` met à jour en début de session (prévenir
  le sponsor s'il échoue) ; `git pull --rebase origin main` avant chaque push ; en cas de conflit,
  s'arrêter et demander.
- **Tests avant un push** : seulement si le push touche du code ou du contenu (`js/`, `tools/`,
  `modules/`, `schema/`, `index.html`, `index.json`), une fois par unité, juste avant le push final.
  Un push de doc seule (`pilotage.md`, `plans/`, `README.md`, `CLAUDE.md`) ne se teste pas. Les
  tests et le push sont deux commandes séparées : s'ils échouent, on ne pousse pas.
- **Une unité est finie** quand : les tests passent ; les contrôles concernés passent et
  `modules/index.json` est régénéré ; la recette (`tools/recette_navigateur.py`, plus ce qu'il
  faut regarder à l'écran) est écrite dans la fiche du plan ; `plans/index.md`, `pilotage.md` et
  le `README.md` (si le fonctionnement change) sont à jour ; commit clair et push.
- **Pendant l'exécution, s'arrêter et demander** sur un point que le plan n'a pas tranché :
  contrainte non négociable, choix visible par les enfants, format de stockage, contenu d'un
  module. Ce qui touche les enfants passe par le brouillon quand c'est possible ; sinon la recette
  automatique doit être verte avant le push.
- Un problème après un push : `git revert` et push tout de suite, puis analyse.
- Ids stables (module, compétence, question) : ne jamais renuméroter. Fichier de module nommé
  `<id>.json` ou `<id>.html`. Petits fichiers, noms explicites, pas d'abstraction prématurée.
- Pas de nouveau fichier dans `docs/` sans l'accord du sponsor.
