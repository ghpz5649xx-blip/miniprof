# P003 — Signaler un problème depuis l'app (et un export plus simple à partager)

- **Statut** : exécuté le 11 oct. 2026 ; feed-back possible jusqu'au 25 oct. 2026, puis clos.
- **Origine** : demande du sponsor, 12 oct. 2026.

## Besoin
Un enfant qui tombe sur une question fausse ou un problème le signale tout de suite, avec un
commentaire facultatif, pour que le sponsor le sache et que Claude corrige.

## Ce qui est déjà décidé
- **Option A** (choix du sponsor) : bouton « Signaler » sous chaque question (modules HTML et JSON),
  commentaire facultatif, enregistré sur l'appareil, visible dans l'export, `tools/analyse.py` et
  un écran parent.
- **Condition du sponsor : revoir la fonction export.** Aujourd'hui un signalement n'arrive au
  sponsor que par un export ; l'export doit être **plus simple à envoyer et à partager d'un
  appareil à un autre**.
- Options écartées : B (le bouton ouvre Messages avec un texte rempli : rien n'est gardé dans
  l'app ; c'était la recommandation de Claude), C (A + B).

## Décisions du 11 oct. 2026 (atelier de cadrage)
- **Export plus simple = bouton « Partager » du système (iOS)** branché sur l'export : deux
  touches vers Messages, AirDrop ou Mail, sans passer par Fichiers. Reste manuel, assumé.
  Aucune contrainte du projet n'est touchée.
- **Pas de base de données connectée** pour les données des enfants (synchronisation complète :
  comptes, données chez un tiers, fin du « tout se recalcule en local » ; déjà écartée par P005).
- **Canal à sens unique pour les seuls signalements** (id module, id question, commentaire, date,
  sans prénom) : **POC isolé dans `poc/`, hors de P003**, ligne au backlog. Il demandera de lever
  « aucune requête vers un tiers » pour ce seul cas : décision du sponsor après le POC.

- **Lecture des signalements : `tools/analyse.py` seulement**, à partir de l'export. Pas d'écran
  parent dans l'app (pourra venir plus tard si le besoin se fait sentir).

- **Parcours de l'enfant (a)** : il appuie sur « Cette question me semble fausse », le signalement
  est enregistré tout de suite ; un champ facultatif apparaît ensuite (« Tu veux dire pourquoi ? »)
  avec « Envoyer ». Sans commentaire, le signalement est déjà pris en compte.
- **Format** : nouvelle clé `miniprof.v1.flag_notes` pour les commentaires, les lignes de
  `miniprof.v1.flags` ne changent pas ; incluse dans l'export et la restauration ; test sur
  anciens et nouveaux signalements.

## Découpage proposé (à valider par un go)
1. **Export partageable** : `navigator.share` avec le fichier d'export (repli sur le
   téléchargement actuel si le partage n'existe pas) ; test de la logique de repli.
2. **Commentaire de signalement** : clé `flag_notes`, champ après le signalement, export /
   restauration, test de compatibilité ; modules JSON puis modules HTML (contrat
   `docs/module-html.md`, via `js/suivi.js`).
3. **`tools/analyse.py`** : section « Signalements » (module, question, profil, date,
   commentaire) ; test.
Recette iPhone (partage réel, signalement avec et sans commentaire) : tâche du sponsor.

## Contraintes connues
- Aucun serveur : un signalement reste sur l'appareil de l'enfant jusqu'à l'export.
- Les modules JSON ont déjà « Cette question me semble fausse » (`js/flags.js`, clé
  `miniprof.v1.flags` = `[module, question, date, profil]`), sans commentaire. Ajouter un
  commentaire = changement de format : nouvelle clé ou migration, avec un test, sans casser les
  anciens signalements.
- Modules HTML : passer par `js/suivi.js` (contrat `docs/module-html.md`), jamais par le stockage.

## Points cadrés le 11 oct. 2026 (voir les décisions ci-dessus)
- Ce que veut dire « plus simple à partager » pour l'export (partage iOS, envoi par message,
  fichier plus léger…).
- Où le sponsor lit les signalements (écran parent, `analyse.py`, les deux).
- Découpage en unités et recettes sur l'iPhone.

## Changements décidés pendant l'exécution
- **Modules HTML** (décision du sponsor) : bouton « Une erreur ? » **à côté de « Valider »**, avec
  confirmation « Tu penses qu'il y a une erreur dans cette question ? Oui / Non » ; miniprof garde **toute la
  question** (énoncé, choix, réponse attendue, réponse donnée), sans id de question (elles sont
  tirées au hasard). Le bandeau du haut n'est pas utilisé.
- **Format** : au lieu de `flag_notes`, une clé **`miniprof.v1.signalements`** (liste d'objets avec
  la copie de la question et le commentaire), commune aux modules JSON et HTML. `flags` ne change
  pas (il retire toujours la question du tirage des modules JSON).
- **Exception à « asynchrone limité à la lecture de fichiers »** (décision du sponsor) :
  `navigator.share()` est asynchrone ; il est confiné à `js/partage.js` et la date du dernier
  export n'est notée que si le partage a abouti. `CLAUDE.md` mis à jour.
- Règle de synchronisation de `CLAUDE.md` et `test_sync.py` : `js/suivi.js` écrit par
  `addEvents()` et `addSignalement()` / `commentSignalement()`.
- Les **5 modules HTML existants** ont reçu le bouton (même correctif que le gabarit, comme P002) ;
  leur contenu pédagogique ne change pas.

## Livré
1. **Export partageable** : « Exporter et partager » (feuille de partage du système) quand le
   navigateur sait partager un fichier ; « Télécharger le fichier » à côté, ou seul sinon.
2. **Signalement avec commentaire** : modules JSON (après la correction, parcours (a) : enregistré
   tout de suite, commentaire ensuite) et modules HTML (gabarit + 5 modules) ; export et
   restauration (`signalements` facultatif : les anciens fichiers restent lisibles).
3. **`tools/analyse.py`** : section « Signalements » en tête (date, enfant, module, question,
   réponses, commentaire) ; les anciens `flags` sans copie y figurent aussi.
Contrat `docs/module-html.md` et `README.md` à jour.

## Vérifié (recette)
- Tests : 77 OK. `check_html.py` et `tirage.py` sur les 5 modules HTML.
- Recette navigateur (Chromium) : 45 OK, dont : « Non » n'enregistre rien ; copie de la question
  et commentaire (module HTML et module JSON) ; export avec `signalements` ; restauration d'un
  ancien fichier (questions et résultats gardés) ; partage simulé (abouti, annulé, en erreur,
  absent).
- Capture à 400 px de large (module de dictée) : « Valider · Un indice · Signaler » sur une ligne,
  confirmation dessous.
- Non vérifié ici : le vrai partage sur iPhone (voir les tâches du sponsor).

## Tâches du sponsor
- Sur l'iPhone, écran « Sauvegarde » : « Exporter et partager » ouvre-t-il bien la feuille de
  partage, et le fichier arrive-t-il dans Messages ou AirDrop ? Si le bouton « Exporter et
  partager » n'apparaît pas, c'est que Safari refuse de partager un fichier JSON : le dire à Claude.
- Dans un module HTML (par exemple la dictée) : appuyer sur « Une erreur ? », répondre Non (rien ne se
  passe), puis Oui, écrire un commentaire. Faire de même sur une question d'un module JSON. Puis
  exporter et lancer `python tools/analyse.py` : les deux signalements doivent apparaître.

## Feed-back
- 11 oct. 2026 : textes des modules HTML jugés trop adultes. Bouton « Signaler » → « Une erreur ? » ;
  confirmation « La réponse attendue te semble fausse ? » → « Tu penses qu'il y a une erreur dans
  cette question ? ». Corrigé dans le gabarit et les 5 modules ; recette relancée.
- Noté, non fait : le bouton des modules JSON garde « Cette question me semble fausse » (déjà
  clair, autre écran) ; à aligner plus tard si le sponsor le souhaite.
- 11 oct. 2026 : recette iPhone faite par le sponsor, tout fonctionne (partage, signalement HTML
  avec commentaire). Export joint à la conversation Claude Code : reçu, `analyse.py` affiche le
  signalement. Circuit retenu pour transmettre un export à Claude : la pièce jointe dans la
  conversation (pas de dépôt ni de Notion).

## Retour P003 / P010 du 12 oct. 2026 (sponsor)
Le bouton « Une erreur ? » gênait à côté de « Valider ». Il est maintenant **large, discret (pointillé gris, drapeau ⚑), tout en bas de l'écran** (rouge plein jugé trop agressif, variante B choisie par le sponsor) (poussé en bas par `margin-top:auto` ; juste après la question si l'écran est petit). Gabarit et 5 modules HTML ; l'app (modules JSON) inchangée. Recette navigateur 55 OK ; Chromium 390×844 et 390×480 : bouton à sa place, confirmation Oui / Non ouverte au-dessus. À regarder sur l'iPhone.
