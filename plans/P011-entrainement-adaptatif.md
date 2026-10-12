# P011 — Entraînement adaptatif : le moteur choisit la compétence et la difficulté

- **Statut** : cadrage terminé le 12 oct. 2026 ; **à mûrir** (aucun code, aucun go demandé).
- **Origine** : sponsor, 12 oct. 2026. Le tirage se répète (« est » une fois sur deux en Être
  niveau 2) ; l'enfant choisit lui-même sa compétence, donc évite ce qui est fragile.
- **Constat dans le code** : le tirage vit dans chaque module HTML (`__miniprofTirage`, générateurs
  avec `Math.random`). Il n'a aucune mémoire de ce que l'enfant a réussi ou raté.

## Décisions du cadrage (sponsor)
| # | Décision | Pourquoi |
|---|---|---|
| D1 | Le moteur choisit la **compétence et la difficulté** ; l'élève ne règle plus rien par défaut. | Le choix de l'élève est le plus mauvais indicateur de ce qu'il doit travailler. |
| D2 | **Rien de visible** : pas de jauge ni de pourcentage pour l'enfant. | Pas de changement d'écran, risque faible ; la jauge relève de P009. |
| D3 | Un « **Je choisis** » **discret** (menu secondaire) conserve le choix libre. | Filet de sécurité : s'entraîner sur ce qui est au contrôle de demain. |
| D4 | Périmètre de départ : **conjugaison CM1** + le **gabarit** (tout nouveau module HTML l'a d'office). | Le problème est observé là ; la revue d'usage n° 2 dira s'il faut élargir. |
| D5 | Les anciens modules HTML ne sont pas retravaillés ; sans poids fournis, ils **tirent comme aujourd'hui** (repli). | Ne rien casser chez les enfants ; le repli coûte quelques lignes. |
| D6 | La maîtrise **se recalcule** depuis les événements existants. | Aucun nouveau format de stockage, aucune migration (`CLAUDE.md`). |

## Approche proposée
- L'app calcule, par compétence, une maîtrise de 0 à 1 et un niveau de difficulté courant, et
  l'expose au module (`window.miniprof.poids()`, nom à confirmer). Le gabarit tire selon ces poids
  s'ils existent, sinon au hasard comme avant.
- **Contrat modifié** (`docs/module-html.md`, gabarit) : c'est une évolution de la grammaire, donc
  un plan avec go (`CLAUDE.md`). `tools/check_html.py` et `test_sync.py` suivent.
- Le mode libre (D3) réutilise l'écran de choix actuel, déplacé derrière un lien secondaire.

## Seuils proposés (à corriger par le sponsor)
- **Démarrage à froid** : les 5 premières questions de chaque compétence sont réparties
  uniformément ; l'adaptatif ne s'active qu'ensuite (aussi pour un nouveau module).
- **Proportions d'une série** : environ 60 % sur le fragile, 30 % en progression, 10 % sur
  l'acquis (révision). Une série commence et finit par une question réussissable.
- **Maîtrise lissée** : les essais récents pèsent plus ; « acquise » seulement avec un minimum
  d'essais (proposition : 5). Une erreur isolée ne bascule rien.
- **Difficulté** : monter après 3 réussites sur 4, redescendre après 2 échecs de suite ;
  jamais plus d'un niveau d'écart avec la dernière question.
- **Répétition** : jamais la même compétence 3 fois de suite ; mémoire des 5 dernières
  questions (cohérent avec P002).
- **Une compétence ratée** repasse tout de suite en haut du tirage.

## Risques et mitigations
| Risque | Mitigation |
|---|---|
| Perte d'autonomie | « Je choisis » conservé (D3). |
| Décrochage si l'enfant ne voit que ses échecs | Proportions 60/30/10 ; début et fin de série réussissables. |
| Démarrage à froid | Tirage uniforme sur les 5 premiers essais. |
| Estimation fragile avec peu de données | Lissage, seuil minimal d'essais, hystérésis. |
| Complexité (tirage dans chaque module) | Poids fournis par l'app, logique dans le gabarit ; repli (D5). |
| Vérification plus difficile | Tests déterministes (graine fixe) sur historiques simulés ; `tools/tirage.py` étendu pour contrôler qu'une compétence n'excède pas une part donnée. |
| Données des enfants | Aucune écriture nouvelle (D6). |

## Questions ouvertes
- Les seuils ci-dessus (à valider ou corriger).
- Où est calculée la maîtrise : `js/stats.js` (existant) ou un nouveau fichier ?
- Nom et forme exacts de l'interface app → module.
- Lien avec P009 (points sur l'effort utile, « à travailler ») : mêmes notions de point faible ;
  à harmoniser avant d'exécuter l'un ou l'autre.

## À l'exécution (rappel)
Contrat modifié → plan avec go ; recette navigateur verte avant le push (module en production
chez le CM1) ; recette iPhone en tâche du sponsor ; `README.md` et `plans/index.md` à jour.
