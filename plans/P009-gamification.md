# P009 — Gamification : étude du comportement et règles génériques

- **Statut** : plan d'étude terminé le 11 oct. 2026 ; **à mûrir** (aucun code, aucun go demandé).
- **Origine** : sponsor, 11 oct. 2026. Question : quelles règles de jeu pour pousser les enfants
  vers le comportement qui profite le plus à leur révision ?
- **Données** : un export (un seul profil, les deux enfants et des essais du sponsor mélangés :
  voir P008). Seules deux séances sont retenues, sur la parole du sponsor : la 6e, module
  d'électricité, 13 h 01 – 13 h 23 ; le CM1, module de dictée 5, 18 h 15 – 18 h 43. **N = 2
  séances** : des hypothèses, pas des preuves.

## Ce que montrent les deux séances
| | 6e (électricité, 22 min) | CM1 (dictée 5, 28 min) |
|---|---|---|
| Enchaînement | s'entraîne (échauffement « del », 17 q.) → évaluation mixte 9/10 → s'entraîne sur **la compétence ratée** (« court », 8 q.) → évaluation niveau 2 8/10 → 2 q. sur « del » → évaluation niveau 2 **10/10**, puis s'arrête | 39 q. d'entraînement niveau 3 (29 justes) → évaluation mixte 8/10 → évaluation niveau 1 7/10 → 8 min d'arrêt → **48 q. « noms » niveau 1** (44 justes, 3 s par réponse, 6 mots) |
| Ce qu'elle/il travaille | exactement ses points faibles | ses points forts ; « nature », « être/avoir », « mots » (ratés à l'évaluation) ne sont pas revus |
| Fin de séance | sur la note maximale | à la fin de la boucle facile |

1. **Les deux sont sensibles à la note** : la 6e s'arrête à 10/10, le CM1 ne rejoue pas une
   évaluation ratée mais se « refait » une série de réussites faciles.
2. **Quand l'écran de résultat nomme la compétence ratée, la 6e s'en sert** : la boucle
   évaluation → entraînement ciblé → réévaluation est la bonne, à un défaut près (réévaluer
   1 à 3 minutes après teste la mémoire immédiate, pas l'acquis : rien ne l'invite à revenir le
   lendemain).
3. **Le CM1 optimise le taux de réussite, pas l'apprentissage** : boucle sur le contenu déjà
   maîtrisé (6/6 en niveau 3 à 18 h 15, puis 44 réussites en niveau 1).
4. **Personne ne revient** dans ces données : une séance par module et par jour ; rien ne
   récompense la régularité, qui est pourtant le premier levier de mémorisation.
5. Hors périmètre mais même motif (si c'est bien un enfant) : « tables 3-6-9 », 13 h 35, ~40
   réponses « table de 3 » niveau 1 à 2-3 s.

## Règles génériques proposées (à valider une par une)
Principe commun : **tout se calcule à partir des événements existants** (date, compétence,
difficulté, mode, juste, question) ; rien de nouveau à stocker, donc aucune migration, et
l'historique déjà là compte rétroactivement. Les points ne baissent jamais.

- **R1 — Valoriser l'effort utile, pas le volume.** Une réussite vaut sa difficulté (1 à 4) ;
  rendements décroissants par compétence, niveau et jour (plein tarif jusqu'à 5, moitié
  jusqu'à 10, zéro ensuite) ; **×2 sur un point faible** (compétence « à travailler » ou ratée
  dans la dernière évaluation). La boucle « noms » du CM1 vaudrait au plus 7,5 points au lieu de
  44 ; la séance de la 6e (ciblée) vaut ~35 points pour 24 réussites.
- **R2 — Maîtrise par compétence, étagée par niveau et espacée.** Un niveau est « validé » après
  des réussites sur plusieurs questions **sur au moins 2 jours différents**. Donne une marche à
  gravir (donc une raison de monter) et une raison de revenir demain.
- **R3 — Régularité à la semaine.** Un « jour actif » = ≥ 10 réponses sur ≥ 2 compétences.
  Objectif : 3 jours actifs par semaine. Pas de série quotidienne qu'on « perd ».
- **R4 — L'évaluation est un contrôle, pas un jeu.** Aucun point pour une note. Un seul geste
  récompensé : **« Réparé »** = compétence ratée en évaluation, puis réussie en entraînement,
  puis réussie à nouveau un autre jour. Il transforme la boucle spontanée de la 6e en
  apprentissage espacé. Les rejouements immédiats restent permis, non récompensés (rejoint P007).
- **R5 — Mission du jour.** En tête d'un module : « 3 points à renforcer » (à travailler, en
  baisse, ratés à la dernière évaluation, non revus depuis 3 jours). Les terminer = l'étoile du
  jour. C'est la porte de sortie de la boucle facile du CM1.
- **R6 — Invitation à monter.** Après ~10 réussites d'affilée à moins de 4 s : « Trop facile ?
  Passe au niveau suivant ». Suggestion, jamais d'obligation.
- **R7 — Carnet de la semaine pour le parent.** Une page (étoiles, jours actifs, missions,
  « Réparé ») : la vraie récompense reste hors de l'app, choisie par le sponsor.
- **Garde-fous** : pas de chronomètre ni de points de vitesse (la 6e a fait l'évaluation 2 à 8 s
  par question contre 22 s pour la 1re) ; pas de classement entre frère et sœur (niveaux
  différents : chacun se mesure à son passé) ; rien de perdu ; pas de récompense aléatoire ;
  pas de notification ; visuel sobre.

## Questions ouvertes
- Réglages (seuils, poids) à calibrer sur la revue d'usage n° 2, avec des exports propres
  (P008 d'abord : sans lui, impossible de séparer les enfants).
- Où afficher : bibliothèque, accueil d'un module, fin de séance ? Les modules HTML doivent-ils
  parler à `js/suivi.js` pour l'affichage en séance (contrat `docs/module-html.md`) ?
- Que vaut un point en vrai ? Décision du sponsor.

## Suite
Reprendre après P008 et la revue d'usage n° 2 (~26 oct.). Si go : découper en livraisons
indépendantes, dans cet ordre : R5 + R6 (nudges, sans score) → R1 + R2 (points et maîtrise) →
R3 + R7 (rythme et carnet) → R4 (« Réparé »). Une seule à la fois, recette navigateur à chaque
étape.

## Feed-back
(sans objet)
