---
name: nouveau-module
description: Crée un module HTML miniprof (modules/<id>.html) à partir des photos d'une leçon, le contrôle, le publie en brouillon sur GitHub Pages et donne au parent les exemples à relire ; « valide <id> » le rend visible aux enfants. À utiliser quand le parent envoie des photos de leçon ou d'exercices, demande de corriger ou régénérer un module HTML, ou de valider un module.
argument-hint: "[niveau ou consignes, ex. « 6e, surtout les exercices de la page 2 »] + photos, ou « valide <id> »"
---

# /nouveau-module : photos d'une leçon → page de révision publiée

**Si le message est « valide <id> »** (ou « valide » juste après une création dans la même
session) : va directement à la section 7.

Le parent est souvent sur son iPhone : il veut **une URL qui marche** à la fin, pas des
questions. Pose une question seulement si tu ne peux vraiment pas décider (niveau illisible,
photos sans rapport avec une leçon). Réponds en français, court.

## 1. Lire avant d'écrire
- `docs/module-html.md` : le contrat (CSP, fiche, `suivi.js`, appels de suivi, interdits) et les
  **règles pédagogiques**. C'est la référence ; ce skill ne la recopie pas.
- **Photo d'une liste de mots de dictée ? Va à la section « Dictée » plus bas** : autre gabarit
  (`docs/gabarit-dictee.html`), autres règles. Le reste de cette section et les sections 3 à 4
  concernent les autres modules.
- `docs/gabarit-module.html` : la page à copier. Son **moteur** (écrans, entraînement,
  évaluation, suivi) se garde tel quel ; tu n'écris que la partie **CONTENU** (données,
  générateurs, fiches Apprendre, accueil). Ne relis pas les modules existants pour leur moteur :
  garde ton effort pour le contenu. Seule exception : une régénération (voir 2).
- Valeurs permises pour `subject` et `level` : `MATIERES` et `NIVEAUX` en tête de `tools/check_html.py`.
- `modules/index.json` : modules existants (pour l'id).

## 2. Décider la fiche
- **Niveau** : celui que donne le parent, sinon celui de la leçon (en-tête, manuel, programme).
  En 2026-2027, le fils est en CM1 et la fille en 6e (`CLAUDE.md`) : « mon fils » = CM1,
  « ma fille » = 6e, sans redemander.
- **id** : `matiere-niveau-sujet` (minuscules, sans accents, tirets), ex. `maths-cm1-fractions`.
- **Si `modules/<id>.html` existe déjà** : c'est une régénération. Garde le même id **et tous
  les ids de compétences existants** (l'historique des enfants y est rattaché) ; tu peux en
  ajouter. Ne crée pas un deuxième id pour la même leçon. Pour une simple correction, modifie la
  page existante (lis seulement les parties concernées) ; s'il lui manque la ligne
  `window.__miniprofTirage` de la fin du gabarit, ajoute-la pour pouvoir lancer le tirage.
- 2 à 8 compétences, tirées de la leçon.
- **Brouillon** : un **nouveau** module (id absent de `modules/index.json`) est publié en
  brouillon : ajoute son id à la liste de `modules/brouillons.json`. Il est caché dans la
  bibliothèque des enfants tant que le parent ne l'a pas relu et validé (section 7) ; son URL
  marche, pour que le parent l'essaie. Pourquoi : une réponse fausse apprise par un enfant est
  le risque principal du projet (décidé par le sponsor le 6 oct. 2026). Une correction
  d'un module déjà validé ne le remet pas en brouillon (l'enfant s'en sert déjà).

## 3. Écrire `modules/<id>.html`
Pars du gabarit : `cp docs/gabarit-module.html modules/<id>.html`, puis remplace la partie CONTENU.

**Le contenu est le cœur du travail** : c'est lui qui fait progresser l'enfant. Avant d'écrire,
liste pour toi les notions et les exercices des photos, puis les erreurs que font souvent les
élèves de ce niveau sur ces notions. Chaque niveau de difficulté vise un piège précis, et chaque
mauvais choix a son « pourquoi » qui corrige cette erreur-là.

**Écrire plutôt que choisir** (décision D15) : pour l'orthographe, la conjugaison, la dictée
(tout ce que l'enfant devra écrire sur sa copie), fais des questions **à écrire** avec `W()` du
gabarit : réponses acceptées, et fautes prévues avec leur pourquoi (homophones : son / sont,
on / ont, a / à, et / est…). Garde le choix (`Q()`) pour reconnaître une notion (nature d'un
mot, série ou dérivation…). Retour d'usage : un module de dictée tout en choix n'a pas corrigé
« son » au lieu de « sont ».

Respecte `docs/module-html.md` (contrat + règles pédagogiques + pièges). En bref : une seule page,
tout dedans (CSS, JS, SVG), polices système, aucune URL externe, aucun accès au stockage, suivi
uniquement par `window.miniprof`, et la page doit marcher sans miniprof.

**Vérifie chaque réponse attendue** : refais chaque calcul, relis chaque générateur aléatoire
pour qu'il ne puisse pas produire une question fausse ou ambiguë (deux bonnes réponses, choix en
double, division qui ne tombe pas juste…).

**Photos** : elles restent dans la conversation. Ne les enregistre jamais dans le dépôt (dépôt
public, cahiers des enfants). Aucun prénom réel dans la page.

## Dictée : liste de mots → un seul parcours (décision du sponsor, 15 nov. 2026, simplifiée le 17)
Une dictée n'est **pas** un module à leçon, entraînement et évaluation : c'est **un seul
parcours, écrire les mots**, sur le modèle de `modules/francais-cm1-dictee-7-sans-famille.html`.
Règles complètes et pourquoi : `docs/module-html.md`, « Dictées ».
1. **Une devinette, l'enfant écrit le mot sans aide.** Pas de QCM (supprimé le 17 nov. : inutile).
2. **Une question par mot** : tous les mots à savoir sont posés, aucun tirage au sort.
3. **Une bonne réponse enchaîne tout de suite**, sans message. Une faute montre la correction.
4. **Passes invisibles** : l'enfant ne voit qu'une jauge des mots acquis et un compteur qui
   monte à chaque bonne réponse. Un mot raté revient 4
   questions plus tard ; à la fin, les mots ratés sont reposés une dernière fois, jusqu'à une
   vérification sans faute ; puis le bilan. Un mot réussi du premier coup n'est jamais reposé. Pas de
   leçon, pas de niveaux, pas d'évaluation. (Tout est dans le moteur du gabarit.)
5. Pars de `docs/gabarit-dictee.html` (`cp docs/gabarit-dictee.html modules/<id>.html`) ; tu ne
   remplis que la fiche et les données (un objet par mot : `id`, `m`, `det` pour un nom, `dev`,
   `tip`, `faux`, `ex` pour un adjectif). Le moteur ne se modifie pas. Compétences : `noms`,
   `verbes`, `mots` (une famille vide se retire).
6. **Une devinette ne doit avoir qu'une réponse possible**, adjectifs et pluriels compris : un
   adjectif est donné avec son nom (`ex`), un nom ou un verbe fixe son nombre et sa forme
   (« écris le mot au singulier », « à l'infinitif »). Prévois dans `faux` les synonymes que
   l'enfant tapera (« vêtir » pour habiller, « heureux » pour joyeux) avec leur pourquoi.
   Les `faux` ne sont jamais montrés comme des choix.
7. **Couverture** : relis la liste des photos et lance
   `python tools/couverture_dictee.py modules/<id>.html "mot1,mot2,…"` : elle doit répondre que
   tous les mots sont couverts. Les mots que la feuille met à part (« à 3 étoiles », facultatifs)
   restent hors module, dis-le au parent.
8. Contrôles de la section 4 (`check_html.py`, `tirage.py`, tests) ; au tirage, les exemples
   à relire sont la fiche de contrôle du parent. Publication et validation : sections 5 à 7
   (nouvel id = brouillon ; ou, pour **refaire une dictée existante**, même id, mêmes
   compétences, sans brouillon si le parent l'a essayée avant).
9. Réponse au parent : nombre de mots, devinettes ambiguës possibles, mots laissés de côté.

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
git add modules/<id>.html modules/index.json modules/brouillons.json
git commit -m "Module : <titre> (<niveau>)"
git push
```
- Une session module n'a pas de fiche de plan : le commit suffit. Le module à valider se voit
  dans `modules/brouillons.json`, que Claude lit en début de session.
- Ne committe que ces fichiers (jamais de photo, d'export, de fichier de travail).
- Si la session travaille sur une branche (session web ou mobile) : pousse la branche, ouvre une
  PR vers `main` si tu le peux (`gh pr create`), sinon donne le lien
  `https://github.com/ghpz5649xx-blip/miniprof/compare/main...<branche>`. Dis au parent que
  **l'URL ne marchera qu'après la fusion** (depuis l'app GitHub : « Merge pull request »).

## 6. Répondre au parent
Un message court (le parent lit sur son iPhone) :
- l'URL : `https://ghpz5649xx-blip.github.io/miniprof/modules/<id>.html` (en ligne environ une
  minute après le push sur `main`), et le rappel : **module en brouillon, ne pas envoyer l'URL à
  l'enfant avant de l'avoir validé** ;
- ce que contient la page : compétences, niveaux, nombre de types de questions ;
- ce que tu n'as pas pu reprendre des photos (illisible, hors sujet) ;
- **à relire** :
  - 2 ou 3 points précis où tu as pu te tromper (une réponse calculée, une notion interprétée) ;
  - **une question par compétence et par niveau, avec sa bonne réponse**, recopiée des exemples
    de `tirage.py` (`--exemples 1`), sous la forme « question → réponse » : c'est la fiche de
    contrôle, produite par le vrai code de la page ;
- la suite : « Si tout est juste, réponds **valide** ; sinon, dis-moi ce qui ne va pas. »

Si le parent signale une erreur ensuite : corrige ou régénère la page avec le **même id** et les
mêmes compétences, refais les contrôles et republie.

## 7. Valider un module (« valide <id> »)
1. Retire l'id de la liste de `modules/brouillons.json` (s'il n'y est pas, dis-le au parent et
   arrête-toi).
2. `python tools/build_index.py` (le module n'a plus `"brouillon": true`), puis
   `python -m unittest discover tools/tests`.
3. Publie :
   ```bash
   git add modules/brouillons.json modules/index.json
   git commit -m "Validation : <titre> (<niveau>)"
   git push
   ```
4. Réponds en une ligne : le module apparaît dans la bibliothèque des enfants d'ici une minute,
   et l'URL peut être envoyée à l'enfant.
