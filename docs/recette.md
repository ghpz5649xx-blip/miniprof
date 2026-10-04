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

## Étape 3 — Apprendre (la leçon)

Préparation : comme l'étape 2 (serveur sur **http://localhost:8000**, un profil créé).

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 3.1 | Ouvrir le module | Carte « Apprendre » active (cliquable) ; les 3 autres grisées « Bientôt (étape n) ». | ☐ |
| 3.2 | « Apprendre » | Barre « ← Retour / Apprendre », « Étape 1 sur 12 », titre « L'histoire de Nolan », texte avec mots en gras et retours à la ligne. Touche Entrée = « Continuer ». | ☐ |
| 3.3 | « Continuer » → « Lire une division euclidienne » | Phrase d'intro, 4 cartes « pensée » chacune avec « Pourquoi : … » en gris, encadré vert « dividende = diviseur × quotient + reste ». | ☐ |
| 3.4 | « Continuer » → « La table de 19 » | « 2 × 19 = [case] », curseur dans la case (clavier numérique sur téléphone). | ☐ |
| 3.5 | Valider sans rien taper ; puis « abc » ; puis « 37 » | « Écris ta réponse. » ; « Écris un nombre. » ; « Pas encore. » + indice, saisie sélectionnée. Tous en orange. | ☐ |
| 3.6 | Taper « 38 » + Entrée | La ligne « 2 × 19 = **38** ✓ » reste affichée, « 3 × 19 = [case] » apparaît avec le curseur dedans. | ☐ |
| 3.7 | Finir la table (57, 76, 95, 114, 133, 152, 171) | 8 lignes cochées, encadré vert de conclusion, bouton « Continuer ». | ☐ |
| 3.8 | Aller jusqu'à « Trouver le quotient » | La case est au milieu de la phrase : « Il reste 341 − 190 = [case] cartes à partager. » | ☐ |
| 3.9 | « Nolan a de la ruse » : répondre 342 puis 0 | « 0 » est accepté ; conclusion sur deux lignes. | ☐ |
| 3.10 | Dernier bloc « À retenir » → « Continuer » | « Bravo, tu as fini la leçon ! », boutons « Je m'entraîne » et « Accueil du module ». « Je m'entraîne » ouvre le réglage de l'entraînement (depuis l'étape 4). | ☐ |
| 3.11 | Pendant la leçon : « ← Retour », puis bouton retour du navigateur | Les deux ramènent à l'accueil du module. Recharger (F5) pendant la leçon : elle reprend à l'étape 1. | ☐ |
| 3.12 | Adresse `…/#/module/maths-cm2-division-euclidienne/apprendre/preuve` | « Revoir : Retrouver le dividende », « Étape 1 sur 2 ». Avec `…/apprendre/inconnu` : « Cette compétence n'existe pas dans ce module. » + « Accueil du module ». | ☐ |
| 3.13 | Sécurité : copie de test du module (comme 2.9), mettre `"prompt": "<b>2</b> × 19 = ▢"` dans la 1re mini-étape, `build_index.py`, ouvrir sa leçon | « <b>2</b> × 19 = » s'affiche avec les chevrons. | ☐ |
| 3.14 | Bloc cassé (avant de supprimer la copie de 3.13) : y supprimer le `"body"` du premier bloc, ouvrir l'adresse `…/#/module/maths-cm2-test` (le module, devenu invalide, n'est plus dans la bibliothèque après `build_index.py`, mais reste ouvrable par son adresse) | Accueil du module : encadré orange « 1 bloc(s) de leçon mal formé(s) ignoré(s) » ; la leçon commence au bloc suivant (« Étape 1 sur 11 »). Ensuite : `rm modules/maths-cm2-test.json && python tools/build_index.py`. | ☐ |
| 3.15 | Règles de réponse côté JS : console du navigateur (Safari ⌥⌘C, Chrome ⌥⌘J) sur l'app, coller le code ci-dessous | Affiche `[]` (aucun cas en échec). | ☐ |
| 3.16 | 360 px de large, thème sombre | La case reste dans la phrase ou passe à la ligne, pas de défilement horizontal ; textes lisibles. | ☐ |
| 3.17 | `python -m unittest discover tools/tests -v` | 33 tests, tous « ok » (dont `test_normalisation` et `test_types_de_bloc`). | ☐ |

Code pour 3.15 (compare `js/answers.js` aux cas partagés avec Python) :

```js
Promise.all([
  import("/js/answers.js"),
  fetch("/tools/tests/fixtures/normalisation.json").then(r => r.json()),
]).then(([{ normalizeText, parseNumber }, cas]) => console.log(
  cas.texte.filter(([e, a]) => normalizeText(e) !== a)
    .concat(cas.nombres.filter(([e, a]) => parseNumber(e) !== a))
));
```

Pas de `await` au niveau supérieur : la console de Safari ne l'accepte pas.

Après la recette : `git status` doit être propre (sinon `git checkout modules/`).

## Étape 4 — S'entraîner

Préparation : comme l'étape 2 (serveur sur **http://localhost:8000**, un profil créé).

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 4.1 | Ouvrir le module | Cartes « Apprendre » et « S'entraîner » actives ; les 2 autres grisées. | ☐ |
| 4.2 | « S'entraîner » | Puces « Niveau 1 » à « Niveau 4 » avec sous-titre et nombre de questions (10, 11, 9, 7) ; puces « Tout mélangé » + les 6 compétences ; « Niveau 1 » et « Tout mélangé » surlignées ; bouton « Commencer ». | ☐ |
| 4.3 | Choisir « Connaître le vocabulaire » puis « Niveau 4 » | Le niveau 4 indique « 0 question » ; encadré bleu « Pas de question de ce niveau… », pas de bouton « Commencer ». | ☐ |
| 4.4 | « Poser la division », « Niveau 1 », « Commencer » | Adresse `…/entrainement/1/calcul`. « Niveau 1 : 0 réussie du premier coup sur 0 », « Poser la division », énoncé avec nombres en gras, cases « quotient » et « reste », curseur dans la 1re case (clavier numérique sur téléphone). Boutons « Valider », « Un indice », lien « Revoir la méthode ». | ☐ |
| 4.5 | « Valider » sans rien ; puis « abc » dans une case | « Remplis toutes les cases. » ; « Écris un nombre dans chaque case. » (orange). Le compteur reste « sur 0 ». | ☐ |
| 4.6 | « Un indice » | Encadré orange « **Indice** » + l'indice (table de multiplication). | ☐ |
| 4.7 | Réponse fausse prévue par le module (ex. 23 par 4 : quotient 4, reste 7 ; 17 par 3 : 4 et 5) | Encadré rouge « Pas tout à fait. » + message ciblé (« Ton reste (…) n'est pas plus petit que le diviseur… »). Cases bloquées, boutons « Réessayer » (Entrée), « Un indice », « Voir la correction ». Compteur « 0 réussie … sur 1 ». | ☐ |
| 4.8 | Autre réponse fausse (ex. 1 et 1) sur une nouvelle question | Message générique « Relis bien l'énoncé, puis réessaie… ». | ☐ |
| 4.9 | « Réessayer », bonne réponse | Curseur dans la case, saisie sélectionnée. Puis encadré vert (« Bravo ! », « Exact ! »…) + « Tu as trouvé au deuxième essai. », cases vertes ; le compteur ne change pas (seul le 1er essai compte). Entrée = « Question suivante ». | ☐ |
| 4.10 | Deux fois faux, ou « Voir la correction » | Cases rouges (vertes si juste), encadré bleu « **Correction** », « Bonne réponse : quotient = 5, reste = 2 » puis l'explication. | ☐ |
| 4.11 | Tolérance : répondre « 5 » et « 3 » entourés d'espaces ; question de texte (« Connaître le vocabulaire ») en majuscules sans accent avec « ! » final | Acceptés. | ☐ |
| 4.12 | QCM (« Repérer l'erreur ») : « Valider » sans choix ; choisir une réponse fausse ; « Réessayer » ; la bonne | « Choisis une réponse. » ; choix surligné en bleu ; message ciblé ; à la fin, bon choix en vert (et le choix faux en rouge si correction). | ☐ |
| 4.13 | « Niveau 2 », « Tout mélangé » : 5 bonnes réponses du premier coup d'affilée | « Tu enchaînes 5 réussites du premier coup… » + bouton « Niveau suivant » → `…/entrainement/3`, compteur remis à 0. Une erreur au 1er essai fait disparaître la proposition (série remise à 0). | ☐ |
| 4.14 | Noter les énoncés de 10 questions de suite au niveau 2 (11 questions) | Aucune répétition parmi les 10. Au niveau 1 de « Résoudre un problème » (1 seule question), la même question revient : normal. | ☐ |
| 4.15 | « Revoir la méthode » | Leçon de la compétence de la question (« Revoir : … »). Bouton retour du navigateur → retour à l'entraînement (nouvelle série). | ☐ |
| 4.16 | « ← Retour » pendant l'entraînement | Écran de réglage avec le niveau et la compétence en cours déjà surlignés. « ← Retour » → accueil du module. | ☐ |
| 4.17 | Fin de leçon (3.10) : « Je m'entraîne » | Écran de réglage de l'entraînement. | ☐ |
| 4.18 | Adresses abîmées : `…/entrainement/9`, `…/entrainement/1/inconnu` | Retour au réglage ; « Cette compétence n'existe pas dans ce module. » + « Choisir un autre réglage ». | ☐ |
| 4.19 | Sécurité : copie de test du module (comme 2.9), mettre `"prompt": "<b>23</b> par 4"` dans `q001`, `build_index.py`, l'entraîner (niveau 1, Poser la division) | « <b>23</b> par 4 » s'affiche avec les chevrons. Ensuite : `rm modules/maths-cm2-test.json && python tools/build_index.py`. | ☐ |
| 4.20 | 360 px de large, thème sombre | Puces sur 2 colonnes, cases et boutons sans défilement horizontal ; vert/rouge/bleu lisibles. | ☐ |
| 4.21 | `python -m unittest discover tools/tests -v` | 33 tests, tous « ok ». | ☐ |

Pas encore fait (étape 6) : les réponses ne sont pas enregistrées (recharger la page remet le compteur à 0) et le signalement des questions n'existe pas.

Après la recette : `git status` doit être propre (sinon `git checkout modules/`).
