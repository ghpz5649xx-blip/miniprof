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

## Contrôles
- Recette navigateur (`tools/recette_navigateur.py`) : aucune question posée deux fois sur 16 ;
  chaque question ratée revient 5 questions plus tard dans la même compétence ; la dictée fait deux
  étapes de 28 questions (24 + 2 rappels + 2 vérifications), sans « passe » affichée.
- Moins strict qu'une vraie passe : le mot raté est reposé juste après 4 autres questions (mémoire
  courte), d'où la vérification finale.

## Reste
- La Dictée 5 (parcours à étoiles, P012) n'a pas le parcours QCM puis écriture : à refaire sur photo.

## Feed-back
(en attente)
