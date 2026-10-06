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
| 2.3 | Taper « Léa », touche Entrée ; « Changer de profil » ; puis « Tom », clic sur OK ; « Changer de profil » | Après chaque création, on arrive directement dans la bibliothèque du profil créé (« Bonjour Léa ! », puis « Bonjour Tom ! ») : pas besoin de retoucher son prénom (depuis le 6 octobre 2026). Au retour : deux gros boutons « Léa » et « Tom », le texte devient « Qui es-tu ? ». | ☐ |
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
| 4.1 | Ouvrir le module | Cartes « Apprendre » et « S'entraîner » actives (depuis l'étape 5 : « Évaluation » aussi) ; « Bilan » grisée. | ☐ |
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

Depuis l'étape 6 : le premier essai est enregistré et « Cette question me semble fausse » apparaît après la correction (voir étape 6).

Après la recette : `git status` doit être propre (sinon `git checkout modules/`).

## Étape 5 — Évaluation

Préparation : comme l'étape 2 (serveur sur **http://localhost:8000**, un profil créé).

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 5.1 | Ouvrir le module | Cartes « Apprendre », « S'entraîner », « Évaluation » actives ; « Bilan » grisée « Bientôt (étape 6) » (depuis l'étape 6 : active). | ☐ |
| 5.2 | « Évaluation » | Encadré « Prête ou prêt pour l'évaluation ? 10 questions, sans indice… ». Puces « Mixte » (surlignée), « Niveau 1 » à « Niveau 4 » avec le nombre de questions (10, 10, 10, 9, 7). Bouton « Lancer l'évaluation » (Entrée). | ☐ |
| 5.3 | « Mixte », « Lancer l'évaluation » | Adresse `…/evaluation/mixte`. 10 pastilles (la 1re en cours), « Question 1 sur 10 », pas de bouton « Un indice » ni « Revoir la méthode ». Bouton « Valider et continuer ». | ☐ |
| 5.4 | « Valider et continuer » sans rien ; puis « abc » | « Remplis toutes les cases. » / « Écris un nombre dans chaque case. » (orange), on reste sur la question. QCM sans choix : « Choisis une réponse. » | ☐ |
| 5.5 | Répondre aux 10 questions (certaines fausses), Entrée dans une case = valider | Aucune correction pendant l'évaluation ; les pastilles se remplissent. Les questions vont du facile au difficile (niveaux 2, 2, 2, 3, 3, 3, 3, 4, 4, 4) et couvrent les 6 compétences (1 ou 2 questions chacune). Dernière question : « Valider et terminer ». | ☐ |
| 5.6 | Résultat | Grande note « n / 10 », message selon la note, « Temps : … min … s ». « Par compétence » : une barre par compétence (rouge < 50 %, orange < 80 %, vert sinon) et « x/y ». | ☐ |
| 5.7 | « Les corrections » | Une ligne « ✓/✗ n. compétence » par question ; un clic la déplie : énoncé, « Ta réponse », « Bonne réponse » (si faux), explication. | ☐ |
| 5.8 | « Travailler : <compétence> » | Entraînement de la compétence la plus faible, au niveau d'une question ratée (pas d'écran vide). | ☐ |
| 5.9 | Retour à l'évaluation : « Recommencer » ; puis « Accueil » | Nouvelle évaluation (« Question 1 sur 10 », autre tirage) ; « Accueil » → accueil du module. Avec 10/10 : pas de bouton « Travailler ». | ☐ |
| 5.10 | « Niveau 4 » | « Question 1 sur 7 » : seulement des questions de niveau 4, note sur 7. | ☐ |
| 5.11 | Pendant l'évaluation : « ← Retour », puis relancer et bouton retour du navigateur | Les deux abandonnent et ramènent au réglage, niveau en cours surligné. Recharger (F5) pendant l'évaluation : nouvelle évaluation. | ☐ |
| 5.12 | Adresses abîmées : `…/evaluation/9`, `…/evaluation/abc` | Retour au réglage. | ☐ |
| 5.13 | Sécurité : copie de test du module (comme 2.9), mettre `"prompt": "<b>23</b> par 4"` dans `q001` et `"difficulty": 2`, `build_index.py`, faire des évaluations mixtes jusqu'à la tomber | « <b>23</b> par 4 » s'affiche avec les chevrons, dans la question et dans sa correction. Ensuite : `rm modules/maths-cm2-test.json && python tools/build_index.py`. | ☐ |
| 5.14 | 360 px de large, thème sombre | Pastilles, cases, barres et corrections sans défilement horizontal ; couleurs lisibles. | ☐ |
| 5.15 | `python -m unittest discover tools/tests -v` | 33 tests, tous « ok ». | ☐ |

Depuis l'étape 6 : l'évaluation est enregistrée à la fin, et les questions signalées sont écartées (voir étape 6).

Après la recette : `git status` doit être propre (sinon `git checkout modules/`).

## Étape 6 — Enregistrement, signalement, bilan

Préparation : comme l'étape 2 (serveur sur **http://localhost:8000**, fenêtre de navigation
privée, deux profils « Léa » et « Tom »). Pour voir le stockage : outils de développement
(Cmd+Option+I) > Application > Local Storage > `http://localhost:8000`.

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 6.1 | `python tools/build_index.py` | `modules/index.json` contient pour le module une liste `skills` (id + libellé). `git status` propre (déjà commité). | ☐ |
| 6.2 | Léa : ouvrir le module | Les 4 cartes sont actives (« Bilan » aussi) ; pas encore de « Dernière note ». | ☐ |
| 6.3 | « S'entraîner », niveau 1, « Poser la division » : une réponse juste, puis une fausse suivie de « Réessayer » et d'une juste | Clé `miniprof.v1.events.<id de Léa>` : 2 lignes seulement (1er essai), la 2e avec `0` (faux), mode `"e"`, la réponse tapée (`{"q":…,"r":…}`). Recharger la page : les lignes restent. | ☐ |
| 6.4 | Après une correction : « Cette question me semble fausse » | Le bouton devient « Merci ! Cette question ne te sera plus posée… ». Clé `miniprof.v1.flags` : une ligne `[module, id de question, date, id de Léa]`. | ☐ |
| 6.5 | « ← Retour » au réglage | Le nombre de questions du niveau de la question signalée a baissé de 1. Une compétence dont toutes les questions d'un niveau sont signalées affiche « 0 question ». | ☐ |
| 6.6 | Faire une évaluation « Mixte » jusqu'au bout | 10 lignes de plus, mode `"v"`, toutes avec la même clé `"<nombre>/mixte"` ; la question signalée n'est jamais posée. Dans chaque correction dépliée : « Cette question me semble fausse ». | ☐ |
| 6.7 | Évaluation abandonnée (← Retour à la question 3) | Aucune ligne ajoutée. | ☐ |
| 6.8 | Accueil du module | Badge « Dernière note : n / 10 » sous « Évaluation ». En bas, « Questions signalées (1) » : dépliée, l'id, l'énoncé et « Rétablir ». | ☐ |
| 6.9 | « Rétablir » | Le bloc disparaît ; la question revient dans les tirages (compteur du réglage rétabli). | ☐ |
| 6.10 | Carte « Bilan » | « Bilan de Léa », « N questions traitées, dont M réussies du premier coup (P %) » ; « À travailler » (compétences < 60 %) ; « Réussite par compétence » : une barre + « P % · x/y » par compétence travaillée, « pas encore travaillé » sinon ; « Dernières évaluations » : date, « Mixte », note. Mention « Les résultats sont enregistrés dans le navigateur de cet appareil. » ; ← Retour → accueil du module. | ☐ |
| 6.11 | « Travailler ce point » | Entraînement de cette compétence, au niveau du dernier essai raté. | ☐ |
| 6.12 | Bibliothèque : carte « Mon bilan » | Même bilan, tous modules : le titre du module sous chaque point à travailler et chaque évaluation ; ← Retour → bibliothèque. | ☐ |
| 6.13 | Changer de profil : Tom, « Mon bilan » | « Pas encore de résultat… » : Tom ne voit pas les résultats de Léa. La question signalée par Léa n'est pas posée à Tom non plus (signalements communs à l'appareil). | ☐ |
| 6.14 | « En baisse » : dans la console, `localStorage.setItem("miniprof.v1.events.<id de Tom>", JSON.stringify(Array.from({length:25}, (_, i) => [1791000000+i, "maths-cm2-division-euclidienne", "q001", "calcul", 2, "e", (i < 15 \|\| i % 2) ? 1 : 0, 5, {q:1,r:1}, null])))` puis recharger le bilan de Tom | « Poser la division » : « 80 % de réussite, en baisse » dans « À travailler » (100 % sur les 15 premiers essais, 50 % sur les 10 derniers). | ☐ |
| 6.15 | Stockage plein simulé : dans la console `Storage.prototype.setItem = () => { throw new Error("plein") }`, puis répondre à une question d'entraînement | Encadré rouge « Sauvegarde impossible sur cet appareil… ». Recharger la page pour revenir à la normale. | ☐ |
| 6.16 | « Gérer les profils » : supprimer Tom (deux clics) | La clé `miniprof.v1.events.<id de Tom>` disparaît. | ☐ |
| 6.17 | 360 px de large, thème sombre | Bilan, signalées et badge sans défilement horizontal ; barres lisibles. | ☐ |
| 6.18 | `python -m unittest discover tools/tests -v` | 33 tests, tous « ok ». | ☐ |


## Étape 7 — Sauvegarde, aperçu, prompt, fusion, analyse

Préparation : `source .venv/bin/activate && pip install -r tools/requirements.txt` (ajoute
pandas et matplotlib), serveur sur **http://localhost:8000**, fenêtre de navigation privée.

### Côté app

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 7.1 | Premier lancement (aucun profil) | Sous le formulaire, lien « Sauvegarder ou restaurer les données ». | ☐ |
| 7.2 | Ce lien | Écran « Sauvegarde » : « Dernier export : jamais · stockage utilisé : 0 % », bouton « Exporter mes données », bloc « Restaurer une sauvegarde » avec un champ fichier. « ← Retour » → choix du profil. | ☐ |
| 7.3 | Restaurer : choisir `tools/tests/fixtures/export.json` | Encadré bleu : « Sauvegarde du … », « Léa : 34 réponse(s) », « Tom : 1 réponse(s) », « 1 question(s) signalée(s) » ; encadré orange « …seront **remplacées** » ; boutons « Confirmer : remplacer les données » (rouge) et « Annuler ». Rien n'a encore changé. | ☐ |
| 7.4 | « Annuler », puis rechoisir le fichier et « Confirmer » | Annuler : retour au champ fichier. Confirmer : « Sauvegarde restaurée. » ; ← Retour : profils Léa et Tom. | ☐ |
| 7.5 | Léa > « Mon bilan » | 34 questions traitées ; « Poser la division » 81 % en baisse ; « Retrouver le dividende » 33 %. (Mêmes chiffres que 7.16.) | ☐ |
| 7.6 | Restaurer un mauvais fichier : `modules/index.json`, puis un fichier texte quelconque renommé en `.json` | « Ce fichier n'est pas une sauvegarde miniprof. » ; « Le fichier « … » n'est pas un JSON valide… ». Données intactes. | ☐ |
| 7.7 | Bibliothèque de Léa | Encadré orange « Pas de sauvegarde depuis N jours… » : la fixture date de septembre 2026 (le rappel repart de la date de la sauvegarde restaurée). | ☐ |
| 7.8 | Rappel 14 jours : console `localStorage.setItem("miniprof.v1.last_export", String(Math.round(Date.now()/1000) - 20*86400))`, recharger | Encadré orange « Pas de sauvegarde depuis 20 jours… » + lien « Sauvegarder ». | ☐ |
| 7.9 | « Sauvegarder » > « Exporter mes données » | Le navigateur télécharge `miniprof-AAAA-MM-JJ.export.json` (ou demande où l'enregistrer) ; « Fichier téléchargé… » ; « Dernier export : <aujourd'hui> ». Bibliothèque : plus de rappel. Ouvrir le fichier : `"format": "miniprof-sauvegarde"`. | ☐ |
| 7.10 | Rappel quota : console `localStorage.setItem("miniprof.v1.gros", "x".repeat(3600000))`, recharger la bibliothèque | « Le stockage de cet appareil est presque plein… » ; l'écran Sauvegarde indique ≈ 72 %. Ensuite : `localStorage.removeItem("miniprof.v1.gros")`. | ☐ |
| 7.11 | Restaurer sur un autre navigateur (ou après avoir vidé les données du site) le fichier de 7.9 | Mêmes profils, mêmes bilans, même question signalée. | ☐ |
| 7.12 | Aperçu : bibliothèque > « Pour les parents : aperçu d'un module » > choisir `tools/tests/fixtures/minimal.json` | Adresse `#/module/_apercu` ; bandeau orange en pointillés « Aperçu — non enregistré » ; « Module minimal de test », « CM1 · 3 questions ». | ☐ |
| 7.13 | Dans l'aperçu : leçon, entraînement (réponses justes et fausses, « Cette question me semble fausse »), évaluation | Tout fonctionne, bandeau sur chaque écran. Dans Application > Local Storage : `events.<id>` et `flags` **inchangés**. Le bilan ne montre rien de l'aperçu. | ☐ |
| 7.14 | Recharger la page (F5) dans l'aperçu | « Aperçu perdu (la page a été rechargée)… » + « Retour à la bibliothèque ». | ☐ |
| 7.15 | Aperçu d'un fichier cassé (`tools/tests/fixtures/entoure.txt` copié en `.json`) | Sous le champ : « Le fichier « … » n'est pas un JSON valide : lance validate.py dessus. » | ☐ |
| 7.16 | 360 px de large, thème sombre ; onglet Réseau pendant export, restauration et aperçu | Rien ne déborde ; aucune requête réseau pour lire les fichiers choisis (lecture locale). | ☐ |

### Côté outils

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 7.17 | `python tools/prompt.py --mode nouveau` | « ✔ Prompt écrit dans docs/prompt-nouveau.md », « Copié dans le presse-papiers ». Le fichier contient la tâche, les règles (dont « VÉRIFIE CHAQUE CALCUL »), le schéma, un exemple court. | ☐ |
| 7.18 | `python tools/prompt.py --mode lot modules/maths-cm2-division-euclidienne.json` | `docs/prompt-lot-maths-cm2-division-euclidienne.md` (ignoré par Git) : « à partir de q038 », les 6 compétences, la répartition, les 37 énoncés existants. Sans fichier : message d'usage. | ☐ |
| 7.19 | `cp tools/tests/fixtures/minimal.json /tmp/minimal.json && python tools/merge.py /tmp/minimal.json tools/tests/fixtures/lot.json` | « Questions ajoutées : 2 », « remplacées (même id) : q2 », « doublon(s) probable(s) : q1 ≈ q5 », « ✔ VALIDE », « ✔ Module réécrit … (version 2) ». Code retour 0. | ☐ |
| 7.20 | Lot invalide : dans une copie de `lot.json`, mettre `"skill": "inconnu"` dans `q4`, relancer sur une nouvelle copie de `minimal.json` | « ✘ INVALIDE », erreur sur la compétence, « Module NON modifié » + texte à renvoyer au LLM. Code retour 1, fichier inchangé. `--essai` sur un lot valide : rien n'est écrit. | ☐ |
| 7.21 | `python tools/analyse.py tools/tests/fixtures/export.json` | Par enfant : tableau par compétence (Léa : calcul 81 %, en baisse), « À travailler », questions les plus ratées (q015 en tête), évaluations (2/3 mixte). « ✔ 5 graphique(s) dans exports/analyse/ » ; PNG lisibles. `git status` : rien sous `exports/`. | ☐ |
| 7.22 | `python tools/analyse.py` sur l'export de 7.9 | Mêmes chiffres que le bilan de l'app. | ☐ |
| 7.23 | `python -m unittest discover tools/tests -v` | 49 tests, tous « ok ». | ☐ |

Après la recette : `git status` doit être propre (sinon `git checkout modules/`).

## Étapes 8 et 9 — Modules HTML : contrat de suivi et module circuit

### Automatique (fait par Claude Code avant chaque push)

| # | Commande | Résultat attendu | OK |
|---|---|---|---|
| 8.1 | `python -m unittest discover tools/tests -v` | 61 tests « ok » : `test_check_html` (page valide, chaque interdit refusé, CSP, fiche), `test_build_index` (module HTML indexé avec `"kind": "html"`, page cassée écartée), `test_sync` (`suivi.js` passe par `addEvents`). | ☑ |
| 8.2 | `python tools/check_html.py modules/*.html` | « ✔ modules/sciences-6e-circuit-electrique.html : conforme au contrat ». | ☑ |
| 8.3 | `python tools/build_index.py` | 3 modules, dont « sciences-6e-circuit-electrique.html (6e, page HTML) ». | ☑ |
| 8.4 | `python tools/recette_navigateur.py` | « ✔ 24 OK, 0 échec(s) ». Elle vérifie : `window.miniprof` chargé ; `fetch` bloqué par la CSP ; bandeau « Tu es Léa » ; 6 réponses d'entraînement puis une évaluation de 10, au format du journal, avec une clé commune ; « Mon bilan » ouvre `#/module/<id>/bilan` (16 questions, libellés lus dans l'index, évaluation « Niveau 2 ») ; « Retour » et « Travailler ce point » ramènent à la page ; la bibliothèque montre le module HTML et les modules JSON ; le bilan général montre le titre ; sans profil, bandeau « Choisis ton profil » et rien n'est enregistré. | ☑ |

### Sur l'iPhone (parent)

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 8.5 | https://ghpz5649xx-blip.github.io/miniprof/ : choisir un profil, puis la carte « Le circuit électrique » (rubrique Sciences) | La page circuit s'ouvre, avec un bandeau bleu « Tu es <prénom> · changer · mon bilan · mes modules ». Polices système : le titre n'est plus en Baloo. | ☐ |
| 8.6 | Apprendre, labo, quelques questions d'entraînement, une évaluation | Tout fonctionne comme la page d'origine : schémas, labo interactif, corrections. | ☐ |
| 8.7 | « Mon bilan » | Bilan miniprof du module : les compétences travaillées et l'évaluation. « ← Retour » ramène à la page circuit. | ☐ |
| 8.8 | Envoyer l'URL de la page (`…/modules/sciences-6e-circuit-electrique.html`) par SMS et l'ouvrir sur le téléphone de l'enfant | Sans profil sur ce téléphone : bandeau « Choisis ton profil… ». Après le choix, les réponses comptent. | ☐ |

## Étape 10 — Créer un module depuis l'iPhone (skill `/nouveau-module`)

### Automatique (fait par Claude Code avant le push)

| # | Commande | Résultat attendu | OK |
|---|---|---|---|
| 10.1 | `python -m unittest discover tools/tests -v` | 62 tests « ok », dont `test_skill_nouveau_module` (le skill lance les trois contrôles, les fichiers cités par le skill et `docs/parent-iphone.md` existent). | ☑ |
| 10.2 | `python tools/check_html.py modules/*.html` ; `python tools/build_index.py` ; `python tools/recette_navigateur.py` ; contrôle de syntaxe du skill (`node --check`) sur le module circuit | Conforme ; 3 modules ; « ✔ 24 OK, 0 échec(s) » ; `node --check` sans erreur. | ☑ |
| 10.2b | Retours de la session iPhone : `test_json_casse` sous Python 3.11 et 3.14 ; `CHROME=/usr/bin/false python tools/recette_navigateur.py` | Le test accepte « ligne 3 » (3.13+) ou « ligne 4 » ; la recette affiche « ✘ Chrome s'est arrêté sans finir la recette » au lieu de « Aucun résultat reçu », code 1. Recette normale toujours « ✔ 24 OK ». | ☑ |

### Sur l'iPhone (parent), en suivant `docs/parent-iphone.md`

| # | Scénario | Résultat attendu | OK |
|---|---|---|---|
| 10.3 | App Claude, onglet Code : nouvelle session sur `miniprof` (`main`, environnement « Default »), taper `/nouveau-module …` en entier et envoyer | Le skill se lance (pas d'autocomplétion au premier message : normal, le dépôt n'est pas encore copié). | ☑ |
| 10.4 | Joindre 2 à 4 photos d'une vraie leçon + `/nouveau-module <niveau>` | Claude Code lit le contrat, écrit `modules/<id>.html`, lance `check_html.py`, `build_index.py` et les tests (tous verts), commit et push. Aucune photo dans le commit. | ☑ (module anglais 6e Zootopia : commit de 2 fichiers ; contrôles refaits sur le Mac : conforme, index à jour, `node --check` OK, tests OK) |
| 10.5 | Où le push arrive | Sur `main` : rien à faire. Sur une branche `claude/…` : lien de PR, fusion depuis l'app GitHub. **Noter le cas constaté dans `docs/parent-iphone.md`.** | ☑ directement sur `main` |
| 10.6 | Une minute après, ouvrir l'URL donnée | La page s'ouvre (pas de page blanche), bandeau « Tu es … », polices système ; la leçon et les exercices reprennent les photos, avec le vocabulaire du cahier. Relire les 2 ou 3 points signalés. | ☑ ouverte et utilisée sans souci sur l'iPhone 8 de l'enfant (6 octobre 2026, voir ci-dessous) |
| 10.7 | Signaler une erreur dans la session (« la question … attend … ») | Correction republiée à la **même URL**, même id. | ☐ |
| 10.8 | URL par SMS au téléphone de l'enfant ; quelques réponses et une évaluation ; puis miniprof → profil → « Mon bilan » | Le nouveau module apparaît dans la bibliothèque et dans le bilan, avec ses compétences et l'évaluation. | ☑ d'après l'export : les réponses et les 9 évaluations du module sont dans le profil, avec ses 6 compétences |

### Première utilisation par un enfant (6 octobre 2026)

L'enfant de 6e s'est entraînée seule sur son iPhone 8, une demi-heure. Son export a été déposé
dans `exports/` (ignoré par Git : il contient son prénom, il ne doit pas partir sur le dépôt
public) et lu avec `python tools/analyse.py exports/<fichier>.export.json`.

| Constat | Détail |
|---|---|
| L'app marche sur un iPhone 8 | Profil créé, module HTML et module JSON joués, évaluations enregistrées, export fait : aucun blocage technique. |
| Volume | 144 réponses : `anglais-6e-zootopia-animaux` (37 en entraînement, 9 évaluations de 10, notes de 6 à 9/10, en progrès) ; `maths-cm2-grands-nombres` (7 en entraînement, 1 évaluation, 5/10). Aucune question signalée. |
| Point à travailler (anglais) | « Décrire un animal » : 43 % de réussite au premier coup. Erreurs surtout sur l'article devant l'adjectif (`art` : « an pink… » / « a orange… »), puis l'ordre adjectif-nom (`ordre`) et le verbe oublié (`is`). Difficulté réelle de la leçon, pas un défaut du module. |
| Retour de l'enfant | Après avoir créé son profil, elle n'a pas compris qu'il fallait encore toucher son prénom. **Corrigé** : la création ouvre directement la bibliothèque du profil (`js/screens/profiles.js`) ; scénario 2.3 mis à jour. |

| # | Vérification | Résultat attendu | OK |
|---|---|---|---|
| 11.1 | `python tools/recette_navigateur.py` | « ✔ 27 OK, 0 échec(s) » : 3 vérifications de plus (profil en double : erreur et saisie gardée ; profil créé devenu le profil courant ; arrivée sur `#/biblio`, « Bonjour Tom »). Sans la correction, les 2 dernières échouent. | ☑ |
| 11.2 | `python -m unittest discover tools/tests -v` | 62 tests « ok ». | ☑ |
| 11.3 | Sur l'iPhone, après le push : « Gérer les profils » pour supprimer un profil de test si besoin, puis créer un profil | On arrive directement sur « Bonjour <prénom> ! ». | ☑ (iPhone, 6 octobre 2026) |
