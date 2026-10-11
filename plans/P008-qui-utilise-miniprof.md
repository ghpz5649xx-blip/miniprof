# P008 — « Qui utilise miniprof ? » redemandé après 30 minutes

- **Statut** : à mûrir, cadré le 11 oct. 2026 ; prêt pour un go (exécution dans une nouvelle
  conversation).
- **Origine** : sponsor, 11 oct. 2026. Un même appareil a servi à un profil de test, à la 6e
  (module d'électricité) puis au CM1 (dictée) : tout est arrivé dans le même profil, parce que
  miniprof garde le dernier profil choisi sans limite de temps (clé `miniprof.v1.current`).

## Besoin
Quand quelqu'un ouvre miniprof, y compris par un lien direct vers un module (lien envoyé par
Claude après la mise en ligne d'un module), il arrive sur « Qui utilise miniprof ? » si
l'appareil n'a pas servi depuis un moment. Les résultats ne se mélangent plus entre personnes.

## Décisions (sponsor, 11 oct. 2026)
- **Quand redemander** : après **30 minutes sans utilisation**. Pas à chaque chargement de page
  (passer d'un module HTML à « Mon bilan » recharge la page : l'enfant devrait choisir sans
  cesse) ; pas « à chaque onglet » (Safari rouvre l'ancien onglet : peu fiable).
- **Lien direct** (app ou module HTML) : choix du profil, puis retour à la page demandée.
- **Page restée ouverte** au-delà de 30 minutes : la réponse suivante **n'est pas enregistrée**,
  la page envoie vers « Qui utilise miniprof ? » puis revient au module. Une question perdue
  plutôt qu'un résultat chez la mauvaise personne.

## Proposition technique (à confirmer à l'exécution)
- Nouvelle clé `miniprof.v1.derniere_activite` (date en secondes), mise à jour à chaque page
  ouverte et à chaque réponse. `miniprof.v1.current` ne change pas de format (rien à migrer) :
  un profil courant dont l'activité date de plus de 30 minutes est traité comme absent.
- App (`js/app.js`, `js/profiles.js`) : sans profil valide, `#/` avec l'adresse de retour.
- Modules HTML (`js/suivi.js`, aucun module à régénérer) : au chargement et à chaque réponse,
  si le délai est dépassé, renvoi vers l'app avec l'adresse du module pour y revenir.
- Tests : recette navigateur (délai simulé : profil gardé avant 30 min, redemandé après ; lien
  direct vers un module ; réponse non enregistrée sur une page restée ouverte).

## Hors périmètre
- Séparer les données déjà mélangées dans un profil (possible à peu près par module : sciences et
  anglais pour la 6e, dictée et tables pour le CM1) : ligne au backlog.

## Feed-back
(sans objet)
