# P004 — Un pipeline de création de modules sans Claude Code

- **Statut** : abandonné le 14 oct. 2026 (tri du backlog, sur décision du sponsor) : on reste sur Claude Code. Cette fiche absorbe l'idée « créer un module depuis miniprof, sans Claude Code ».
- **Origine** : demande du sponsor (assessment), 6 oct. 2026.

## La question
Aujourd'hui un module naît ainsi : photos → `/nouveau-module` dans Claude Code (abonnement Pro) →
page contrôlée et publiée. Existe-t-il un pipeline moins cher, ou qui ne dépende pas de Claude
Code ? Seule l'écriture de la page demande un LLM ; les contrôles (`check_html.py`,
`tirage.py`, `build_index.py`, tests) et la publication n'en demandent pas.

## Options étudiées
| | Option | Coût | Qualité | À construire |
|---|---|---|---|---|
| O0 | Statu quo : Claude Code sur l'iPhone | abonnement Pro, dans la limite du quota | la meilleure | rien |
| O1 | App Claude (un « Projet » avec gabarit et contrat) + robot de contrôle GitHub (GitHub Actions, gratuit sur un dépôt public) | même abonnement | proche de O0, sans correction en boucle | le robot (1 session) |
| O2 | LLM gratuit (ChatGPT, Gemini, Le Chat), même circuit | 0 € | plus faible (40 Ko de JS à la limite des offres gratuites) | le robot |
| O3 | API Claude payée à l'usage : script sur le Mac, correction en boucle, push | environ 0,3 à 1,5 $ par module (estimation sur les tarifs publics au 25 sept. 2026 ; < 10 $/mois à 2 modules par semaine) | égale à O0 | script (1 à 2 sessions) + clé API |
| O4 | Modèle local sur le Mac | 0 € | insuffisante aujourd'hui | beaucoup |

SWOT en bref : forces (le gabarit et `tirage.py` portent le savoir-faire ; contrôles sans LLM) ;
faiblesses (sans boucle de correction, chaque erreur revient au sponsor) ; opportunités (le robot
GitHub sert à toutes les options, O0 comprise ; O3 est la voie de sortie si l'abonnement s'arrête) ;
menaces (photos de cahiers chez un tiers avec les offres gratuites ; prix et quotas qui changent ;
erreurs de fond invisibles aux contrôles).

## Recommandation de Claude (non engagée)
1. Rester sur O0. 2. Construire le robot de contrôle GitHub. 3. POC O3 pour mesurer le coût et la
qualité réels. 4. Écarter O2 et O4. Détail complet : historique Git de `pilotage.md`, commit
« Pilotage : retours du sponsor, assessment du pipeline sans Claude Code… ».

## Feed-back
(sans objet)
