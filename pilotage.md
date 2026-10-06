# Pilotage miniprof

Support des comités de pilotage. **Claude le met à jour à la fin de chaque session**, pour la
suivante (Claude n'existe que pendant une session : « avant chaque comité » veut donc dire « à la
fin du précédent »). Le sponsor le lit avant le comité. Règles de la gouvernance : `CLAUDE.md`,
« Gouvernance ».

---

## Comité n° 1 — à la date choisie par le sponsor

**Durée : 30 minutes.** Je tiens le temps : à l'échéance d'un point, je propose de trancher, de
reporter au comité suivant ou de prolonger (avec ton accord).

| # | Point | Temps | Ce qu'on attend de toi |
|---|---|---|---|
| 1 | Tes retours du 6 octobre : relevé, et la fin de ta phrase (« … mais ») | 3 min | compléter, valider le relevé |
| 2 | Le rituel et le travail entre deux comités | 7 min | décisions D1 à D4 |
| 3 | Le cadre des POC | 3 min | décision D6 |
| 4 | **Assessment : un pipeline de création de modules sans Claude Code** | 10 min | décision D7 |
| 5 | Étape 12 (relecture des modules avant les enfants) | 5 min | décision D5 |
| 6 | Météo, retour d'usage, relevé des décisions et actions | 2 min | validation du relevé |

---

## 1. Tes retours du 6 octobre (relevé à valider)

- **Ce qui te gênait le plus** : ne pas savoir précisément où on en était, et ne pas comprendre
  ce que tu devais faire en lisant le `README.md`. Réponse : ce fichier (état, décisions,
  actions), et la refonte du README (action A6).
- **Rôle du `README.md`** : documentation de reprise. Il explique comment tout fonctionne à
  quelqu'un qui découvre le dépôt, ou à toi dans cinq ans. Il n'y a pas de guide utilisateur à
  part : le mode d'emploi reste dans le README. Le projet reste lié à l'usage d'un LLM, même
  une fois fini : le README doit donc expliquer ce pipeline aussi.
- **Mon rôle** : faire le travail de chef de projet (synthèse, priorités, risques), porter un
  regard critique sur la façon dont le projet avance et proposer ce qui le rendrait plus
  efficace. Je le fais dans la section « Regard du chef de projet » de chaque support.
- **POC** : je peux en proposer, tu peux en demander ; le cadre est proposé en D6.
- **Ta phrase s'arrêtait sur « Dans l'ensemble je suis plutôt d'accord avec ton constat
  mais… »** : à compléter en début de comité.

---

## 2. Le rituel et le travail entre deux comités

### D1 — Format du comité
- **Proposition** : une session que tu ouvres par le message « comité ». Je déroule l'ordre du
  jour et je tiens le temps. À la fin, j'écris le relevé (décisions, actions), je prépare le
  support du comité suivant, puis je commite et je pousse.
- Fréquence : à ta demande, idéalement une fois par semaine, ou avant toute nouvelle évolution.
- **Recommandation** : oui.

### D2 — `pilotage.md`, seul point d'entrée pour toi
- **Proposition** : tu ne lis que ce fichier. Les autres docs sont des annexes : le README pour
  la reprise du projet, le plan et `risques.md` pour le pourquoi détaillé.
- **Recommandation** : oui (déjà en place ; si tu refuses, je reviens en arrière).

### D3 — Le travail entre deux comités, et les sessions en parallèle
Aujourd'hui, deux sessions ont avancé chacune de leur côté (l'étape 12 d'un côté, le gabarit de
l'autre), sans se voir. Je propose trois sortes de sessions :

| Sorte | Quoi | En parallèle ? | Règle |
|---|---|---|---|
| **Service courant** (« run ») | `/nouveau-module`, correction d'un module, question, `git revert` en cas d'incident | oui, sans limite | ne touche que les modules, l'index et les faits marquants ; se met à jour avant de pousser |
| **Évolution** (« build ») | ce que le comité a décidé, et rien d'autre | **une seule à la fois** | au début, j'écris en tête de ce fichier « Évolution en cours : <sujet> », et je l'efface à la fin. Une session qui voit cette ligne ne lance pas d'autre évolution. |
| **POC** | voir D6 | oui | ne touche jamais l'app ni les modules |

- Une idée nouvelle, la tienne ou la mienne, va à l'ordre du jour du comité suivant. Je ne
  l'attaque pas dans la conversation où elle naît.
- **Recommandation** : oui. Le coût : une idée attend le comité suivant ; une urgence reste
  possible par le service courant.

### D4 — Ton identité dans le dépôt
- Le dépôt est **public**. Y écrire ton prénom, ton âge et ton employeur les rendrait lisibles
  par tous, et pour toujours (l'historique Git le garde).
- **Proposition** : dans le dépôt, tu es « le sponsor » ; dans nos conversations, je t'appelle
  par ton prénom et je te tutoie.
- **Recommandation** : oui (c'est ce qui est écrit aujourd'hui).

---

## 3. Le cadre des POC (D6)

Un POC sert à **voir pour décider** : il répond à une question qu'on ne peut pas trancher sur le
papier (est-ce faisable, est-ce que ça rend bien sur l'iPhone, combien ça coûte vraiment, est-ce
que l'enfant comprend).

- **Déclenchement** : je propose un POC dans le support (section « POC proposés ») quand une
  décision dépend d'une telle question et que le POC tient en une session. Tu peux aussi en
  demander un à tout moment. Dans les deux cas, c'est toi qui dis go.
- **Cadre** :
  - un dossier `poc/<sujet>/`, autonome, qui ne touche ni l'app, ni les modules, ni les données
    des enfants. Il est en ligne (tu peux l'ouvrir sur l'iPhone) mais aucun lien n'y mène ;
  - une session au plus ;
  - le livrable : une URL de démonstration, et une conclusion en cinq lignes dans ce fichier.
- **Sortie** : tu décides go (il devient une évolution, refaite proprement) ou no-go (on
  supprime le dossier, la conclusion reste ici). Un POC n'est jamais promu tel quel.
- **Recommandation** : oui.

---

## 4. Assessment : un pipeline de création de modules sans Claude Code (D7)

**La question** : aujourd'hui, un module naît ainsi : photos → `/nouveau-module` dans Claude
Code (abonnement Pro) → page contrôlée et publiée. Existe-t-il un pipeline moins cher, ou qui ne
dépende pas de Claude Code, et qui marche sans trop de difficulté ?

**Ce que Claude Code apporte vraiment** (et qu'il faut remplacer) :
1. l'écriture de la page, à partir des photos : c'est le cœur, et ça demande un bon modèle ;
2. les contrôles, avec correction en boucle : `check_html.py`, `tirage.py`, `build_index.py`,
   tests ;
3. la publication : commit et push sur GitHub, depuis l'iPhone.

Les points 2 et 3 ne demandent **pas** de LLM. Les sortir de Claude Code rendrait n'importe quel
pipeline possible.

### Les options

| | Option | Comment | Coût | Qualité | Ton travail par module | À construire |
|---|---|---|---|---|---|---|
| O0 | **Statu quo** | Claude Code sur l'iPhone | abonnement Pro (fixe, déjà payé), dans la limite du quota | la meilleure | photos + 1 message + relecture | rien |
| O1 | **App Claude, sans Claude Code** | un « Projet » Claude qui contient le gabarit et le contrat ; photos → la page HTML ; tu la déposes sur GitHub depuis l'iPhone ; un **robot GitHub** (GitHub Actions, gratuit sur un dépôt public) lance les contrôles et met l'index à jour | même abonnement, ou l'offre gratuite de Claude (limitée) | proche de O0 au premier jet, mais sans correction en boucle : si un contrôle échoue, tu recopies le message dans la conversation | photos + déposer un fichier + relire le résultat du robot | le robot de contrôle (1 session) |
| O2 | **LLM gratuit** (ChatGPT, Gemini, Le Chat) | même circuit que O1 | 0 € | plus faible : une page de 40 Ko de JS est à la limite des offres gratuites. La voie JSON (`prompt.py`, `validate.py`), conçue pour ces LLM, existe déjà, mais elle demande le Mac. | plus d'allers-retours | le robot de contrôle |
| O3 | **API Claude payée à l'usage** | un script sur le Mac (`tools/generer.py`) : photos → API → page → contrôles → correction automatique en boucle → push | environ **0,3 à 1,5 $ par module** selon le modèle (estimation, voir plus bas), sans abonnement | égale à O0 (mêmes modèles) | photos copiées sur le Mac + 1 commande | le script (1 à 2 sessions) + une clé API |
| O4 | **Modèle local** (sur le Mac) | idem O3, sans réseau | 0 € | insuffisante aujourd'hui pour lire des photos de cahier et écrire 40 Ko de JS juste | lourd | beaucoup |

**Estimation O3** (tarifs publics de l'API au 25 sept. 2026, en dollars par million de jetons,
entrée / sortie : Sonnet 5.5, 2 / 10 ; Opus 5.5, 4 / 20 ; Haiku 4.5, 1 / 5). Un module : 3 photos
(environ 5 000 jetons) + gabarit et contrat (environ 12 000), avec 3 à 5 tours de correction,
donne de l'ordre de 100 000 jetons lus et 30 000 écrits. Soit environ 0,50 $ avec Sonnet, 1 $
avec Opus, 0,25 $ avec Haiku (qualité nettement moindre). À deux modules par semaine : moins de
10 $ par mois. **À mesurer par un POC avant de s'y fier.**

### SWOT du pipeline « sans Claude Code »

| Forces | Faiblesses |
|---|---|
| Le gabarit et `tirage.py` portent déjà l'essentiel du savoir-faire : n'importe quel LLM part d'une base solide. Les contrôles sont du Python, sans LLM. Le site est statique, donc rien à héberger. | Sans boucle de correction automatique (O1, O2), chaque erreur te revient. O3 demande le Mac et une clé API. La qualité dépend du modèle : c'est là que se joue la valeur pour les enfants. |
| **Opportunités** | **Menaces** |
| Le robot GitHub sert à **toutes** les options, O0 comprise : il contrôle chaque push, même fait depuis l'iPhone ou par une autre session. O3 devient la voie de sortie si tu arrêtes l'abonnement une fois le produit fini. | Photos de cahiers envoyées à un tiers : avec les offres gratuites, elles peuvent servir à l'entraînement selon les réglages. Les prix et les quotas changent. Une page générée par un LLM plus faible peut être fausse sur le fond, ce qu'aucun contrôle automatique ne voit. |

### Recommandation
1. **Rester sur O0** tant que tu as l'abonnement : c'est la meilleure qualité, et le cœur de la
   valeur.
2. **Construire le robot de contrôle GitHub** (évolution, 1 session). Il sert tout de suite (un
   push qui casse le contrat est signalé, quelle que soit la session) et il ouvre O1 et O3.
3. **POC O3** (1 session, une fois le robot fait) : générer un vrai module par l'API, mesurer le
   coût réel et la qualité contre un module fait par Claude Code. C'est la voie de sortie
   documentée pour « le produit est fini ».
4. Écarter O2 et O4 : le gain est nul ou faible, et le risque sur la qualité est fort.

**D7 — à trancher** : (a) recommandation complète ; (b) robot seul ; (c) rien pour l'instant.

---

## 5. Étape 12 : la poursuivre ou l'alléger (D5)

- **Le besoin (ta demande du 6 oct.)** : relire un module avant que les enfants le voient,
  vite, avec quelques exercices et leurs réponses en face.
- **Fait** : unité 1, le statut brouillon (module caché aux enfants tant qu'il n'est pas validé).
- **Reste, tel que prévu** : 2. un écran parent avec la fiche de contrôle des modules JSON ;
  3. la même fiche dans les pages HTML ; 4. le skill publie en brouillon, et tu valides par un
  message.
- **Ce qui a changé** : `tools/tirage.py` affiche déjà des exemples « question → bonne réponse »
  tirés du vrai code de la page (une bonne part de l'unité 3), et tu ne crées plus de modules
  JSON (unité 2).

| Option | Contenu | Coût | Ce que tu perds |
|---|---|---|---|
| A. Poursuivre | unités 2, 3 et 4 | 3 sessions, 2 recettes iPhone | rien |
| **B. Alléger** | unité 4 seule : publication en brouillon ; ma réponse te donne les exemples de `tirage.py` ; tu valides par « valide <id> » | 1 session, 1 recette iPhone | la fiche dans l'app (tu relis dans la conversation) |
| C. Arrêter | on garde l'unité 1 | aucun | un brouillon ne sort que si je retire son id à la main |

**Recommandation : B.** Même valeur pour un tiers du coût ; les unités 2 et 3 restent possibles
plus tard.

---

## 6. Météo et faits marquants

**Météo : service au vert** (l'app et la création de modules depuis l'iPhone marchent ; la 6e
s'en sert depuis le 6 octobre). **Gouvernance : à l'orange**, en cours de mise en place.

| Date | Fait marquant |
|---|---|
| 4 oct. | App v1 livrée : profils, leçons, entraînement, évaluations, bilan, sauvegarde (modules JSON). |
| 5 oct. | Modules HTML générés par Claude, suivis par miniprof (module circuit, 6e). |
| 6 oct. | `/nouveau-module` depuis l'iPhone : photos → page publiée → URL (module anglais Zootopia). |
| 6 oct. | Première utilisation par la 6e : 144 réponses, 9 évaluations d'anglais (6 à 9/10). |
| 6 oct. | Module anglais corrigé (a / an expliqué pas à pas), après la difficulté constatée. |
| 6 oct. | Étape 12, unité 1 : un module « brouillon » est caché aux enfants tant qu'il n'est pas relu. |
| 6 oct. | Gabarit commun des modules HTML et `tools/tirage.py` (milliers de questions vérifiées). |
| 6 oct. | Gouvernance en comités de pilotage ; ce fichier. |

Modules en ligne : anglais 6e (Zootopia), circuit électrique 6e (HTML) ; division euclidienne
et grands nombres CM2 (JSON). **Retour d'usage** : « Décrire un animal » réussi à 43 % du premier
coup le 6 octobre (surtout a / an devant l'adjectif) ; module corrigé ; nouvel export attendu
(A4) pour mesurer l'effet.

---

## Regard du chef de projet

- **Rythme** : en trois jours, beaucoup a été livré et peu a été vérifié par toi sur l'iPhone
  (actions A2 et A3 ouvertes). Je propose de ne lancer aucune nouvelle évolution tant que le
  comité n° 1 n'a pas tranché D1 à D7.
- **Le vrai risque du projet est la qualité du contenu** (une réponse fausse apprise par un
  enfant), pas la technique. Les décisions D5 et D7 sont à juger d'abord sous cet angle.
- **Dépendance à Claude Code** : tout le pipeline passe aujourd'hui par lui. Le robot de
  contrôle (D7) réduit cette dépendance à la seule écriture des pages.
- **Le deuxième enfant (CE2/CM1) n'a aucun module à son niveau** : les deux modules de maths
  sont de CM2. À discuter : est-ce un besoin du moment ?

---

## Actions

| # | Action | Porteur | Échéance | Statut |
|---|---|---|---|---|
| A1 | Lire ce support avant le comité n° 1 | Sponsor | comité n° 1 | à faire |
| A2 | Au prochain `/nouveau-module` : vérifier que la réponse cite des exemples tirés à relire (recette G.5) | Sponsor | prochain module | à faire |
| A3 | Jouer le module circuit sur l'iPhone (recette 8.5 à 8.8), seulement s'il doit être envoyé à un enfant | Sponsor | si besoin | à faire |
| A4 | Faire un export des données de la 6e après une semaine d'usage (Sauvegarde > Exporter), puis me le transmettre en session | Sponsor | vers le 13 oct. | à faire |
| A5 | Appliquer les décisions du comité n° 1, puis préparer le support du comité n° 2 | Claude | fin du comité n° 1 | à faire |
| A6 | Refondre le `README.md` en documentation de reprise : à quoi sert le projet, comment il marche (app, modules, pipeline avec un LLM, gouvernance), comment s'en servir | Claude | proposé au comité n° 1, livré avant le comité n° 2 | à faire |

---

## Relevé des décisions

| Date | Comité | Décision |
|---|---|---|
| 6 oct. 2026 | (hors comité) | Gouvernance en comités de pilotage. Rôles : Claude est chef de projet, architecte fonctionnel, développeur, PMO, testeur, responsable de production et support ; le parent est sponsor et client. Chaque session se conclut par des décisions du sponsor et des actions. Claude tient le temps. |
| 6 oct. 2026 | (hors comité) | Le `README.md` est la documentation de reprise du projet (pour qui le découvre, ou pour le sponsor dans cinq ans), mode d'emploi compris ; pas de guide utilisateur séparé ; l'état du projet est dans `pilotage.md`. |
| 6 oct. 2026 | (hors comité) | Claude assume le rôle de chef de projet : synthèse, priorités, risques, regard critique sur l'avancement et propositions d'amélioration. |
| 6 oct. 2026 | (hors comité) | Des POC peuvent être proposés par Claude ou demandés par le sponsor ; le sponsor dit go. Cadre à valider (D6). |
