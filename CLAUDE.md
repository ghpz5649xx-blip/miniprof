# miniprof

App web de révision pour 2 enfants, en français. **Année 2026-2027 : le fils est en CM1, la fille
en 6e** (niveau par défaut d'un module). Le parent lit le Python, peu le JS : code simple,
commenté en français (le **pourquoi**). Comment tout marche : `README.md`.

## Comment on travaille
- Le parent est le sponsor : il décide. Claude le tutoie, l'appelle par son prénom, « le
  sponsor » dans le dépôt (public), et pose **une question à la fois**.
- Début de session : lire `pilotage.md` (plan en cours, backlog, tâches du sponsor). Un sujet
  passé : `plans/index.md`, puis sa seule fiche.
- **Pas de code sans le go du sponsor**, sauf une correction courte sur un plan livré et une
  session module (photos + demande : suivre `.claude/skills/nouveau-module/SKILL.md`, sans fiche).
- Un sujet = une fiche dans `plans/` (besoin, décisions, livré, vérifié, tâches du sponsor).
  Un seul plan ouvert à la fois, en tête de `pilotage.md`.
- Fin de tâche : fiche, `plans/index.md` et `pilotage.md` à jour, commit, push, et un mot au
  sponsor. Ce qui demande l'iPhone devient une tâche du sponsor.

## Contraintes (non négociables)
- 100 % statique (GitHub Pages) : HTML + CSS + JS vanilla en modules ES. Pas de framework, de
  build, de npm, de serveur, de PWA, de worker ni d'IndexedDB ; polices système. Asynchrone
  seulement pour lire des fichiers et partager (`js/loader.js`, `js/partage.js`).
- **Sécurité** : jamais d'`innerHTML` avec du texte de module (`richText()` / `textContent`).
  Un module HTML doit passer `tools/check_html.py` (contrat : `docs/module-html.md`).
- Aucune requête vers un tiers, aucun compte, aucun suivi.
- **Données des enfants** (`localStorage`, clés `miniprof.v1.*`) : ne jamais les casser ; tout
  changement de format = nouvelle clé ou migration, avec un test. Un push arrive directement
  sur leurs appareils.
- **Vie privée** : jamais de photo, de prénom réel ni d'export dans le dépôt.

## Repères
- L'app : `index.html`, `js/`. Les modules : `modules/` (`index.json` est généré). Le schéma :
  `schema/module.schema.json`. Les outils et tests : `tools/`.
- `docs/recette.md` et `reference/` sont des archives : ne pas les relire.

## Commandes
```bash
python tools/check_html.py modules/<id>.html  # contrat d'un module HTML
python tools/tirage.py modules/<id>.html      # cherche les questions ambiguës
python tools/validate.py modules/<id>.json    # module JSON
python tools/build_index.py                   # régénère modules/index.json
python -m unittest discover tools/tests -v    # tests (dont la synchro Python ≡ JS)
python tools/recette_navigateur.py            # recette auto de l'app
```
`python` introuvable : `python3`. Site : https://ghpz5649xx-blip.github.io/miniprof/ (un push
sur `main` publie en une minute).

## Règles de travail
- Avant de pousser du code ou un module : tests verts. S'ils échouent, on ne pousse pas.
- `git pull --rebase origin main` avant chaque push ; en cas de conflit, s'arrêter et demander.
- **S'arrêter et demander** sur un point non tranché : contrainte ci-dessus, choix visible par
  les enfants, format de stockage, contenu d'un module.
- Un problème après un push : `git revert`, push, puis analyse.
- Ids stables (module, compétence, question) : ne jamais renuméroter.
- Non testé, à vérifier à la main : `tools/analyse.py` ≡ `js/events.js` et `js/stats.js`.
