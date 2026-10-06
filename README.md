# miniprof

Une app de révision pour deux enfants (primaire et collège), en français. L'enfant apprend sa
leçon pas à pas, s'entraîne avec des indices et des corrections, passe des évaluations et suit
sa progression. Les leçons (« modules ») sont fabriquées par un LLM, Claude, à partir des photos
du cahier ou du manuel.

- **Site** : https://ghpz5649xx-blip.github.io/miniprof/ (un push sur `main` le met à jour en
  une minute environ).
- **Où en est le projet, ce qui est décidé, ce qui reste à faire** : `pilotage.md`.
- **Règles de travail pour Claude** : `CLAUDE.md`.

Ce README sert à **reprendre le projet** : il explique comment tout fonctionne à quelqu'un qui
découvre le dépôt, ou au sponsor dans quelques années. Il sert aussi de mode d'emploi.

---

## 1. Comment ça marche

### Vue d'ensemble

```
photos d'une leçon
   │  (iPhone, app Claude, onglet Code)
   ▼
/nouveau-module ── Claude écrit modules/<id>.html à partir du gabarit
   │                puis lance les contrôles (contrat, tirage de milliers de questions, tests)
   ▼
push sur GitHub ── GitHub Pages publie la page, en BROUILLON (cachée aux enfants)
   │
   ▼
le parent relit les questions-réponses, essaie la page, répond « valide »
   │
   ▼
le module apparaît dans la bibliothèque ; l'URL est envoyée à l'enfant
   │
   ▼
l'enfant répond ── chaque réponse va dans le journal de son profil (localStorage du téléphone)
   │
   ▼
« Mon bilan » dans l'app ; export → tools/analyse.py sur le Mac
```

### Trois principes qui expliquent presque tout

1. **Aucun serveur.** Le site est statique (HTML, CSS, JavaScript sans framework ni étape de
   build), hébergé gratuitement par GitHub Pages. Pas de compte, pas de base de données, aucune
   requête vers un tiers. Conséquence : le dépôt est **public** (condition de la gratuité), il ne
   contient donc jamais de photo, de prénom réel ni d'export.
2. **Les données des enfants restent sur leur appareil**, dans le `localStorage` du navigateur
   (clés `miniprof.v1.*`). Le journal ne garde que des événements bruts (une ligne par réponse) ;
   tout le reste (réussite, compétences à travailler) est recalculé. Il n'y a ni synchronisation
   ni copie ailleurs : d'où l'export (voir « Sauvegarder »). **Un changement de format de ces
   données exige une nouvelle clé ou une migration** : un push arrive directement sur les
   téléphones des enfants.
3. **Le contenu est produit par un LLM, et contrôlé par du code.** Un LLM peut se tromper (une
   réponse fausse apprise par un enfant est le risque principal du projet). Chaque module passe
   donc des contrôles automatiques, puis la relecture du parent avant d'être visible.

### L'app

`index.html` charge `js/app.js`, qui route par l'adresse (`#/biblio`, `#/module/<id>/bilan`…)
vers un écran de `js/screens/` :

| Écran | Rôle |
|---|---|
| `profiles` | choisir ou créer le profil de l'enfant (un appareil peut en avoir plusieurs) |
| `library` | la bibliothèque des modules (les brouillons n'y sont pas) |
| `module-home`, `lesson`, `practice-setup`, `practice`, `exam-setup`, `exam`, `exam-result` | jouer un module JSON : leçon, entraînement, évaluation |
| `report` | le bilan par module et par compétence |
| `backup` | exporter et restaurer les données |

Les autres fichiers de `js/` sont des briques partagées : `storage.js` (accès protégé au
`localStorage`), `events.js` (le journal), `stats.js` (les calculs du bilan), `answers.js`
(comparaison tolérante des réponses), `ui.js` (affichage sans `innerHTML`), `loader.js` (la seule
partie asynchrone : lire un fichier).

### Deux sortes de modules

| | **Module HTML** (la voie normale depuis octobre 2026) | **Module JSON** (la première voie) |
|---|---|---|
| Fichier | `modules/<id>.html` : une page autonome, avec son propre JavaScript (schémas, animations, questions tirées au hasard) | `modules/<id>.json` : une liste fixe de questions, jouée par les écrans de l'app |
| Fabriqué par | Claude Code, avec le skill `/nouveau-module` | n'importe quel LLM, avec `tools/prompt.py` |
| Contrôlé par | `tools/check_html.py` (le contrat) et `tools/tirage.py` (milliers de questions tirées) | `tools/validate.py` (le schéma `schema/module.schema.json`) |
| Suivi | la page appelle `window.miniprof` (`js/suivi.js`), qui écrit dans le même journal | l'app écrit directement dans le journal |

Pourquoi les deux : une page HTML sait faire ce qu'une liste de questions ne peut pas (un circuit
électrique qu'on manipule, des questions recalculées à chaque fois), mais elle exécute du code
écrit par un LLM sur le site des enfants. Elle n'est acceptée que si elle respecte un **contrat**
(`docs/module-html.md`) : aucune requête réseau, aucun accès direct au stockage, et le suivi
uniquement par `js/suivi.js`. Les modules JSON restent pris en charge.

`modules/index.json` est la liste lue par l'app. Il est **généré** par `tools/build_index.py`,
qui n'y met que les modules conformes. `modules/brouillons.json` liste les modules pas encore
relus par le parent : ils sont indexés avec `"brouillon": true` et cachés dans la bibliothèque.

### Le rôle du LLM

Le projet reste lié à l'usage d'un LLM, même une fois l'app finie : c'est lui qui transforme une
leçon en module. Aujourd'hui :

- **Claude Code** (offre Pro, depuis l'app Claude sur l'iPhone) fait tout le travail : il lit les
  photos, écrit la page, lance les contrôles et publie. Ses consignes sont dans
  `.claude/skills/nouveau-module/SKILL.md` ; il part de `docs/gabarit-module.html` (le moteur
  commun des pages) et suit `docs/module-html.md` (contrat et règles pédagogiques).
- **Claude Code est aussi le mainteneur de l'app** : il code, teste, documente et pilote le
  projet (voir « Gouvernance »).
- **Sans Claude Code** : la voie JSON marche avec n'importe quel LLM (voir « Créer un module JSON
  depuis le Mac »). Un pipeline de modules HTML sans Claude Code a été étudié (robot de contrôle
  GitHub, puis API Claude payée à l'usage, environ 1 $ par module) ; il est au backlog de
  `pilotage.md`.

### La gouvernance

Deux acteurs. **Claude** est chef de projet, architecte, développeur, testeur, responsable de
production et support. **Le parent** est sponsor et client : il décide.

- Le projet est piloté en **comités** : des sessions de 30 minutes ouvertes par le sponsor, sur
  la base de `pilotage.md` (état, décisions à prendre avec options et recommandation, actions,
  backlog, relevé des décisions).
- Entre deux comités, le **service courant** (créer ou corriger un module) se fait à la demande ;
  une **évolution** de l'app ne démarre que sur décision inscrite dans `pilotage.md`, une seule à
  la fois.
- Le détail est dans `CLAUDE.md`, « Gouvernance ».

---

## 2. Mode d'emploi

### Créer un module (depuis l'iPhone)

1. Photographier la leçon et les exercices (page entière, sans prénom ni visage si possible).
2. Ouvrir une nouvelle session dans l'app Claude, onglet **Code**, dépôt `miniprof`.
3. Joindre les photos et écrire, par exemple : `/nouveau-module CM1, la leçon sur les fractions`.
4. La réponse donne l'URL de la page, ce qu'elle contient et **une question avec sa bonne réponse
   pour chaque compétence et chaque niveau**. Le module est en **brouillon** : invisible dans la
   bibliothèque des enfants.
5. Relire ces questions-réponses et essayer la page (une minute après la réponse). Une erreur :
   la dire dans la même session, Claude corrige.
6. Tout est juste : répondre **« valide »**. Le module apparaît dans la bibliothèque ; envoyer
   l'URL à l'enfant (par SMS, par exemple).

Pas à pas, réglages de la première fois compris : `docs/parent-iphone.md`.

**Corriger un module plus tard** : nouvelle session, `/nouveau-module corrige le module <id> :
<ce qui ne va pas>`. **Valider plus tard** : `/nouveau-module valide <id>`. L'adresse et
l'historique de l'enfant sont conservés : **l'id d'un module, de ses compétences et de ses
questions ne change jamais**.

### Côté enfant

L'enfant ouvre l'URL du module (ou le site, puis la bibliothèque) et choisit son profil une
fois par appareil. Une page HTML affiche en haut « Tu es <prénom> · changer · mon bilan » ;
sans profil choisi, rien n'est enregistré. « Mon bilan » montre la réussite par compétence et
les évaluations.

### Sauvegarder et restaurer

La progression est stockée dans le navigateur de chaque appareil : vider les données du site ou
changer de téléphone la fait perdre. D'où la sauvegarde :

- **Exporter** : écran des profils > « Sauvegarder ou restaurer les données » (ou le lien du
  rappel dans la bibliothèque) > « Exporter mes données ». Le navigateur télécharge
  `miniprof-AAAA-MM-JJ.export.json` (profils, résultats, questions signalées). Le ranger dans
  `exports/` sur le Mac : ce dossier et les fichiers `*.export.json` sont **ignorés par Git**
  (données personnelles).
- **Restaurer** (même écran, accessible sans profil, donc sur un appareil neuf) : choisir le
  fichier, vérifier le résumé, puis « Confirmer : remplacer les données ». Les données de
  l'appareil sont **remplacées**, pas fusionnées.
- **Rappel** : la bibliothèque affiche un encadré orange si aucun export depuis 14 jours alors
  qu'il y a des résultats, ou si le stockage dépasse 70 % (environ 40 000 réponses).

### Analyser la progression (sur le Mac)

```bash
python tools/analyse.py exports/miniprof-2026-10-04.export.json
```

Affiche par enfant la réussite, le nombre d'essais et le temps par compétence, les compétences
« à travailler » (moins de 60 %, ou en baisse de plus de 15 points sur les 10 derniers essais :
même règle que le bilan de l'app), les questions les plus ratées et les notes des évaluations.
Enregistre des graphiques dans `exports/analyse/`.

### Créer un module JSON depuis le Mac (voie de secours, n'importe quel LLM)

1. `python tools/prompt.py --mode nouveau` : le prompt (schéma, règles pédagogiques, exemple) est
   écrit dans `docs/prompt-nouveau.md` et copié dans le presse-papiers. Le coller dans le LLM avec
   les photos.
2. Coller la réponse dans un fichier, puis `python tools/validate.py brouillon.json`. Texte autour
   du JSON : `--nettoyer`. Erreurs : `--llm` produit le message à renvoyer au LLM.
3. Prévisualiser dans l'app : en bas de la bibliothèque, « Pour les parents : aperçu d'un
   module » (rien n'est enregistré). **Relire quelques questions.**
4. Renommer en `modules/<id>.json`, puis `python tools/build_index.py`, commit et push.

Compléter un module par lots de 40 à 60 questions : `python tools/prompt.py --mode lot
modules/<id>.json`, puis `python tools/merge.py modules/<id>.json lot.json` (`--essai` pour tout
vérifier sans écrire). `merge.py` ajoute les nouvelles questions, remplace celles de même id (c'est
ainsi qu'on corrige une question), signale les doublons probables, et n'écrit que si le résultat
est valide.

---

## 3. Reprendre le projet

### Installer les outils (une fois, sur le Mac)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt     # jsonschema, pandas, matplotlib
```

`node` est utile en plus pour `tools/tirage.py`. Une session Claude Code dans le cloud installe
ce qu'il lui faut seule.

### Tester

```bash
python -m unittest discover tools/tests -v   # tests automatiques
python tools/check_html.py modules/*.html    # contrat des modules HTML
python tools/tirage.py modules/<id>.html     # milliers de questions tirées et vérifiées
python tools/recette_navigateur.py           # recette automatique de l'app (Chrome sans fenêtre)
python3 -m http.server 8000                  # puis ouvrir http://localhost:8000
```

L'app doit être servie par un serveur, même local : ouverte directement (`file://`), elle ne peut
pas lire les fichiers de modules.

### Carte du dépôt

| Chemin | Contenu |
|---|---|
| `pilotage.md` | état du projet, décisions, actions, backlog (pour le sponsor) |
| `CLAUDE.md` | règles du dépôt pour Claude : gouvernance, contraintes, commandes, conventions |
| `index.html`, `css/`, `js/` | l'app |
| `modules/` | les modules, `index.json` (généré), `brouillons.json` |
| `schema/module.schema.json` | le format des modules JSON (source de vérité) |
| `tools/` | outils Python : validation, contrôle, tirage, index, prompt, fusion, analyse, recette ; `tools/tests/` |
| `.claude/` | le skill `/nouveau-module` et le hook qui met la session à jour au démarrage |
| `docs/` | annexes, voir ci-dessous |
| `reference/` | le prototype d'origine, gardé pour mémoire |

### Les docs

| Fichier | Contenu |
|---|---|
| `docs/parent-iphone.md` | créer un module depuis l'iPhone, pas à pas |
| `docs/module-html.md` | le contrat des modules HTML et les règles pédagogiques |
| `docs/gabarit-module.html` | la page de départ de tout module HTML |
| `docs/plan-modules-html.md` | le plan en cours et le **pourquoi** de ses choix |
| `docs/recette.md` | ce qui a été vérifié à chaque étape, et comment |
| `docs/risques.md` | les risques du projet et leurs parades |
| `docs/besoins.md`, `docs/ux.md` | les besoins et l'interface de la première version (figés) |

Le **pourquoi** d'une décision se trouve, par ordre : dans le relevé des décisions de
`pilotage.md`, dans le plan, dans `docs/risques.md`, dans les commentaires du code, enfin dans
l'historique Git (les plans finis y restent lisibles).

### Points de vigilance

- **Ne jamais casser les données des enfants** (`miniprof.v1.*`) : nouvelle clé ou migration
  testée.
- **Ne jamais publier de photo, de prénom réel ni d'export** : le dépôt est public, et
  l'historique Git garde tout.
- **Ne jamais changer un id** (module, compétence, question) : l'historique y est rattaché.
- **Pas d'`innerHTML` avec du texte de module dans l'app** (`test_sync.py` le vérifie) ; les pages
  HTML passent `check_html.py`.
- **Règles à garder synchronisées** entre Python et JavaScript : liste dans `CLAUDE.md`.

### Format d'un module JSON, en bref

Référence complète : `schema/module.schema.json` ; exemple :
`modules/maths-cm2-division-euclidienne.json`.

- Métadonnées : `id`, `version`, `title`, `subject`, `level`, `description`.
- `skills` : les compétences (`id`, `label`).
- `lesson` : blocs `text`, `worked_example`, `guided_steps`.
- `questions` : `number`, `choice` ou `text`, chacune avec `difficulty` 1 à 4, `hint`,
  `explanation` et, facultatif, `common_errors`.
- Mise en forme autorisée : `**gras**` et retours à la ligne, pas de HTML.

### Format du journal (export et `tools/analyse.py`)

Un export contient `profiles` (`id`, `name`), `events` (`{id du profil: [lignes]}`) et `flags`.
Une ligne du journal : `[date (s), module, question, compétence, difficulté, mode ("e"
entraînement / "v" évaluation), juste (1/0), durée (s), réponse, clé d'évaluation]`.
`tools/analyse.py` en fait un tableau pandas (colonnes : `COLONNES` en tête du fichier).
