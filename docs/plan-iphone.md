# Créer un module depuis l'iPhone (copier-coller avec un LLM, sans API)

## Contexte
Aujourd'hui, créer un module oblige à passer par l'ordinateur (prompt.py, validate.py, build_index,
commit), et le format vise 100 à 200 questions, impossibles à relire. Objectif : tout faire depuis le
téléphone, sans serveur ni clé d'API.
1. Le LLM gratuit est réglé une fois pour toutes (Projet Claude ou Gem Gemini dont les instructions
   contiennent le prompt). Le parent prend 1 à 10 photos dans l'app du LLM, puis copie le JSON obtenu.
2. Il le colle dans miniprof. L'app contrôle le module et, s'il y a des erreurs, prépare le message
   à renvoyer au LLM.
3. Le parent teste 5 questions tirées au hasard. S'il trouve une erreur, l'app prépare un message de
   correction pour le LLM. S'il n'en trouve pas, il valide et le module est **enregistré sur
   l'appareil** (un seul appareil, partagé avec les enfants : pas de publication sur GitHub).
Le site reste 100 % statique et aucune requête ne part vers un tiers. Les modules publiés sur le site
(`modules/*.json`) continuent de fonctionner.

## Décisions
- **Taille d'un module : environ 30 questions** (2 à 4 compétences, 8 à 10 questions par compétence,
  chaque niveau de difficulté représenté). La leçon ne change pas. 30 questions plus la leçon
  représentent environ 25 à 35 Ko de JSON : un LLM gratuit les produit sans problème en une seule
  réponse (`prompt.py` situe la limite vers 60 questions). Le format garde la possibilité d'ajouter
  des lots plus tard (merge.py).
- **Test de 5 questions** : une par compétence d'abord, en privilégiant les difficultés 3 et 4 (là où
  le LLM se trompe le plus). À dire clairement dans l'app : ce test repère les erreurs systématiques
  (méthode mal comprise, format) mais pas toutes les erreurs isolées. Si 3 questions sur 30 sont
  fausses, le test a environ 1 chance sur 2 de n'en voir aucune. Le bouton « signaler » reste le
  filet de sécurité.
- **Brouillon gardé en localStorage** : sur iPhone, passer à l'app Claude puis revenir peut faire
  recharger la page Safari. Une version gardée seulement en mémoire (comme l'aperçu actuel) serait
  perdue.
- **Correction** : le LLM renvoie le JSON complet (pas de fusion en JS). L'app revalide, puis refait
  un test qui contient les questions corrigées et de nouvelles questions tirées au hasard.
- **Copier le prompt** : bouton qui utilise `navigator.clipboard.writeText` (asynchrone). C'est une
  2ᵉ exception à la règle « asynchrone limité à la lecture de fichiers », à ajouter dans CLAUDE.md.
  Le prompt est lu dans `docs/prompt-nouveau.md`, toujours généré par prompt.py.

⚠ Complexité ajoutée (à signaler, comme le demande CLAUDE.md) : environ 400 à 500 lignes de JS
nouvelles, dont un **validateur JS** qui recopie les règles principales de validate.py. Il faudra
garder les deux synchronisés, avec des cas de test partagés (même principe que `normalisation.json`).

## Étapes (une par session, recette dans docs/recette.md)

### Étape 8 — Modules plus courts (Python et docs seulement)
- `tools/prompt.py` : `REGLES` et texte d'en-tête → 2 à 4 compétences, environ 30 questions.
  Ajouter une phrase pour le Projet Claude : « je t'envoie des photos ; réponds par le module JSON ».
  Régénérer `docs/prompt-nouveau.md`.
- `tools/validate.py` : `CIBLE_QUESTIONS` 100 → 30 et message de l'avertissement (plus de « 100 à
  200 »).
- Tests : `test_prompt.py` et `test_validate.py`.
- `docs/besoins.md` et `docs/risques.md` (R3 : test de 5 questions + signalement).
- Nouveau `docs/parent-iphone.md` : régler le Projet Claude (ou le Gem) une fois, et le refaire
  quand le schéma change.

### Étape 9 — Modules enregistrés sur l'appareil
- Nouveau `js/local-modules.js` : clé `miniprof.v1.modules` = { id: module }. Fonctions
  `listLocalModules()`, `getLocalModule(id)`, `saveLocalModule(data)` (refuse un id déjà utilisé
  par un module du site), `deleteLocalModule(id)`. Passe par `readKey` et `writeKey` de
  `js/storage.js`.
- `js/open-module.js` : un id présent sur l'appareil s'ouvre sans `readJson`, avec le même
  `checkModule`.
- `js/screens/library.js` et `js/screens/report.js` : ajouter les modules de l'appareil à ceux de
  `index.json` (badge « sur cet appareil »). Si `index.json` est illisible, les modules locaux
  s'affichent quand même.
- `js/screens/module-home.js` : zone parent « Supprimer ce module de l'appareil ».
- `js/backup.js` (`buildBackup`, `checkBackup`, `restoreBackup`) : la sauvegarde contient les
  modules de l'appareil, sinon un téléphone perdu ferait perdre les modules. Vérifier que
  `tools/analyse.py` accepte la nouvelle clé.

### Étape 10 — Écran « Nouveau module » (parent)
- Nouveau `js/screens/new-module.js`, route `#/nouveau` dans `js/app.js`, lien depuis la zone
  parent de la bibliothèque (à la place de l'import de fichier, ou à côté).
- Contenu : bouton « Copier le prompt », grande zone pour coller la réponse du LLM, bouton
  « Contrôler ».
- Nouveau `js/validate-module.js` : extrait le JSON du texte collé (du premier `{` au dernier `}`,
  ce qui retire les ``` et le texte autour), puis applique les règles de structure et les règles
  sémantiques reprises de `validate.py` (`verifier_semantique`, `verifier_number`,
  `verifier_choice`, `verifier_text`), avec les mêmes messages, et produit le même texte que
  `texte_llm()`. Réutilise `normalizeText` (`js/answers.js`). `checkModule` reste le contrôle
  défensif à l'ouverture.
- Message pour le LLM affiché dans une zone en lecture seule, avec un bouton « Copier ».
- Brouillon (texte collé et état du test) gardé dans `miniprof.v1.brouillon`.
- Synchronisation : `tools/tests/fixtures/validation.json` (modules invalides et chemins d'erreur
  attendus). Test Python dans `test_validate.py` ; côté JS, extrait à coller dans la console
  (comme la recette 3.15). Nouvelle règle dans « Règles à garder synchronisées » de CLAUDE.md.

### Étape 11 — Test des 5 questions et validation
- Dans `new-module.js` : tirage des 5 questions (une par compétence, difficultés 3 et 4 en
  priorité). Chaque question s'affiche avec `js/question-view.js` en mode aperçu (rien n'est
  enregistré), puis deux boutons : « Correcte » et « Erreur », avec une note libre.
- Lien « Voir la leçon » : ouvre le brouillon en aperçu (`setPreview` + `#/module/_apercu`).
- S'il y a au moins une erreur, l'app prépare le message pour le LLM (« Les questions q012, q031
  sont fausses : <notes>. Corrige-les sans changer les id, renvoie le JSON complet. »), puis on
  revient au collage. S'il n'y en a aucune, bouton « Ajouter le module » → `saveLocalModule`,
  suppression du brouillon, ouverture du module.
- Mettre à jour CLAUDE.md : arborescence et contraintes (modules sur l'appareil, exception
  presse-papiers).

## Vérification
- `python -m unittest discover tools/tests -v` (prompt, validate, cas de synchronisation).
- Extrait à coller dans la console pour le validateur JS (fixtures partagées) : affiche `[]`.
- Bout en bout sur l'iPhone (Safari, site GitHub Pages ou `python3 -m http.server` sur le réseau
  local) : photos dans le Projet Claude → copier → coller dans miniprof → erreur volontaire
  (supprimer une virgule) → message pour le LLM → correction → test de 5 questions → noter une
  erreur → message → JSON corrigé → validation → le module apparaît dans la bibliothèque, se
  pratique, compte dans le bilan, et figure dans la sauvegarde exportée puis restaurée.
- Passer à l'app Claude au milieu de la création, revenir : le brouillon est toujours là.
