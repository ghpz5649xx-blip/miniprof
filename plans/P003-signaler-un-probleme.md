# P003 — Signaler un problème depuis l'app (et un export plus simple à partager)

- **Statut** : à mûrir (option décidée le 12 oct. 2026, cadrage à faire).
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

## À cadrer en atelier
- Ce que veut dire « plus simple à partager » pour l'export (partage iOS, envoi par message,
  fichier plus léger…).
- Où le sponsor lit les signalements (écran parent, `analyse.py`, les deux).
- Découpage en unités et recettes sur l'iPhone.

## Feed-back
(sans objet)
