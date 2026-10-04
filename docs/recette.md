# Recette

Scénarios à jouer à la main, étape par étape. Cocher quand le résultat obtenu correspond.

## Étape 1 — Schéma, validateur, module d'exemple

Préparation (une seule fois, depuis la racine du dépôt) :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
```

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 1.1 | `python tools/validate.py modules/maths-cm2-division-euclidienne.json` | « ✔ VALIDE », 2 avertissements (37 questions < 100 ; pas de difficulté 4 en vocabulaire), tableau de répartition (6 compétences, total 37). Code retour 0 (`echo $?`). | ☐ |
| 1.2 | Ouvrir le module ; dans la question `q001`, remplacer la réponse du quotient `"answer": 5` par `"answer": "5"` ; valider | « ✘ INVALIDE », message `questions[0].fields[0].answer (question q001) : doit être un nombre (reçu : un texte "5")`. Code retour 1. | ☐ |
| 1.3 | Même fichier, avec `--llm` | Texte commençant par « Ton JSON contient les erreurs suivantes », la même erreur, et la consigne de renvoyer le JSON complet. | ☐ |
| 1.4 | Changer le `skill` d'une question en `"inconnu"` | Erreur « compétence « inconnu » absente de skills ». | ☐ |
| 1.5 | Dans un QCM (`verifier`), mettre `"answer": "z"` | Erreur « « z » ne fait pas partie des choix (a, b, c) ». | ☐ |
| 1.6 | Ajouter une virgule après le dernier champ d'un objet | Erreur « JSON mal formé ligne N, colonne M : virgule en trop avant } ou ] ». | ☐ |
| 1.7 | Copier `tools/tests/fixtures/entoure.txt` vers `/tmp/essai.json`, valider | Erreur unique : texte autour du JSON, conseil `--nettoyer`. | ☐ |
| 1.8 | Relancer 1.7 avec `--nettoyer` | « Fichier réécrit en JSON propre », puis « ✔ VALIDE ». Le fichier commence par `{`. | ☐ |
| 1.9 | `python -m unittest discover tools/tests -v` | 23 tests, tous « ok ». | ☐ |
| 1.10 | Relecture pédagogique : lire 5 questions et la leçon dans le fichier du module | Textes justes, niveau CM2, indices qui ne donnent pas la réponse. | ☐ |

Annuler les modifications de test du module après la recette : `git checkout modules/`.

## Étape 2 — Squelette de l'app, profils, chargement des modules

Préparation : `source .venv/bin/activate`, puis dans un 2e terminal `python3 -m http.server 8000`
(à laisser tourner) et ouvrir **http://localhost:8000** (une fenêtre de navigation privée
permet de repartir de zéro).

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 2.1 | `python tools/build_index.py` | « ✔ 1 module(s) indexé(s) », ligne `maths-cm2-division-euclidienne.json (CM2, 37 questions)`. Code retour 0. `git status` : `modules/index.json` inchangé (il est déjà commité). | ☐ |
| 2.2 | Ouvrir l'app pour la première fois | Titre « miniprof », « Bienvenue ! Crée ton profil pour commencer. », champ « Ajouter un profil » avec le curseur dedans. | ☐ |
| 2.3 | Taper « Léa », touche Entrée ; puis « Tom », clic sur OK | Deux gros boutons « Léa » et « Tom » ; le texte devient « Qui es-tu ? ». | ☐ |
| 2.4 | Valider un prénom vide ; puis « léa » | Encadré rouge « Écris un prénom. » ; puis « Le profil « léa » existe déjà. » avec la saisie conservée. Le champ n'accepte pas plus de 20 caractères. | ☐ |
| 2.5 | Cliquer « Léa » | « Bonjour Léa ! », titre « Mathématiques », carte « Division euclidienne », badge « CM2 », description. | ☐ |
| 2.6 | Recharger la page (F5), puis fermer l'onglet et rouvrir http://localhost:8000 | On reste / on revient sur la bibliothèque de Léa. | ☐ |
| 2.7 | « Changer de profil » | Retour au choix du profil. | ☐ |
| 2.8 | Ouvrir le module | Titre, description, « CM2 · 37 questions », 4 cartes grisées « Bientôt (étape n) ». Bouton « ← Retour » → bibliothèque ; rouvrir le module puis bouton retour du navigateur → bibliothèque. | ☐ |
| 2.9 | Sécurité : `cp modules/maths-cm2-division-euclidienne.json modules/maths-cm2-test.json`, dans la copie mettre `"id": "maths-cm2-test"` et `"title": "<b>Test</b> **gras**"`, puis `build_index.py`, recharger | Dans la bibliothèque et dans la page du module, le titre s'affiche « <b>Test</b> **gras** » avec les chevrons visibles et le mot « gras » en gras (sans les étoiles). Le HTML n'est jamais interprété. | ☐ |
| 2.10 | Module cassé : dans `maths-cm2-test.json`, ajouter une virgule après le dernier champ (sans relancer `build_index`), recharger, ouvrir « <b>Test</b> … » puis l'autre module | Bibliothèque intacte ; le module test affiche « Ce module ne peut pas s'ouvrir. Le fichier … n'est pas un JSON valide » + « Retour à la bibliothèque » ; l'autre module s'ouvre normalement. | ☐ |
| 2.11 | `python tools/build_index.py` avec le fichier cassé | Le fichier est listé dans « ✘ fichier(s) écarté(s) » avec la raison ; code retour 1. Ensuite : `rm modules/maths-cm2-test.json && python tools/build_index.py`. | ☐ |
| 2.12 | Accueil > « Gérer les profils » > « Supprimer » sur Tom | 1er clic : bouton rouge « Confirmer : supprimer Tom » ; 2e clic : Tom disparaît. « Terminé » revient à l'accueil. | ☐ |
| 2.13 | Outils de développement (⌥⌘I) > mode appareil, largeur 360 px | Pas de défilement horizontal, boutons pleine largeur faciles à toucher. | ☐ |
| 2.14 | Passer le Mac en apparence sombre | Couleurs sombres, textes lisibles. | ☐ |
| 2.15 | Onglet Réseau, recharger | Seules des requêtes vers `localhost:8000` (html, css, js, json). | ☐ |
| 2.16 | `python -m unittest discover tools/tests -v` | 31 tests, tous « ok » (dont `test_sync` : listes de champs alignées avec le schéma, aucun `innerHTML`). | ☐ |

Après la recette : `git status` doit être propre (sinon `git checkout modules/`).
