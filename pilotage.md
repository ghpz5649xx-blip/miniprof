# Pilotage miniprof

Support des comités de pilotage. **Claude le met à jour à la fin de chaque session**, pour la
suivante. Le sponsor le lit avant le comité. Règles de la gouvernance : `CLAUDE.md`,
« Gouvernance ».

**Évolution en cours : étape 12 allégée (unité 4 : publication en brouillon, validation par
message).** Une session qui voit cette ligne ne lance pas d'autre évolution (décision D3).

---

## Comité n° 2 — à la date choisie par le sponsor

**Durée : 30 minutes.** Ordre du jour provisoire, complété à la fin de chaque session :

| # | Point | Temps | Ce qu'on attend de toi |
|---|---|---|---|
| 1 | Bilan de l'étape 12 allégée (si livrée) : un vrai module publié en brouillon puis validé | 5 min | ton retour d'usage |
| 2 | Refonte du `README.md` (A6) | 5 min | ta relecture |
| 3 | Retour d'usage de la 6e : l'export (A4) dit-il si la correction du a / an a aidé ? | 10 min | l'export |
| 4 | Premier module CE2/CM1 : comment ça s'est passé | 5 min | ton retour |
| 5 | Backlog : priorités | 3 min | arbitrage |
| 6 | Relevé des décisions et des actions | 2 min | validation |

---

## Météo et faits marquants

**Météo : service au vert ; gouvernance au vert** (rituel décidé au comité n° 1).

| Date | Fait marquant |
|---|---|
| 4 oct. | App v1 livrée : profils, leçons, entraînement, évaluations, bilan, sauvegarde (modules JSON). |
| 5 oct. | Modules HTML générés par Claude, suivis par miniprof (module circuit, 6e). |
| 6 oct. | `/nouveau-module` depuis l'iPhone : photos → page publiée → URL (module anglais Zootopia). |
| 6 oct. | Première utilisation par la 6e : 144 réponses, 9 évaluations d'anglais (6 à 9/10). |
| 6 oct. | Module anglais corrigé (a / an expliqué pas à pas), après la difficulté constatée. |
| 6 oct. | Étape 12, unité 1 : un module « brouillon » est caché aux enfants tant qu'il n'est pas relu. |
| 6 oct. | Gabarit commun des modules HTML et `tools/tirage.py` (milliers de questions vérifiées). |
| 6 oct. | Comité n° 1 : gouvernance adoptée (D1 à D4, D6), étape 12 allégée (D5), pipeline sans Claude Code mis au backlog (D7). |

Modules en ligne : anglais 6e (Zootopia), circuit électrique 6e (HTML) ; division euclidienne
et grands nombres CM2 (JSON). Aucun module encore au niveau CE2/CM1.

---

## Regard du chef de projet

- **Priorité du moment** : l'étape 12 allégée, avant le premier module CE2/CM1 attendu ce
  week-end. Ce module sera ainsi le premier publié en brouillon, relu par toi avant ton enfant.
- **Le vrai risque reste la qualité du contenu** (une réponse fausse apprise par un enfant) :
  l'étape 12 y répond directement.
- **Vérifications sur l'iPhone en retard** (A2, A3) : elles se feront naturellement avec le
  module de ce week-end.

---

## Backlog (idées notées, pas engagées)

| # | Idée | Origine | Priorité | Note |
|---|---|---|---|---|
| B1 | Pipeline sans Claude Code : robot de contrôle GitHub, puis POC de l'API Claude payée à l'usage | assessment du comité n° 1 (D7) | basse | l'assessment complet (options, SWOT, coûts) est dans l'historique de ce fichier, commit « Pilotage : retours du sponsor, assessment… » |
| B2 | Étape 12, unités 2 et 3 : fiche de contrôle dans l'app (modules JSON, puis HTML) | plan de l'étape 12 | basse | inutiles tant que la relecture dans la conversation suffit (D5) |

---

## Actions

| # | Action | Porteur | Échéance | Statut |
|---|---|---|---|---|
| A2 | Au prochain `/nouveau-module` : vérifier que la réponse cite des exemples tirés à relire (recette G.5) | Sponsor | ce week-end | à faire |
| A3 | Jouer le module circuit sur l'iPhone (recette 8.5 à 8.8), seulement s'il doit être envoyé à un enfant | Sponsor | si besoin | à faire |
| A4 | Faire un export des données de la 6e après une semaine d'usage (Sauvegarde > Exporter), puis me le transmettre en session | Sponsor | vers le 13 oct. | à faire |
| A6 | Refondre le `README.md` en documentation de reprise : à quoi sert le projet, comment il marche (app, modules, pipeline avec un LLM, gouvernance), comment s'en servir | Claude | avant le comité n° 2 | à faire |
| A7 | Étape 12 allégée (unité 4) : un nouveau module est publié en brouillon, la réponse donne les exemples à relire, « valide <id> » le rend visible aux enfants | Claude | avant ce week-end | en cours |
| A8 | Créer le premier module CE2/CM1 avec `/nouveau-module` (il sortira en brouillon), le relire, puis le valider | Sponsor | ce week-end | à faire |

Actions closes : A1 (support lu), A5 (décisions du comité n° 1 appliquées).

---

## Relevé des décisions

| Date | Comité | Décision |
|---|---|---|
| 6 oct. 2026 | (hors comité) | Gouvernance en comités de pilotage. Rôles : Claude est chef de projet, architecte fonctionnel, développeur, PMO, testeur, responsable de production et support ; le parent est sponsor et client. Chaque session se conclut par des décisions du sponsor et des actions. Claude tient le temps. |
| 6 oct. 2026 | (hors comité) | Le `README.md` est la documentation de reprise du projet (pour qui le découvre, ou pour le sponsor dans cinq ans), mode d'emploi compris ; pas de guide utilisateur séparé ; l'état du projet est dans `pilotage.md`. |
| 6 oct. 2026 | (hors comité) | Claude assume le rôle de chef de projet : synthèse, priorités, risques, regard critique sur l'avancement et propositions d'amélioration. |
| 6 oct. 2026 | n° 1 | D1 : le comité est une session ouverte par le sponsor, 30 minutes ; Claude tient le temps, écrit le relevé et prépare le support suivant. |
| 6 oct. 2026 | n° 1 | D2 : `pilotage.md` est le seul document que lit le sponsor. |
| 6 oct. 2026 | n° 1 | D3 : service courant en parallèle sans limite ; une seule évolution à la fois, annoncée en tête de `pilotage.md` ; une idée nouvelle va au comité suivant ou au backlog. |
| 6 oct. 2026 | n° 1 | D4 : dans le dépôt public, le parent est « le sponsor », sans nom. |
| 6 oct. 2026 | n° 1 | D5 : étape 12 allégée (option B) : unité 4 seule ; unités 2 et 3 au backlog. |
| 6 oct. 2026 | n° 1 | D6 : cadre des POC : proposés par Claude ou demandés par le sponsor, go du sponsor, dossier `poc/<sujet>/` isolé de l'app, des modules et des données, une session au plus, démo + conclusion en cinq lignes, jamais mis en production tel quel. |
| 6 oct. 2026 | n° 1 | D7 : le pipeline sans Claude Code va au backlog, priorité basse. |
| 6 oct. 2026 | n° 1 | Dans les échanges, Claude pose **une question à la fois**. |
