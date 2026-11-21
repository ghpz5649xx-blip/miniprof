# P006 — Dictée répétable

- **Statut** : **archivé le 21 nov. 2026 (clôturé avec le dernier moteur ; la Dictée 5 ne sera pas refaite)**. Avant : exécuté en partie (15 nov. 2026 : gabarit, règles et outil de couverture livrés ; reste à refaire la Dictée 5).
- **Origine** : sponsor et Claude, 7 oct. 2026 (décision D8 : un module « dictée » par liste de
  mots, fait avec `/nouveau-module`).

## Besoin
Rendre fiable et répétable la fabrication du module de chaque liste de mots : une photo de la
liste suffit, la couverture de la liste est vérifiée par un programme.

## Leçons déjà apprises
- Refaire toujours la même dictée fait apprendre le texte plutôt que les mots : phrases nouvelles
  à chaque séance, courtes, au présent.
- La couverture de la liste se vérifie par programme, jamais par le LLM (5 mots jamais travaillés
  avec l'ancienne méthode).
- Les mots s'**écrivent** (P001) : un module tout en choix n'a pas corrigé « son / sont ».

## Décision du 15 nov. 2026
Toute dictée suit un parcours **d'écriture** (devinettes, une question par mot, rappels invisibles
des mots ratés ; le QCM d'abord prévu a été supprimé le 17 nov., pas de leçon). Règles :
`docs/module-html.md`, « Dictées ». Livré : `docs/gabarit-dictee.html`,
`tools/couverture_dictee.py` (liste des photos ≡ mots de la page), section « Dictée » du skill
`/nouveau-module`, Dictée 7 refaite. Reste : refaire la Dictée 5 (parcours à étoiles P012).

## À cadrer en atelier (réponses)
- Un outil de `tools/` qui vérifie la couverture : fait (`couverture_dictee.py`).
- Ce que le skill change pour une dictée : fait (section « Dictée »).

## Ancien cadrage
- Un outil de `tools/` qui vérifie que chaque mot de la liste est travaillé.
- Ce que le skill doit changer pour une dictée.

## Feed-back
- **21 nov. 2026 (sponsor, écran d'admin)** : « plan clôturé avec le dernier moteur. Tu peux l'archiver ». Le reste (refaire la Dictée 5 en parcours d'écriture) est abandonné, décision du sponsor le même jour.
