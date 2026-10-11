# miniprof

App web d'entraînement et d'évaluation pour 2 enfants, en français. **Année 2026-2027 : le fils est
en CM1, la fille en 6e** (à prendre par défaut pour un module, sans le redemander au sponsor).
Le parent (à l'aise en Python, peu en JS) doit pouvoir **lire** le code (pas forcément le
corriger) : c'est aussi ce qui permet à la session Claude suivante de reprendre.

## Gouvernance (méthode décidée par le sponsor le 12 octobre 2026)
- **Deux acteurs.** **Claude** : chef de projet, architecte fonctionnel, développeur, PMO,
  testeur, responsable de production, support ; il fait la synthèse, propose les priorités,
  porte un regard critique et propose des améliorations. **Le parent** : sponsor et client
  (profil chef de projet / BA) ; il décide. Claude le tutoie et l'appelle par son prénom dans la
  conversation ; dans le dépôt (public), il est « le sponsor », sans nom. Claude pose **une
  question à la fois**.
- **Une session = un sujet, un plan.** Elle repart de zéro : Claude relit `pilotage.md` (plan en
  cours, backlog, tâches du sponsor) et, si un plan passé est évoqué, `plans/index.md` puis la
  seule fiche utile. Si une conversation devient longue, Claude propose d'en ouvrir une nouvelle.
- **Début de session** : Claude propose **un ou deux sujets** du backlog, avec ses raisons (pas
  tout le backlog, sauf si revoir l'ensemble des priorités lui semble important) ; le sponsor
  valide, corrige ou apporte son propre sujet.
- **Atelier de cadrage** : échanges courts (besoin, pour quel enfant, périmètre, contraintes,
  risques, coût, ce qu'on perd), dans l'esprit d'une phase de cadrage de projet. Pendant
  l'atelier, Claude ne fait que des lectures rapides ; une vraie investigation devient un
  **plan d'étude** (sa sortie est une analyse, pas du code). Quand le plan est assez précis, l'un
  propose, l'autre donne son avis.
- **Trois sorties possibles** : **rien** (plan abandonné, fiche gardée avec son pourquoi) ;
  **à mûrir** (fiche dans `plans/`, ligne dans le backlog) ; **à exécuter** : sur le **go** du
  sponsor seulement, Claude exécute (développe, teste, fait la recette, documente, pousse).
  Les tâches lourdes ne se lancent qu'après le go, à la fin de la session.
- **Un seul plan ouvert à la fois** : la ligne « Plan en cours » de `pilotage.md` le dit ; une
  autre session qui la voit n'en ouvre pas. Un plan à mûrir ne bloque pas : il attend au backlog.
  Exceptions : un feed-back, et une session module.
- **Fin d'exécution** : Claude écrit la fiche du plan (livré, vérifié, tâches du sponsor),
  pousse, puis **déclare la session terminée** et prévient le sponsor (notification de l'app si
  elle arrive ; sinon le résumé dans la session et sur le dépôt fait foi). Ce qui demande
  l'iPhone devient une **tâche du sponsor**, à valider ou contester par feed-back.
- **Feed-back** (même plusieurs jours après) : le sponsor cite le plan (« feed-back sur P003 »)
  ou décrit le sujet ; Claude retrouve la fiche par l'index. Une correction courte, dans le
  périmètre de la fiche, se fait tout de suite, même si un autre plan est ouvert ; si elle élargit
  le périmètre, c'est un nouveau plan. Elle est notée dans la fiche. **Une fiche exécutée se ferme
  2 semaines après**, sans retour.
- **Session module** (créer ou corriger le contenu d'un module) : les photos et la demande du
  sponsor servent de plan, Claude exécute tout de suite en suivant la grammaire de
  `.claude/skills/nouveau-module/SKILL.md` (gabarit, contrat, contrôles, brouillon puis
  « valide »), que le sponsor tape `/nouveau-module` ou non. Pas de fiche. Si la demande oblige à
  changer la grammaire elle-même (moteur du gabarit, contrat, nouveau type de question ou
  d'interaction), c'est un plan qui demande un go.
- **Revue d'usage** : environ toutes les 2 semaines, Claude propose un plan d'étude à partir des
  exports des enfants (`tools/analyse.py`) : constats et corrections de modules.
- **Backlog** : chaque ligne a une date ; au-delà de 10 lignes, ou pour une ligne de plus d'un
  mois, Claude propose un tri.
- **Décisions** : celles d'un plan vont dans sa fiche, avec leur pourquoi ; celles qui valent pour
  tout le projet vont dans ce fichier.
- **POC** : un plan dont la sortie est une démonstration, proposé par Claude ou demandé par le
  sponsor. Dossier `poc/<sujet>/` autonome, sans lien depuis l'app, qui ne touche ni l'app, ni les
  modules, ni les données ; jamais mis en production tel quel (go = plan refait proprement).

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
- `pilotage.md` : plan en cours, plans exécutés en attente de feed-back, backlog actif, tâches du
  sponsor ; seul doc que lit le sponsor.
- `plans/` : une fiche par plan (`P001-<nom>.md` : besoin, périmètre, décisions et pourquoi,
  livré, vérifié, tâches du sponsor, feed-back), y compris les plans abandonnés ; `index.md` :
  une ligne par plan (numéro, date, titre, statut, mots-clés, résumé, chemin), à lire en premier.
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
- `README.md` : documentation de reprise du projet (comment tout marche, mode d'emploi, carte
  du dépôt et des docs) ; à tenir à jour quand le fonctionnement change.
- `docs/` (carte : `README.md`, « Les docs ») : `plan-modules-html.md` (plan en cours),
  `recette.md` (ce qui a été vérifié, et comment), `parent-iphone.md` (créer un
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
- **Rester synchronisé avec `origin/main`** (le parent travaille depuis l'iPhone et le Mac,
  plusieurs sessions peuvent pousser en parallèle) : mise à jour en début de session par le hook
  `synchro.sh` (si son message signale un échec, prévenir le parent), puis
  `git pull --rebase origin main` juste avant chaque push et relancer les tests. En cas de
  conflit, s'arrêter et demander au parent.
- Rien ne s'exécute sans **go** du sponsor (voir « Gouvernance ») ; une idée nouvelle, la sienne
  ou celle de Claude, va au backlog au lieu d'être réalisée dans la conversation où elle naît.
  Restent possibles sans go : une session module, une correction de feed-back, une réponse à une
  question, un `git revert` en cas d'incident. Un plan exécuté est découpé en **unités
  vérifiables**.
- Une unité est **finie** quand :
  1. `python -m unittest discover tools/tests -v` passe ;
  2. les contrôles concernés passent (`validate.py`, `check_html.py`, `build_index.py`) et
     `modules/index.json` est régénéré ;
  3. la recette est faite dans le navigateur : `tools/recette_navigateur.py` (à compléter quand
     une évolution le permet), plus ce qui demande de regarder l'écran ; elle est écrite dans la
     **fiche du plan** (`docs/recette.md` est l'archive figée des étapes 1 à 12) ;
  4. les docs touchées sont à jour (arborescence, « Règles à garder synchronisées »), ainsi que
     la fiche du plan, `plans/index.md`, `pilotage.md` et le `README.md` si le fonctionnement
     change ;
  5. commit clair, puis **push**.
- **S'arrêter et demander au parent**, sans pousser, si l'exécution rencontre un point que le plan
  n'a pas tranché : changement d'une contrainte non négociable, choix pédagogique ou d'UX visible
  par les enfants, changement du format de stockage, point qui demande son jugement (contenu
  d'un module). Ce qui touche les enfants passe par le brouillon quand c'est possible ; sinon la
  recette automatique doit être verte avant le push.
- Si un problème apparaît après un push : `git revert` et push tout de suite, puis analyse.
- Toute décision non évidente est écrite avec son **pourquoi** dans le doc concerné (plan,
  `risques.md`, commentaire), pas seulement dans le message de commit.
- Signaler au parent ce qui ajoute du travail manuel de son côté ou un risque pour les données
  des enfants.
- **Docs sobres** : le sponsor suit le projet par `pilotage.md` seulement ; les fiches de
  `plans/` gardent le détail ; les autres docs sont des annexes. Pas de nouveau fichier dans
  `docs/` sans son accord. Dépôt public : aucune fiche ne contient de prénom, de donnée d'export
  ni de photo.

## Prochaines étapes
- État : `pilotage.md` ; plans : `plans/index.md`.
- Créer un module : le parent passe par `/nouveau-module` depuis l'iPhone
  (`docs/parent-iphone.md`) ; les sessions dans le cloud suivent le même `CLAUDE.md`.
