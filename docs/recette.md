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
