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
