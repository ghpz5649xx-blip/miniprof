---
name: nouveau-module
description: Crée un module HTML miniprof (modules/<id>.html) à partir des photos d'une leçon, le contrôle, le publie sur GitHub Pages et donne l'URL à envoyer à l'enfant. À utiliser quand le parent envoie des photos de leçon ou d'exercices, ou demande de régénérer un module HTML.
argument-hint: "[niveau ou consignes, ex. « 6e, surtout les exercices de la page 2 »] + photos"
---

# /nouveau-module : photos d'une leçon → page de révision publiée

Le parent est souvent sur son iPhone : il veut **une URL qui marche** à la fin, pas des
questions. Pose une question seulement si tu ne peux vraiment pas décider (niveau illisible,
photos sans rapport avec une leçon). Réponds en français, court.

## 1. Lire avant d'écrire
- `docs/module-html.md` : le contrat (CSP, fiche, `suivi.js`, appels de suivi, interdits) et les
  **règles pédagogiques**. C'est la référence ; ce skill ne la recopie pas.
- `docs/gabarit-module.html` : la page à copier. Son **moteur** (écrans, entraînement,
  évaluation, suivi) se garde tel quel ; tu n'écris que la partie **CONTENU** (données,
  générateurs, fiches Apprendre, accueil). Ne relis pas les modules existants pour leur moteur :
  garde ton effort pour le contenu. Seule exception : une régénération (voir 2).
- `schema/module.schema.json` : valeurs permises pour `subject` et `level`.
- `modules/index.json` : modules existants (pour l'id).

## 2. Décider la fiche
- **Niveau** : celui que donne le parent, sinon celui de la leçon (en-tête, manuel, programme).
  Les enfants sont en CE2/CM1 et en 6e/5e.
- **id** : `matiere-niveau-sujet` (minuscules, sans accents, tirets), ex. `maths-cm1-fractions`.
- **Si `modules/<id>.html` existe déjà** : c'est une régénération. Garde le même id **et tous
  les ids de compétences existants** (l'historique des enfants y est rattaché) ; tu peux en
  ajouter. Ne crée pas un deuxième id pour la même leçon. Pour une simple correction, modifie la
  page existante (lis seulement les parties concernées) ; s'il lui manque la ligne
  `window.__miniprofTirage` de la fin du gabarit, ajoute-la pour pouvoir lancer le tirage.
- 2 à 8 compétences, tirées de la leçon.

## 3. Écrire `modules/<id>.html`
Pars du gabarit : `cp docs/gabarit-module.html modules/<id>.html`, puis remplace la partie CONTENU.

**Le contenu est le cœur du travail** : c'est lui qui fait progresser l'enfant. Avant d'écrire,
liste pour toi les notions et les exercices des photos, puis les erreurs que font souvent les
élèves de ce niveau sur ces notions. Chaque niveau de difficulté vise un piège précis, et chaque
mauvais choix a son « pourquoi » qui corrige cette erreur-là.

Respecte `docs/module-html.md` (contrat + règles pédagogiques + pièges). En bref : une seule page,
tout dedans (CSS, JS, SVG), polices système, aucune URL externe, aucun accès au stockage, suivi
uniquement par `window.miniprof`, et la page doit marcher sans miniprof.

**Vérifie chaque réponse attendue** : refais chaque calcul, relis chaque générateur aléatoire
pour qu'il ne puisse pas produire une question fausse ou ambiguë (deux bonnes réponses, choix en
double, division qui ne tombe pas juste…).

**Photos** : elles restent dans la conversation. Ne les enregistre jamais dans le dépôt (dépôt
public, cahiers des enfants). Aucun prénom réel dans la page.

## 4. Contrôler (tout doit passer avant le commit)
```bash
python tools/check_html.py --llm modules/<id>.html    # corriger jusqu'à « conforme au contrat »
python tools/build_index.py                            # le module doit apparaître dans la liste
python -m unittest discover tools/tests                # tous les tests passent
```
- `python` introuvable : utiliser `python3`. `ModuleNotFoundError` (session dans le cloud,
  sans `.venv`) : `pip install -r tools/requirements.txt`, puis relancer. En local :
  `source .venv/bin/activate`.
- **Tirage** (si `node` est disponible) : `python tools/tirage.py modules/<id>.html` fait tourner
  les vrais générateurs (2000 questions par compétence et niveau). Il voit une erreur de syntaxe
  (page blanche sur l'iPhone), deux bonnes réponses, un choix en double, un « undefined ».
  Corrige jusqu'à « aucune erreur de forme », puis **lis les exemples affichés comme le ferait
  l'enfant** : l'outil ne voit pas une réponse fausse sur le fond (un calcul faux, une traduction
  discutable). Sans `node`, dis-le au parent : il relira plus d'exemples.
- `python tools/recette_navigateur.py` teste l'app (non-régression), pas le nouveau module : la
  lancer si un navigateur est disponible, sinon le dire au parent (elle sera relancée en local).
  Si tu as un navigateur, ouvre plutôt la nouvelle page et fais une question par compétence.
- Un test **sans rapport avec le module** qui échouait déjà avant ton travail (vérifie avec
  `git stash`) ne bloque pas la publication : publie, et signale-le au parent en une ligne.

Si un contrôle échoue et que tu ne trouves pas pourquoi après deux essais, **ne pousse pas** :
explique au parent ce qui bloque.

## 5. Publier
```bash
git add modules/<id>.html modules/index.json
git commit -m "Module : <titre> (<niveau>)"
git push
```
- Ne committe que ces deux fichiers (jamais de photo, d'export, de fichier de travail).
- Si la session travaille sur une branche (session web ou mobile) : pousse la branche, ouvre une
  PR vers `main` si tu le peux (`gh pr create`), sinon donne le lien
  `https://github.com/ghpz5649xx-blip/miniprof/compare/main...<branche>`. Dis au parent que
  **l'URL ne marchera qu'après la fusion** (depuis l'app GitHub : « Merge pull request »).

## 6. Répondre au parent
Un message court :
- l'URL : `https://ghpz5649xx-blip.github.io/miniprof/modules/<id>.html` (en ligne environ une
  minute après le push sur `main`) ;
- ce que contient la page : compétences, niveaux, nombre de types de questions ;
- ce que tu n'as pas pu reprendre des photos (illisible, hors sujet) ;
- **à relire avant d'envoyer l'URL** à l'enfant : 2 ou 3 points précis où tu as pu te tromper
  (une réponse calculée, une notion interprétée).

Si le parent signale une erreur ensuite : corrige ou régénère la page avec le **même id** et les
mêmes compétences, refais les contrôles et republie.
