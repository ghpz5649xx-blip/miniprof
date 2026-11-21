# miniprof

App web de révision pour 2 enfants, en français. **Année 2026-2027 : le fils est en CM1, la fille
en 6e** (niveau par défaut d'un module). Comment tout marche : `README.md`.

## Particularités de l'organisation
- **Début de session** : lire `pilotage.md` (les tâches du sponsor) et `modules/brouillons.json`.
  Signaler au sponsor chaque tâche échue (refaire, reporter ou abandonner ?) et chaque module en
  brouillon qui attend sa validation.
- `pilotage.md` ne contient que les tâches du sponsor : 6 au plus, chacune avec une échéance
  datée. Retirer une tâche dès qu'elle est faite ou abandonnée.
- Plans : une fiche par sujet dans `plans/`, index dans `plans/index.md`. Le plan en cours est
  celui au statut « en cours » de l'index ; les idées sans fiche sont en bas de l'index.
- **Exception au « go avant de coder » : la session module.** Photos + demande : suivre
  `.claude/skills/nouveau-module/SKILL.md`, sans fiche.
- Ce qui demande l'iPhone devient une tâche du sponsor.

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
- **Vie privée** : dépôt public. Jamais de photo, de prénom réel ni d'export dans le dépôt.

## Repères
- L'app : `index.html`, `js/`. Les modules (pages HTML) : `modules/` (`index.json` est généré). Les outils et tests : `tools/`.
- `docs/recette.md` et `reference/` sont des archives : ne pas les relire.

## Commandes
```bash
python tools/check_html.py modules/<id>.html  # contrat d'un module HTML
python tools/tirage.py modules/<id>.html      # cherche les questions ambiguës
python tools/couverture_dictee.py modules/<id>.html "mot1,mot2"   # une dictée pose tous ses mots
python tools/build_index.py                   # régénère modules/index.json
python -m unittest discover tools/tests -v    # tests (dont la synchro Python ≡ JS)
python tools/recette_navigateur.py            # recette auto de l'app
```
`python` introuvable : `python3`. Site : https://ghpz5649xx-blip.github.io/miniprof/ (un push
sur `main` publie en une minute).

## À vérifier à la main (non testé)
- `tools/analyse.py` ≡ `js/events.js` et `js/stats.js`.
