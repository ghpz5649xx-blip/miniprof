# miniprof

App de révision pour les enfants : apprendre une leçon pas à pas, s'entraîner avec indices
et corrections, passer des évaluations, suivre sa progression. 100 % statique, hébergée sur
GitHub Pages, sans compte ni serveur ; la progression reste dans le navigateur de l'appareil.

> État : **étape 2** livrée (profils, bibliothèque, ouverture d'un module). Les activités
> Apprendre, S'entraîner, Évaluation et Bilan arrivent aux étapes 3 à 6.

## Installation des outils (une fois)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
```

## Ajouter un module

1. Photographier le cours, les exercices, les contrôles (1 à 10 photos).
2. Envoyer les photos au LLM avec le prompt « nouveau module » (`tools/prompt.py`, étape 7).
3. Coller la réponse du LLM dans un fichier, par ex. `brouillon.json`.
4. Valider :
   ```bash
   python tools/validate.py brouillon.json
   ```
   - Texte autour du JSON (« Voici ton module : ```json … ») → `--nettoyer` réécrit le fichier.
   - Erreurs → `python tools/validate.py brouillon.json --llm`, recopier le texte au LLM,
     remplacer le fichier par sa réponse, revalider. Il faut parfois deux allers-retours :
     les erreurs de structure sont signalées d'abord, les erreurs de cohérence ensuite.
5. **Relire quelques questions** : le LLM peut se tromper dans une réponse.
6. Renommer en `modules/<id>.json` (l'`id` est dans le fichier), puis :
   ```bash
   python tools/build_index.py      # met à jour la liste des modules lue par l'app
   git add modules/ && git commit -m "Module : <titre>" && git push
   ```
   `build_index.py` n'indexe que les modules valides et bien nommés ; les autres sont
   listés comme « écartés » avec la raison.

Compléter un module (lots de 40 à 60 questions) : `tools/merge.py` (étape 7).

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

## Tester

```bash
python -m unittest discover tools/tests -v   # tests automatiques
python3 -m http.server 8000                  # puis ouvrir http://localhost:8000
```
L'app doit être servie par un serveur (même local) : ouvrir `index.html` directement
(`file://`) ne marche pas, le navigateur refusant alors de lire les fichiers de modules.

## Sauvegarder et analyser la progression

À venir (étapes 6 et 7) : export/import depuis l'app, analyse avec `tools/analyse.py`.
