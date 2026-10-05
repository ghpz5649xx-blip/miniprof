# Module HTML : le contrat

Un module HTML est une page autonome (`modules/<id>.html`) générée par un LLM à partir des photos
d'une leçon : leçon, entraînement, évaluation, avec schémas SVG, animations et questions tirées au
hasard si c'est utile. Exemple de référence : `modules/sciences-6e-circuit-electrique.html`.

miniprof ne l'affiche pas : il en **suit les résultats**. La page écrit chaque réponse dans le
journal de l'enfant (`js/events.js`) par le script `js/suivi.js`. Le bilan de miniprof, la
sauvegarde et `tools/analyse.py` la traitent comme un module JSON.

Contrôle : `python tools/check_html.py modules/<id>.html` (`--llm` : texte de correction).
`tools/build_index.py` n'indexe que les pages conformes.

## Ce que la page doit contenir

1. **La politique de sécurité**, recopiée telle quelle dans `<head>` (constante `BALISE_CSP` de
   `tools/check_html.py`) :
   ```html
   <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; object-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'">
   ```
2. **La fiche du module**, dans `<head>` :
   ```html
   <script type="application/json" id="miniprof-module">
   {
     "id": "sciences-6e-circuit-electrique",
     "title": "Le circuit électrique",
     "subject": "sciences",
     "level": "6e",
     "description": "Une ou deux phrases pour l'enfant.",
     "skills": [{ "id": "serie", "label": "Les lampes en série" }]
   }
   </script>
   ```
   - `id` : `matiere-niveau-sujet`, minuscules sans accents, tirets. Le fichier s'appelle `<id>.html`.
     **L'id ne change plus jamais** (l'historique des enfants y est rattaché).
   - `subject` et `level` : mêmes valeurs que le schéma (`schema/module.schema.json`).
   - `skills` : 2 à 8 compétences. Leurs `id` sont stables, comme l'id du module.
3. **Le script de suivi**, juste avant `</body>` :
   ```html
   <script type="module" src="../js/suivi.js"></script>
   ```
4. **Les appels de suivi**. Le script de la page reste un `<script>` classique. Il n'appelle
   `window.miniprof` qu'au moment d'une réponse, et doit fonctionner sans (page ouverte ailleurs) :
   ```js
   // Entraînement : seulement le premier essai de chaque question.
   if (window.miniprof) window.miniprof.reponse({
     competence: "serie",  // id d'une compétence de la fiche
     juste: true,
     mode: "e",            // "e" entraînement, "v" évaluation
     difficulte: 1,        // niveau de la question (1 à 4)
     question: "serie",    // nom du générateur, ou id de la question si elle est fixe
     reponse: "b",         // réponse donnée (courte)
     duree: 12,            // secondes passées sur la question
   });

   // Évaluation : une clé au début, puis toutes les réponses d'un coup à la fin.
   const cle = window.miniprof ? window.miniprof.debutEvaluation(niveau) : null;  // niveau : 1..4, ou 0 = mixte
   if (window.miniprof) window.miniprof.reponse(resultats.map((r) => ({ ...r, mode: "v", evaluation: cle })));
   ```
   - `miniprof.profil()` : prénom du profil courant, ou `null`.
   - `miniprof.racine` : adresse de l'app. Le bilan du module est à
     `miniprof.racine + "#/module/" + miniprof.module + "/bilan"`. La page n'a pas de bilan à
     elle : un bouton « Mon bilan » y mène.
   - Sans profil choisi, rien n'est enregistré. `suivi.js` ajoute en haut de la page un bandeau
     (« Tu es Léa · changer · mon bilan » ou « Choisis ton profil »).

## Ce qui est interdit (refusé par `check_html.py`)
- Toute requête réseau : `fetch`, `XMLHttpRequest`, `WebSocket`, `sendBeacon`, `import()`.
  La CSP (`connect-src 'none'`) les bloque de toute façon.
- Toute URL externe, polices Google comprises : polices système, images en SVG dans la page. Seules
  les URL de namespace `http://www.w3.org/…` sont acceptées.
- Tout accès direct au stockage (`localStorage`, `sessionStorage`, `indexedDB`, `cookie`) : seul
  `suivi.js` écrit, par `addEvents()`.
- `<iframe>`, `<object>`, `<embed>`, workers.

## Règles pédagogiques
La page sert à **réviser la leçon que l'enfant a eue en classe**, pas un cours général.
- **Partir des photos** : reprendre les notions, les définitions et surtout les **exercices** de
  la leçon (mêmes types de questions, mêmes présentations, autres nombres ou autres exemples).
  Ne pas ajouter de notion absente de la leçon.
- **Vocabulaire de la leçon** : mêmes mots, mêmes notations, même méthode que le cahier ou le
  manuel (une autre méthode, même juste, embrouille l'enfant).
- **Apprendre** : quelques fiches courtes qui reprennent la leçon, avec un exemple chacune ; une
  petite question de vérification par fiche quand c'est possible.
- **Corrections expliquées** (comme le circuit) : après une réponse fausse, dire en une phrase
  pourquoi ce choix est faux, puis « Réessayer », « Un indice » ou « Voir la correction ». La
  correction donne la bonne réponse **et pourquoi**, en une ou deux phrases, aussi quand
  l'enfant a trouvé.
- **Niveaux** : 2 à 4 niveaux de difficulté (`difficulte` 1 à 4), du plus direct (application
  de la règle) au plus piégeux (erreurs fréquentes, plusieurs étapes). L'évaluation propose
  chaque niveau et un mélange (`debutEvaluation(0)`).
- **Questions tirées au hasard** par des générateurs (un par compétence) quand la notion s'y
  prête ; chaque réponse attendue est **vérifiée** (recalculée, une seule bonne réponse, pas de
  choix en double).
- **Âge** : phrases courtes, consignes d'une ligne, gros boutons (iPhone, au doigt), pas de
  chronomètre affiché, encouragements sobres. Formulations qui conviennent à une fille comme à un
  garçon (« On passe à l'évaluation ? » plutôt que « Prête ? »).
- **Évaluation** : 10 questions environ, sans correction pendant l'épreuve, corrigé détaillé à la
  fin ; puis le bouton « Mon bilan ».

## Pièges vus sur le module circuit
- **Polices Google** dans la page d'origine : refusées (URL externe). Polices système
  (`font-family: system-ui, -apple-system, sans-serif`).
- **`localStorage` utilisé directement** pour garder les scores : refusé. Les scores sont ceux
  de miniprof (« Mon bilan »).
- **Pas de CSP** dans la page d'origine : la balise est obligatoire, recopiée telle quelle.
- **Une seule réponse comptée par question en entraînement** (le premier essai) : sinon un
  enfant qui clique au hasard jusqu'à trouver gonfle sa réussite.
- **Évaluation enregistrée d'un bloc à la fin**, avec la clé de `debutEvaluation()` : une
  évaluation abandonnée au milieu ne compte pas.
- **`window.miniprof` absent** (page ouverte ailleurs ou `suivi.js` pas encore chargé) : chaque
  appel est protégé par `if (window.miniprof)`.
- **Erreur de syntaxe JS** = page blanche sur l'iPhone : `node --check` sur le script avant de
  publier (skill `/nouveau-module`).
- Le texte affiché passe par `innerHTML` dans la page : échapper (`esc()`) tout ce qui n'est pas
  écrit en dur dans le script.

## Pourquoi ces règles
La page exécute du JS généré sur le même site que la progression des enfants. On ne relit pas ce
JS ligne à ligne : la page est **jetable**, et on la régénère au lieu de la corriger. Le contrat
garantit trois choses :
1. rien ne sort de l'appareil (aucune requête, CSP) ;
2. le journal n'est écrit qu'au bon format (par `suivi.js`) ;
3. la page reste utile même hors de miniprof.

`check_html.py` est un garde-fou contre les erreurs du LLM, pas contre un attaquant : le contenu
vient du parent, sans tiers.
