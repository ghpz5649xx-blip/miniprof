# Pilotage miniprof

Support des comités de pilotage. **Claude le met à jour à la fin de chaque session**, pour la
suivante (Claude n'existe que pendant une session : « avant chaque comité » veut donc dire « à la
fin du précédent »). Le sponsor le lit avant le comité. Règles de la gouvernance : `CLAUDE.md`,
« Gouvernance ».

---

## Comité n° 1 — à la date choisie par le sponsor

**Durée : 30 minutes.** Claude tient le temps : à l'échéance d'un point, il propose de trancher,
de reporter au comité suivant ou de prolonger (sur accord du sponsor).

| # | Point | Temps | Ce qu'on attend du sponsor |
|---|---|---|---|
| 1 | Ce qui ne va pas dans la gouvernance actuelle | 5 min | ton retour (je n'ai que mon analyse, plus bas) |
| 2 | Le rituel du comité | 10 min | décisions D1 à D4 |
| 3 | Météo et faits marquants | 3 min | rien, sauf question |
| 4 | Étape 12 (relecture des modules avant les enfants) : la poursuivre ou l'alléger | 7 min | décision D5 |
| 5 | Retour d'usage de la 6e | 3 min | action A4 |
| 6 | Relevé des décisions et des actions | 2 min | validation du relevé |

---

## 1. Ce qui ne va pas : mon analyse, à confronter à la tienne

- **Les décisions sont dispersées** dans les conversations, le `README.md`, le plan et la recette.
  Tu dois lire trois fichiers pour savoir où on en est, et rien ne dit clairement ce qui attend
  ta décision.
- **Je livre beaucoup, vite, sans point d'arrêt.** Le 6 octobre : 14 commits, une évolution
  (le gabarit) décidée et livrée dans la même conversation, sur un simple « oui parfait ».
- **Plusieurs sessions poussent en parallèle** (l'étape 12 avance dans une autre session pendant
  que celle-ci livrait le gabarit). Chacune décide de son côté.
- **Tu fais un travail de lecture qui devrait être le mien** : synthèse, priorités, risques.

---

## 2. Le rituel du comité : décisions attendues

Déjà en place dans ce commit (à valider ou à défaire en D2) : ce fichier, et la section
« Gouvernance » de `CLAUDE.md` (rôles, rituel, ce que Claude fait seul entre deux comités).

### D1 — Format du comité
- **Proposition** : une session que tu ouvres par le message « comité ». J'ouvre `pilotage.md`,
  je déroule l'ordre du jour, je tiens le temps. À la fin, j'écris le relevé (décisions,
  actions), je prépare le support du comité suivant, je commite et je pousse.
- Fréquence : à ta demande, idéalement une fois par semaine, ou avant toute nouvelle évolution.
- **Recommandation** : oui. Option : un skill `/comite` qui fait la même chose, inutile tant
  que le mot « comité » suffit.

### D2 — `pilotage.md`, seul point d'entrée pour toi
- **Proposition** : tu ne lis que ce fichier. Le `README.md` (« Où en est le projet ») et
  l'en-tête de `docs/recette.md` (« Reste à vérifier ») renvoient ici ; leurs listes sont
  reprises dans les actions ci-dessous. Les autres docs deviennent des annexes pour moi
  (le **pourquoi** détaillé reste dans le plan et `risques.md`).
- **Recommandation** : oui. C'est fait dans ce commit ; si tu refuses, je remets les deux
  listes en place.

### D3 — Ce que je fais seul entre deux comités
- **Proposition** :
  - **le service courant (« run »)**, à ta demande et sans attendre un comité :
    `/nouveau-module`, correction d'un module signalée par toi ou un enfant, réponse à une
    question, retour arrière (`git revert`) en cas d'incident en production ;
  - **les évolutions (« build »)** : seulement celles décidées en comité, avec le découpage
    validé. Une idée nouvelle, la tienne ou la mienne, va à l'ordre du jour du comité suivant ;
    je ne l'attaque pas dans la conversation où elle naît ;
  - **une seule session « build » à la fois** (fin des sessions qui avancent en parallèle).
- **Recommandation** : oui. Le coût : une idée attend le comité suivant, au lieu de partir tout
  de suite.

### D4 — Ton identité dans le dépôt
- Le dépôt est **public** (GitHub Pages gratuit). Aujourd'hui, aucun prénom réel n'y figure.
  Y écrire ton prénom, ton âge et ton employeur les rendrait lisibles par tous, et pour toujours
  (l'historique Git le garde).
- **Proposition** : dans le dépôt, tu es « le sponsor » ; je t'appelle par ton prénom et je te tutoie
  dans nos conversations. Ton profil (chef de projet, BA) est écrit sans nom ni employeur, pour
  que la session suivante sache comment te parler.
- **Recommandation** : oui. C'est ce que j'ai écrit en attendant ta décision.

---

## 3. Météo et faits marquants

**Météo : en service, au vert.** L'app et la création de modules depuis l'iPhone marchent. La
6e s'en sert depuis le 6 octobre. **Gouvernance : à l'orange** (objet de ce comité).

| Date | Fait marquant |
|---|---|
| 4 oct. | App v1 livrée : profils, leçons, entraînement, évaluations, bilan, sauvegarde (modules JSON). |
| 5 oct. | Modules HTML générés par Claude, suivis par miniprof (module circuit, 6e). |
| 6 oct. | `/nouveau-module` depuis l'iPhone : photos → page publiée → URL (module anglais Zootopia). |
| 6 oct. | Première utilisation par la 6e : 144 réponses, 9 évaluations d'anglais (6 à 9/10). |
| 6 oct. | Module anglais corrigé (a / an expliqué pas à pas), après la difficulté constatée. |
| 6 oct. | Étape 12, unité 1 : un module « brouillon » est caché aux enfants tant qu'il n'est pas relu. |
| 6 oct. | Gabarit commun des modules HTML et `tools/tirage.py` (milliers de questions vérifiées). |

Modules en ligne : anglais 6e (Zootopia), circuit électrique 6e (HTML) ; division euclidienne
et grands nombres CM2 (JSON).

---

## 4. Étape 12 : la poursuivre ou l'alléger (D5)

- **Le besoin (ta demande du 6 oct.)** : relire un module avant que les enfants le voient,
  vite, avec quelques exercices et leurs réponses en face.
- **Fait** : unité 1, le statut brouillon (module caché aux enfants tant qu'il n'est pas validé).
- **Reste, tel que prévu** : 2. un écran parent avec la fiche de contrôle des modules JSON ;
  3. la même fiche dans les pages HTML (mode `#controle`) ; 4. le skill publie en brouillon,
  et tu valides par un message.
- **Ce qui a changé depuis** : `tools/tirage.py` tire déjà des milliers de questions avec le
  vrai code de la page et affiche des exemples « question → bonne réponse ». Il couvre une bonne
  part de la fiche de contrôle prévue pour les modules HTML (unité 3). Et tu ne crées plus de
  modules JSON (unité 2).

| Option | Contenu | Coût | Ce que tu perds |
|---|---|---|---|
| A. Poursuivre | unités 2, 3 et 4 | 3 sessions, 2 recettes iPhone, un écran de plus dans l'app, une règle de plus au contrat HTML | rien |
| **B. Alléger** | unité 4 seule : le module est publié en brouillon ; ma réponse te donne les exemples tirés par `tirage.py` (questions + réponses) ; tu valides par « valide <id> » | 1 session, 1 recette iPhone | la fiche dans l'app (tu relis dans la conversation) ; les modules JSON n'ont pas de fiche (on n'en crée plus) |
| C. Arrêter | on garde l'unité 1 | aucun | aujourd'hui, un brouillon ne peut sortir que si je retire son id à la main |

**Recommandation : B.** Même valeur (tu relis avant les enfants, avec les questions produites par
le vrai code), pour un tiers du coût. Les unités 2 et 3 restent possibles plus tard.

---

## 5. Retour d'usage de la 6e

- Export du 6 octobre : « Décrire un animal » réussi à 43 % du premier coup ; erreurs surtout
  sur a / an devant l'adjectif. Le module a été corrigé le jour même.
- Pour savoir si la correction aide, il faut un nouvel export (action A4).

---

## Actions

| # | Action | Porteur | Échéance | Statut |
|---|---|---|---|---|
| A1 | Lire ce support avant le comité n° 1 | Sponsor | comité n° 1 | à faire |
| A2 | Au prochain `/nouveau-module` : vérifier que la réponse cite des exemples tirés à relire (recette G.5) | Sponsor | prochain module | à faire |
| A3 | Jouer le module circuit sur l'iPhone (recette 8.5 à 8.8), seulement s'il doit être envoyé à un enfant | Sponsor | si besoin | à faire |
| A4 | Faire un export des données de la 6e après une semaine d'usage (Sauvegarde > Exporter), puis me le transmettre en session | Sponsor | vers le 13 oct. | à faire |
| A5 | Appliquer les décisions du comité n° 1, puis préparer le support du comité n° 2 | Claude | fin du comité n° 1 | à faire |

---

## Relevé des décisions

| Date | Comité | Décision |
|---|---|---|
| 6 oct. 2026 | (hors comité) | Gouvernance en comités de pilotage. Rôles : Claude est chef de projet, architecte fonctionnel, développeur, PMO, testeur, responsable de production et support ; le parent est sponsor et client. Chaque session se conclut par des décisions du sponsor et des actions. Claude tient le temps. |
