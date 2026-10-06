# miniprof

App de révision pour les enfants : apprendre une leçon pas à pas, s'entraîner avec indices
et corrections, passer des évaluations, suivre sa progression. 100 % statique, hébergée sur
GitHub Pages, sans compte ni serveur ; la progression reste dans le navigateur de l'appareil.

Site : https://ghpz5649xx-blip.github.io/miniprof/ (un push sur `main` publie en une minute).

## Où en est le projet (mis à jour à chaque unité livrée)

- **En service** : l'app (profils, bilan, sauvegarde) et la création de modules HTML depuis
  l'iPhone avec `/nouveau-module` (photos → page publiée → URL par SMS). Utilisée par l'enfant
  de 6e depuis le 6 octobre 2026. Modules : 2 HTML (anglais 6e, circuit 6e), 2 JSON (CM2).
- **Dernière livraison** : un gabarit commun pour les modules HTML et `tools/tirage.py`, qui
  tire des milliers de questions pour repérer les erreurs avant publication.
- **En cours : étape 12, la relecture des modules par le parent.** Un module publié reste
  « brouillon » (caché aux enfants) tant que le parent ne l'a pas validé. Fait : le statut
  brouillon. À faire : 2. un écran parent avec la fiche de contrôle des modules JSON ;
  3. la même fiche pour les modules HTML ; 4. le skill `/nouveau-module` qui publie en
  brouillon et valide sur demande.
- **À vérifier par le parent** : liste en tête de `docs/recette.md`.

## Les docs : lesquelles lire

| Pour | Fichier | Quand le lire |
|---|---|---|
| Suivre le projet | ce `README.md` | toujours : état, modes d'emploi |
| | `docs/plan-modules-html.md` | pour le détail et le **pourquoi** des décisions en cours |
| | `docs/recette.md` | ce qui a été vérifié ; en tête, ce qui reste à vérifier par le parent |
| Créer un module | `docs/parent-iphone.md` | marche à suivre depuis l'iPhone |
| Référence (rarement) | `docs/risques.md` | registre des risques et de leurs parades |
| | `docs/besoins.md`, `docs/ux.md` | ce que fait l'app v1, figé |
| Pour Claude Code | `CLAUDE.md`, `docs/module-html.md`, `docs/gabarit-module.html` | règles du dépôt, contrat d'un module HTML, page à copier |

Règle : pas de nouveau fichier dans `docs/` sans accord du parent ; un plan fini ou abandonné
est retiré (l'historique Git le garde) une fois son « pourquoi » reporté ailleurs.

## Installation des outils (une fois)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt     # jsonschema, pandas, matplotlib
```

## Ajouter un module

**Façon habituelle, depuis l'iPhone** : photos de la leçon + `/nouveau-module` dans Claude Code
(onglet Code de l'app Claude). Claude Code écrit la page HTML, la contrôle, la publie et donne
l'URL à envoyer à l'enfant. Marche à suivre : `docs/parent-iphone.md`.

**Module JSON** (ancienne façon, depuis le Mac : questions fixes jouées par l'app, plus long à
produire) :

1. Photographier le cours, les exercices, les contrôles (1 à 10 photos).
2. Générer le prompt « nouveau module » :
   ```bash
   python tools/prompt.py --mode nouveau
   ```
   Il est écrit dans `docs/prompt-nouveau.md` (non versionné) **et copié dans le
   presse-papiers** : le coller dans le LLM avec les photos. Le prompt contient le schéma, les règles pédagogiques,
   l'obligation de vérifier chaque calcul et un exemple court. Il demande la leçon et un
   premier lot de 40 à 60 questions.
3. Coller la réponse du LLM dans un fichier, par ex. `brouillon.json`.
4. Valider :
   ```bash
   python tools/validate.py brouillon.json
   ```
   - Texte autour du JSON (« Voici ton module : ```json … ») → `--nettoyer` réécrit le fichier.
   - Erreurs → `python tools/validate.py brouillon.json --llm`, recopier le texte au LLM,
     remplacer le fichier par sa réponse, revalider. Il faut parfois deux allers-retours :
     les erreurs de structure sont signalées d'abord, les erreurs de cohérence ensuite.
5. **Prévisualiser** dans l'app avant de publier (voir plus bas), et **relire quelques
   questions** : le LLM peut se tromper dans une réponse.
6. Renommer en `modules/<id>.json` (l'`id` est dans le fichier), puis :
   ```bash
   python tools/build_index.py      # met à jour la liste des modules lue par l'app
   git add modules/ && git commit -m "Module : <titre>" && git push
   ```
   `build_index.py` n'indexe que les modules valides et bien nommés ; les autres sont
   listés comme « écartés » avec la raison.

## Compléter ou corriger un module

Un LLM gratuit perd en qualité au-delà de ~60 questions par réponse : la banque (100 à 200
questions) se construit par lots.

```bash
python tools/prompt.py --mode lot modules/<id>.json   # prompt « lot suivant », copié aussi
# coller la réponse du LLM ({"questions": [...]}) dans lot.json, puis :
python tools/merge.py modules/<id>.json lot.json --essai   # tout vérifier sans écrire
python tools/merge.py modules/<id>.json lot.json           # fusionner
python tools/build_index.py
```

Le prompt « lot » liste les compétences, la répartition actuelle et tous les énoncés déjà
présents (pour éviter les répétitions), et indique le premier id à utiliser (ex. `q038`).

`merge.py` :
- ajoute les questions dont l'id est nouveau ;
- **remplace** celles dont l'id existe : c'est ainsi qu'on corrige une question signalée
  (renvoyer la question corrigée avec le **même id**, l'historique des enfants est conservé) ;
- signale les énoncés quasi identiques sous un autre id (doublons probables) et, si le LLM
  renvoie un module complet, les questions disparues (renumérotation) ;
- augmente `version` de 1 ;
- n'écrit le module **que si le résultat est valide** ; sinon il affiche les erreurs et le
  texte à renvoyer au LLM.

## Prévisualiser un module

Dans l'app (serveur local ou GitHub Pages), en bas de la bibliothèque : « Pour les parents :
aperçu d'un module », puis choisir le fichier JSON sur l'appareil. Le module s'ouvre en
mémoire avec un bandeau « Aperçu — non enregistré » : on peut tout tester (leçon,
entraînement, évaluation), **rien n'est enregistré** (ni résultat ni signalement). Recharger
la page ferme l'aperçu.

## Le format de module en bref

Référence complète : `schema/module.schema.json`. Exemple : `modules/maths-cm2-division-euclidienne.json`.

- Métadonnées : `id`, `version`, `title`, `subject`, `level`, `description`.
- `skills` : les compétences (`id`, `label`).
- `lesson` : blocs `text`, `worked_example` (pensée + pourquoi), `guided_steps` (phrases à trous).
- `questions` : `number` (une ou plusieurs cases), `choice` (QCM), `text` (réponse courte),
  chacune avec `difficulty` 1–4, `hint`, `explanation` et, facultatif, `common_errors`
  (message ciblé pour une erreur prévue).
- Mise en forme autorisée dans les textes : `**gras**` et retours à la ligne. Pas de HTML.
- **Ne jamais changer les `id`** d'un module publié : l'historique des enfants y est rattaché.

## Sauvegarder et restaurer

La progression est stockée dans le navigateur de chaque appareil : vider les données du
site ou changer de téléphone la fait perdre. D'où la sauvegarde :

- **Exporter** : écran des profils > « Sauvegarder ou restaurer les données » (ou le lien du
  rappel dans la bibliothèque) > « Exporter mes données ». Le navigateur télécharge
  `miniprof-AAAA-MM-JJ.export.json` (profils, résultats, questions signalées). Le ranger
  dans `exports/` du dépôt : ce dossier et les fichiers `*.export.json` sont **ignorés par
  Git** (données personnelles des enfants).
- **Restaurer** (même écran, accessible sans profil, donc sur un appareil neuf) : choisir le
  fichier, vérifier le résumé (date, nombre de réponses par enfant), puis « Confirmer :
  remplacer les données ». Les données actuelles de l'appareil sont **remplacées**, pas
  fusionnées.
- **Rappel** : la bibliothèque affiche un encadré orange si aucun export depuis 14 jours (ou
  jamais) alors qu'il y a des résultats, ou si le stockage dépasse 70 % (environ 40 000
  réponses). Il n'y a aucune synchronisation entre appareils.

## Analyser la progression

```bash
python tools/analyse.py exports/miniprof-2026-10-04.export.json
python tools/analyse.py export.json --sortie exports/analyse-octobre   # autre dossier
```

Affiche par enfant : réussite, nombre d'essais et temps moyen par compétence, compétences
« à travailler » (moins de 60 % ou en baisse de plus de 15 points sur les 10 derniers
essais, même règle que le bilan de l'app), les questions les plus ratées et les notes des
évaluations. Enregistre des graphiques PNG dans `exports/analyse/` : réussite par
compétence, évolution par semaine, notes des évaluations.

Format de l'export (pour faire évoluer `analyse.py`) : `profiles` (`id`, `name`),
`events` = `{id du profil: [lignes]}`, `flags`. Une ligne d'événement est un tableau :
`[date (s), module, question, compétence, difficulté, mode ("e" entraînement / "v"
évaluation), juste (1/0), durée (s), réponse, clé d'évaluation]`. `charger()` en fait un
DataFrame pandas avec ces colonnes nommées (`COLONNES` en tête du fichier).

## Tester

```bash
python -m unittest discover tools/tests -v   # tests automatiques
python tools/check_html.py modules/*.html    # contrat des modules HTML
python tools/recette_navigateur.py           # recette automatique dans Chrome sans fenêtre
python3 -m http.server 8000                  # puis ouvrir http://localhost:8000
```
L'app doit être servie par un serveur (même local) : ouvrir `index.html` directement
(`file://`) ne marche pas, le navigateur refusant alors de lire les fichiers de modules.

Scénarios de recette, étape par étape : `docs/recette.md`.
