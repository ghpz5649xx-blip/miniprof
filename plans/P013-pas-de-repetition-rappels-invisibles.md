# P013 — Pas de question répétée, passes invisibles

- **Statut** : exécuté le 15 nov. 2026 (feed-back possible jusqu'au 29 nov.).
- **Origine** : sponsor, 15 nov. 2026, après l'essai de la Dictée 7 en parcours QCM puis écriture :
  « éviter de poser plusieurs fois les mêmes questions et utiliser le principe de passe sans que ce
  soit forcément visible », pour tous les modules, pas seulement les dictées. Décision du sponsor
  le même jour : supprimer les modules JSON (il ne s'en sert pas).

## Besoin
Un enfant ne doit pas revoir la même question dans une séance, et ce qu'il rate doit lui revenir
sans qu'il ait à comprendre un système de « passes ».

## Décisions
- **Entraînement (tous les modules HTML)** : jamais deux fois la même question (énoncé + réponse) ;
  une question ratée du premier coup revient 4 questions plus tard, sous une autre forme (même
  compétence, même niveau). Rien d'affiché. Dans le moteur du gabarit (`questionNeuve()`,
  `S.rappels`, `S.vus`), appliqué aux 8 modules existants par le même correctif.
- **Dictées** : une jauge « mots acquis » remplace les passes. Un mot raté revient 4 questions plus
  tard ; quand tous les mots sont posés, les mots ratés sont reposés (vérification cachée) jusqu'à une
  vérification sans faute. Un mot réussi du premier coup n'est jamais reposé.
- **Évaluation** : inchangée (10 questions, sans rappel, sans doublon : P002).
- **Rien n'est gardé entre deux séances** : aucun nouveau format dans le journal.
- **Modules JSON supprimés** (écrans, outils, schéma, tests) : le deuxième lot prévu (moteur JSON)
  n'a donc plus d'objet.

## Mise à jour du 17 nov. 2026
Le sponsor supprime l'étape 1 (QCM) des dictées, jugée inutile, et veut qu'une bonne réponse passe
tout de suite à la question suivante, sans « Bravo ». Une dictée = un seul parcours « écrire les
mots » (Dictée 7 et gabarit mis à jour). Dans les autres modules, l'entraînement garde ses messages.

## Contrôles
- Recette navigateur (`tools/recette_navigateur.py`) : aucune question posée deux fois sur 16 ;
  chaque question ratée revient 5 questions plus tard dans la même compétence ; la dictée fait
  28 questions (24 + 2 rappels + 2 vérifications) en un seul parcours, sans « passe » affichée.
- Moins strict qu'une vraie passe : le mot raté est reposé juste après 4 autres questions (mémoire
  courte), d'où la vérification finale.

## Mise à jour du 21 nov. 2026 (feed-back du sponsor)
- **Le compteur monte à chaque bonne réponse.** Entraînement : « N bonnes réponses » remplace « X
  réussies du premier coup sur Y » et compte aussi le deuxième essai (le journal ne garde toujours
  que le premier). Dictées : le même compteur, qui monte aussi sur un mot raté plus tôt (rappel,
  vérification). Dictée 5 (parcours à étoiles) : la deuxième chance juste rapporte 1 point au lieu
  de 0. Un « +1 » (ou « +n ») bref s'affiche à côté du compteur.
- **Bonne réponse = question suivante tout de suite, sans « Bravo »**, dans tous les modules (la
  règle des dictées du 17 nov.). Deux arrêts restent : la proposition de niveau, une fois, à 5
  réussites d'affilée ; le schéma juste du module circuit (la lampe allumée est la correction).
- Le parcours de la Dictée 5 se recalcule depuis le journal : les deuxièmes chances déjà réussies
  rapportent maintenant 1 point chacune, donc certaines jauges montent un peu (jamais l'inverse).
- Contrôles : `test_parcours.py` (gain de la deuxième chance) ; recette navigateur : en
  entraînement, une bonne réponse passe à la suivante sans message, compteur +1 ; en dictée, le
  compteur monte à chaque bonne réponse.

## Reste
- Rien (la Dictée 5 ne sera pas refaite : décision du sponsor, 21 nov. 2026).

## Feed-back
- **21 nov. 2026 (sponsor, écran d'admin)** : « Ce plan est très bon dans l'ensemble. A noter, mes enfants se plaignent que lorsqu'ils font une faute, la prochaine question même juste n'augmente pas leur score. Il faudra donc modifier ce comportement pour que le compteur augmente à chaque bonne réponse et c'est très important pour mes enfants de voir le compteur monter. La mise à jour du 17/11/26 doit être appliqué à tous les types de modules pas seulement au module dictée. » Traité le même jour : voir « Mise à jour du 21 nov. 2026 ».
