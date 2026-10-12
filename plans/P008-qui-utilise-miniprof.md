# P008 — « Qui utilise miniprof ? » redemandé après 30 minutes

- **Statut** : exécuté le 12 oct. 2026 (go du sponsor) ; feed-back possible jusqu'au 26 oct. 2026.
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

## Proposition technique (initiale)
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

## Livré (12 oct. 2026)
- `js/activite.js` (nouveau) : clé `miniprof.v1.derniere_activite` (secondes, écrite au plus toutes
  les 10 s), délai de 30 min, adresse de retour validée (écran de l'app `#/…` ou
  `modules/<id>.html` seulement : pas de redirection vers un autre site), et `garderSession()`.
- `js/profiles.js` : `profilActif()` = profil courant **et** activité de moins de 30 min.
  `currentProfile()` ne change pas (les écrans l'utilisent), `miniprof.v1.current` non plus : rien
  à migrer. `setCurrent()` note aussi l'activité.
- `js/app.js` : sans profil actif, `#/?retour=<écran>` puis retour à l'écran après le choix.
- `js/suivi.js` (modules HTML, aucun à régénérer) : au chargement, sans profil actif, renvoi vers
  le choix avec retour à la page du module.
- **Page restée ouverte** : `garderSession()` intercepte le toucher suivant *avant* que la page le
  voie (capture + `stopImmediatePropagation`), dans l'app comme dans les modules. Rien n'est
  enregistré, on passe par le choix du profil. Choix un peu plus large que la fiche (« la réponse
  suivante ») : même le premier toucher est intercepté, ce qui évite aussi les effets de bord de la
  page générée.
- Un appareil sans `derniere_activite` (tous, au premier chargement après ce push) redemande le
  profil **une fois** ; le profil courant est conservé et reste proposé.
- Docs : `README.md` (côté enfant), `docs/module-html.md` (profil).

## Vérifié
- Tests unitaires : 77 OK (dont `test_sync.py`). `build_index.py` : index inchangé.
- Recette navigateur : 55 OK, dont 11 nouveaux contrôles : sans profil → choix → retour au
  module ; 25 min : profil gardé ; 31 min : redemandé ; profil courant conservé ; page de module
  restée ouverte (réponse refusée, toucher intercepté) ; lien direct vers un module de l'app ;
  adresse de retour d'un autre site ignorée ; page de l'app restée ouverte.

## Recette (à faire sur l'iPhone)
1. Ouvrir le site : « Qui utilise miniprof ? » s'affiche une fois (clé nouvelle). Choisir un profil.
2. Fermer l'app, la rouvrir dans les 30 min : on arrive directement dans la bibliothèque.
3. Ouvrir un lien direct vers un module HTML après 30 min sans l'utiliser : choix du profil, puis
   le module s'ouvre.
4. Laisser un module ouvert plus de 30 min, puis toucher une réponse : retour au choix du profil,
   puis au module ; la réponse n'est pas enregistrée.

## Tâches du sponsor
- Faire la recette ci-dessus sur l'iPhone (les deux enfants, un appareil partagé).

## Feed-back
(aucun pour l'instant)
