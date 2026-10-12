# Pilotage miniprof

L'état du projet en un coup d'œil : le plan en cours, le backlog actif et les tâches du
sponsor. Claude le tient à jour à la fin de chaque session. Les plans passés et à mûrir ont
chacun leur fiche dans `plans/` (index : `plans/index.md`). La méthode de travail est dans
`CLAUDE.md`, « Gouvernance ».

---

## Plan en cours

**Aucun.** Une session qui ouvre un plan écrit ici son numéro et son titre ; une autre session qui
voit un plan en cours n'en ouvre pas de nouveau (sauf un feed-back ou une session module).

---

## Plans exécutés en attente de feed-back

| Plan | Exécuté le | Feed-back possible jusqu'au |
|---|---|---|
| P001 Questions à écrire | 12 oct. 2026 | 26 oct. 2026 |
| P002 Évaluation sans doublon | 12 oct. 2026 | 26 oct. 2026 |
| P003 Signaler un problème, export à partager | 11 oct. 2026 | 25 oct. 2026 |
| P008 « Qui utilise miniprof ? » après 30 min | 12 oct. 2026 | 26 oct. 2026 |
| P010 Valider et Réessayer | 12 oct. 2026 | 26 oct. 2026 |

---

## Backlog actif

Au début d'une session, Claude propose un ou deux sujets, avec ses raisons ; le sponsor valide
ou corrige. Les lignes avec une fiche sont des plans à mûrir ; les autres sont de simples idées.

| Sujet | Depuis | Priorité proposée | Fiche ou note |
|---|---|---|---|
| Séparer les données déjà mélangées dans un profil (par module) | 11 oct. 2026 | moyenne (P008 est livré) | idée ; voir P008 |
| Revue d'usage n° 2 (exports des deux enfants, effet de P001 sur « son / sont », « Décrire » en 6e) | 12 oct. 2026 | **haute**, vers le 26 oct. | revue d'usage n° 1 : historique Git de `pilotage.md` (11 oct.) |
| Gamification : règles génériques (points sur l'effort utile, maîtrise espacée, mission du jour, « Réparé ») | 11 oct. 2026 | moyenne, après P008 et la revue n° 2 | `plans/P009-gamification.md` |
| POC « signalements envoyés à une boîte externe » (canal à sens unique, sans prénom ; lève « aucun tiers » pour ce seul cas s'il est adopté) | 11 oct. 2026 | moyenne, après P003 | idée ; voir `plans/P003-signaler-un-probleme.md` |
| Tirage adaptatif par compétence fine (maîtrise de 0 à 1, tirage proportionnel à ce qui reste à acquérir, arbre de compétences par enfant) : le tirage actuel répète (« est » une fois sur deux en Être niv. 2) | 12 oct. 2026 | **haute** (atelier de cadrage, session dédiée) | idée ; analyse de la session du 12 oct. dans la conversation |
| Dictée répétable | 7 oct. 2026 | moyenne | `plans/P006-dictee-repetable.md` |
| Évaluations rejouées en boucle | 11 oct. 2026 | à revoir à la revue n° 2 | `plans/P007-evaluations-rejouees.md` |
| Limite de taille des modules : au-delà de 8 compétences, un deuxième module (le circuit en a 10, 105 Ko) | 11 oct. 2026 | moyenne | idée |
| Cacher aux enfants les deux modules CM2 (aucun enfant à ce niveau) | 11 oct. 2026 | basse | idée (réversible) |
| POC « dictée lue par le téléphone » (synthèse vocale locale) | 11 oct. 2026 | basse | idée |
| « À revoir aujourd'hui » : révision espacée dans la bibliothèque | 11 oct. 2026 | après 2 revues d'usage | idée |
| Renommer un profil | 11 oct. 2026 | basse | idée (l'historique est rattaché à l'id, pas au prénom) |
| Créer un module depuis miniprof, sans Claude Code | 12 oct. 2026 | basse | idée, techniquement difficile sans serveur ; voir P004 |
| Fiche de contrôle d'un module dans l'app | 6 oct. 2026 | basse | idée (la relecture dans la conversation suffit) |
| Pipeline sans Claude Code | 6 oct. 2026 | basse | `plans/P004-pipeline-sans-claude-code.md` |
| Fusion des sauvegardes | 6 oct. 2026 | basse | `plans/P005-fusion-des-sauvegardes.md` |

---

## Tâches du sponsor

| Tâche | Échéance |
|---|---|
| Sur l'appareil du CM1 : créer un profil « Test » pour tes essais ; l'enfant garde le profil actuel (son historique y est) | avant ton prochain essai de module |
| Proposer à la 6e 10 questions « S'entraîner > Décrire », niveau Échauffement, dans Zootopia | cette semaine |
| Ouvrir l'accès réseau de l'environnement cloud pour que Claude lise des ressources de référence (Eduscol…) : menu de l'environnement dans le titre de la session, Edit, Network access. Mode d'emploi : https://code.claude.com/docs/en/cloud-environments#network-access | avant la prochaine dictée |
| Autoriser les notifications de l'app Claude sur l'iPhone (pour être prévenu de la fin d'une exécution ; à vérifier à la première tâche lourde) | avant le prochain plan exécuté |
| Recette P008 sur l'iPhone : le choix du profil réapparaît une fois, puis après 30 min sans utilisation, y compris par un lien de module (4 étapes dans la fiche) | cette semaine |
| Recette P010 sur l'iPhone : dans une dictée, taper un mot faux, « Réessayer » : champ vide, « Valider » disparu, clavier ouvert | cette semaine |
| Relire le `README.md` : t'y retrouves-tu ? | quand tu veux |
| Exporter les données des deux appareils (Sauvegarde > Exporter et partager) et joindre les deux fichiers à la conversation Claude Code de la revue d'usage n° 2 | vers le 26 oct. |
