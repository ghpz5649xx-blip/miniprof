# Pilotage miniprof

Support des comités de pilotage. **Claude le met à jour à la fin de chaque session**, pour la
suivante. Le sponsor le lit avant le comité. Règles de la gouvernance : `CLAUDE.md`,
« Gouvernance ».

**Évolution en cours : aucune.** Aucune autre évolution décidée : la suite se décide au comité n° 2.

---

## Comité n° 2 — à la date choisie par le sponsor

**Durée : 30 minutes.** Ordre du jour provisoire, complété à la fin de chaque session :

| # | Point | Temps | Ce qu'on attend de toi |
|---|---|---|---|
| 1 | Bilan de la période (synthèse ci-dessous) : brouillon et validation, README, premiers modules CM1 | 4 min | ton retour d'usage, validation des actions closes |
| 2 | Revue d'usage n° 1 (exports du 11 oct., analyse ci-dessous) | 6 min | décision D14, action A13 |
| 3 | Module « dictée » (D8) : retour d'usage ; faut-il l'évolution B4 ? | 4 min | ton retour |
| 4 | Challenges et opportunités vus par le chef de projet | 12 min | décisions D9 à D13 |
| 5 | Backlog : priorités | 2 min | arbitrage |
| 6 | Relevé des décisions et des actions | 2 min | validation |

---

## Synthèse de la période (6 au 11 octobre)

**Ce qui s'est passé**
- **Gouvernance** : comités de pilotage, `pilotage.md` seul support, une question à la fois,
  service courant à la demande, une seule évolution à la fois, cadre des POC (comité n° 1).
- **Livré** : relecture avant les enfants (un nouveau module sort en brouillon, avec une
  question-réponse par compétence et par niveau ; « valide » le publie), gabarit commun et
  `tools/tirage.py`, `README.md` refondu en documentation de reprise.
- **Service courant, à ton rythme** : 4 modules créés (Paddington 2, tables de 3-6-9, dictée 5,
  et le premier module CM1), 4 corrections (a / an expliqué pas à pas ; circuit : dessin de
  schéma, dérivation dès le niveau 1, DEL). Chaque nouveau module est passé par le brouillon puis
  ta validation, une fois après une correction (« au-déssus »).
- **Ce qui a bien marché** : la boucle courte « tu signales, je corrige, c'est en ligne dans la
  minute » (série / dérivation corrigée et mesurée le jour même) ; la relecture des
  questions-réponses tirées du vrai code.
- **Ce qui a moins bien marché** : des réponses envoyées dans la mauvaise session (sessions en
  parallèle) ; le tableau des faits marquants qui s'allonge ; aucune mesure encore de l'effet sur
  les enfants (A4 en attente).

---

## Revue d'usage n° 1 (exports des deux appareils, 11 octobre)

Analyse faite avec `tools/analyse.py` ; les exports restent hors du dépôt (données personnelles).

| | 6e | CM1 |
|---|---|---|
| Usage | 203 réponses : Zootopia (6 oct.), Paddington 2 (8 oct.) ; **rien depuis le 8 oct.** | 248 réponses du 11 oct. : tables (141), dictée 5 (107) |
| Réussi | couleurs 100 %, animaux 88 %, épeler 81 %, he / she / it 81 % | tables de 3, 6 et 9 : **10/10 au niveau 3**, 96 % sur 85 essais de la table de 3 ; noms de la dictée 95 % |
| À travailler | **« Décrire » (adjectif + a / an)** : 43 % dans Zootopia (28 essais), 36 % dans Paddington (11). Erreurs : l'article devant l'adjectif, puis l'ordre adjectif-nom | avoir et être (≈ 70 % : « êtes » sans accent, « sont ») ; nature des mots (69 %) ; écrire conduire, regarder, s'arrêter (69 %) |

**Constats**
1. **La difficulté de la 6e est la même dans deux modules** : décrire un nom avec un adjectif
   (« an orange fox », « a big umbrella »). C'est un vrai point de la leçon, pas un défaut de
   module. La correction du a / an (6 oct. après-midi) est arrivée après sa seule séance sur
   Zootopia (6 oct. matin) : **on ne peut pas encore mesurer son effet**.
2. **Évaluations enchaînées pour la note** : en 6e, 8 évaluations Zootopia en 11 minutes (4 à
   9 secondes par question). Elle rejoue pour améliorer la note plutôt que pour réviser. En
   Paddington, « personnages » à 40 % : questions sur des personnages d'un film peut-être pas
   encore vu.
3. **Données mélangées sur l'appareil du CM1** : le profil porte le prénom du sponsor, et ses
   tests (circuit, Paddington, division : 160 réponses) s'y mêlent aux réponses de l'enfant. Le
   bilan de l'enfant est faussé. Les modules CM1 permettent de les séparer à la main cette fois,
   pas à l'avenir.

**Actions et décision proposées**
- **A13** (toi) : sur l'appareil du CM1, créer un profil à son prénom ; garder ton profil pour
  tes essais (ou l'aperçu). Rien n'est perdu : l'historique reste sur ton profil.
- **A14** (toi, puis la 6e) : lui proposer 10 questions « S'entraîner > Décrire », niveau
  Échauffement, dans Zootopia (la méthode a / an y est expliquée pas à pas). Je mesure à la
  prochaine revue ; si « Décrire » reste sous 60 %, je propose un petit module dédié.
- **D14 — Évaluations rejouées en boucle** : (a) ne rien changer, en parler avec elle ; (b) dans
  les modules HTML, après une évaluation, proposer d'abord de s'entraîner sur la compétence la
  plus faible (le bouton existe), et afficher « Tu as déjà fait 3 évaluations : entraîne-toi
  d'abord » à partir de la 4e en une heure ; (c) limiter à une évaluation par jour et par module.
  Coût : (b) 1 session (gabarit + modules existants) ; (c) idem, mais frustrant.
  **Recommandation : (a) d'abord**, (b) si ça continue à la prochaine revue.
- **Prochains modules CM1** : les tables de 3, 6 et 9 sont sues ; la suite naturelle est la
  table de 7 et 8. La prochaine dictée peut reprendre avoir et être.

---

## Challenges et opportunités (regard du chef de projet)

**Challenges**
1. **On ne mesure pas encore si ça marche.** On produit des modules, mais personne ne regarde le
   bilan des enfants. Sans revue d'usage, on ne sait pas quoi corriger ni quoi refaire (D9).
2. **Le contenu sans source vérifiée.** Paddington 2 (faits du film) et les tables CM1 (programme
   non lu) reposent sur ma seule connaissance. La relecture te revient : elle doit rester rapide
   pour ne pas devenir une corvée.
3. **Le module circuit grossit** : 10 compétences et 105 Ko, pour un contrat qui en prévoit 2 à 8.
   Chaque ajout se fait par correction d'une page « jetable » de plus en plus lourde : risque de
   régression et de lecture difficile pour l'enfant (D12).
4. **Les sessions en parallèle se croisent** : une réponse arrive dans une autre session que celle
   qui a posé la question. Le service courant en parallèle reste utile, mais une session doit
   finir par une question claire, rattachée à son module.
5. **`pilotage.md` s'allonge** : le tableau des faits marquants dépasse 20 lignes (D13).

**Opportunités**
1. **La dictée lue par le téléphone.** La synthèse vocale du navigateur (sans réseau sur
   l'iPhone) permettrait à ton fils de faire sa dictée seul, le téléphone lisant les phrases.
   C'est la question idéale pour un POC (D10).
2. **Réviser au bon moment.** Une rubrique « À revoir aujourd'hui » dans la bibliothèque, qui
   ressort les compétences ratées de tous les modules quelques jours plus tard (révision
   espacée). Gros gain pédagogique, mais évolution de l'app : à décider après la revue d'usage
   (D11).
3. **Une routine hebdomadaire** : la liste de mots et la leçon de la semaine deviennent chacune un
   module, le week-end. C'est déjà ce qui se dessine ; B4 la rendrait plus fiable.
4. **Ranger la bibliothèque** : les deux modules CM2 (JSON) ne correspondent à aucun des enfants
   cette année. Les cacher allégerait la bibliothèque, sans rien perdre (ils restent dans le dépôt).

### Décisions proposées pour le comité n° 2

| # | Proposition | Coût | Ce qu'on perd | Recommandation |
|---|---|---|---|---|
| D9 | **Revue d'usage à chaque comité** : tu fais un export des deux enfants avant le comité, je l'analyse (`tools/analyse.py`) et j'en tire 3 constats et 1 à 3 corrections de modules | 2 minutes pour toi par comité ; 10 minutes de comité | rien | oui |
| D10 | **POC « dictée lue par le téléphone »** (synthèse vocale locale, dans `poc/dictee-vocale/`) : voir si la voix française de l'iPhone lit bien une dictée, phrase par phrase | 1 session ; 10 minutes d'essai pour toi | rien (un POC n'est jamais mis en production tel quel) | oui |
| D11 | **« À revoir aujourd'hui »** (révision espacée dans la bibliothèque) | 2 à 3 sessions, 1 recette iPhone ; aucun changement du format des données (tout est recalculé depuis le journal) | rien | au backlog, à reprendre après 2 revues d'usage (D9) |
| D12 | **Limite de taille des modules** : au-delà de 8 compétences, un nouvel ajout va dans un deuxième module (ex. « circuit électrique 2 : DEL et dessin ») ; on n'enlève rien au module actuel | aucun aujourd'hui | un module unique par chapitre | oui |
| D13 | **Hygiène de `pilotage.md`** : je ne garde que les faits marquants depuis le comité précédent ; les plus anciens restent dans l'historique Git | aucun | la liste complète à l'écran (elle reste dans Git et le README) | oui |

**Action proposée** : cacher aux enfants les deux modules CM2 (une ligne dans un fichier, réversible). À confirmer en comité (point 5).

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
| 6 oct. | Étape 12 allégée livrée : un nouveau module sort en brouillon, avec une question-réponse par compétence et par niveau à relire ; « valide » le rend visible aux enfants. Reste ta recette sur l'iPhone (12.7, 12.8) avec le module de ce week-end. |
| 6 oct. | `README.md` refondu en documentation de reprise : comment tout marche (app, modules, rôle du LLM, gouvernance), mode d'emploi, carte du dépôt et des docs. |
| 7 oct. | Besoin « listes de mots pour la dictée » (CE2/CM1) analysé à partir d'une ancienne conversation LLM : refaire toujours la même dictée fait apprendre le texte plutôt que les mots, et le LLM se trompait sur la couverture de la liste (5 mots jamais travaillés). Décision D8 : un module « dictée » fait par `/nouveau-module`. |
| 8 oct. | Module « Paddington 2 en VO » (anglais 6e) créé à la demande du sponsor, pour préparer le film vu en VO sous-titrée : mots du film, personnages, politesse, se présenter, décrire, l'histoire (sans la fin). Publié **en brouillon**, à relire puis valider. |
| 8 oct. | Module « Paddington 2 en VO » validé par le sponsor : visible dans la bibliothèque. Première utilisation réelle du brouillon et de la validation (recette 12.7, 12.8). |
| 11 oct. | Module « circuit électrique » corrigé à la demande du sponsor : nouvelle compétence **« Dessiner un schéma »**. L'élève pose fils et symboles sur une grille (choix du sponsor : grille plutôt que dessin libre, pour une correction automatique) ; toute disposition juste est acceptée, chaque erreur est expliquée (bout libre, court-circuit, série au lieu de dérivation…). Une question à dessiner dans chaque évaluation ; une fiche Apprendre en plus. Historique des enfants conservé (mêmes compétences, une ajoutée). |
| 11 oct. | Module circuit, « Dessiner un schéma » : le sponsor n'avait que des montages en série. Au niveau Échauffement, les 5 montages étaient tous en série. Corrigé : la dérivation arrive dès le niveau 1, et chaque question tire série ou dérivation à pile ou face (mesuré : environ 50/50). |
| 11 oct. | Module circuit : nouvelle compétence **« La diode électroluminescente (DEL) »**, à la demande du sponsor. Une fiche Apprendre (symbole, sens passant / bloquant, patte la plus longue au +), un montage « DEL et lampe » au labo (on retourne la DEL au doigt), des questions sur 2 niveaux (sens passant ou bloquant, pile retournée, DEL et lampe en série ou en dérivation) et au moins une question DEL par évaluation. Le symbole DEL entre aussi dans « Les symboles ». Pas remis en brouillon (module déjà utilisé) : questions à relire dans la conversation. Historique conservé. |
| 11 oct. | DEL du module circuit relue par le sponsor : les 3 points signalés et les questions-réponses par niveau sont justes. |
| 11 oct. | Premier module CM1 : « Les tables de 3, 6 et 9 » (table de 6 = double, table de 9 = triple de la table de 3, multiples), à la demande du sponsor, à partir du programme du cycle 3 (pas de photos ; le PDF du programme n'a pas pu être ouvert depuis la session). Publié **en brouillon**, à relire puis valider. |
| 11 oct. | Module « Les tables de 3, 6 et 9 » (CM1) validé par le sponsor : visible dans la bibliothèque. |
| 11 oct. | Module « Dictée 5 : Devinettes, avoir et être » (CM1, à partir de la photo de la liste de mots) : les 13 mots surlignés à écrire et à classer par nature, présent d'avoir et être. Publié **en brouillon**, à relire puis valider. Niveaux des enfants notés dans `CLAUDE.md` à la demande du sponsor. |
| 11 oct. | Module « Dictée 5 : Devinettes, avoir et être » (CM1) validé par le sponsor après retrait d'une faute proposée (« au-déssus ») : visible dans la bibliothèque. |

Modules en ligne : 6e : anglais Zootopia, Paddington 2, circuit électrique (HTML). CM1 : tables
de 3, 6 et 9, dictée 5 (HTML). CM2 : division euclidienne, grands nombres (JSON, aucun enfant à
ce niveau cette année).

---

## Regard du chef de projet

- **Priorité du moment** : la revue d'usage (A4, D9). Les modules sont là ; il faut maintenant
  savoir s'ils servent et où les enfants butent.
- **Le vrai risque reste la qualité du contenu** (une réponse fausse apprise par un enfant) :
  l'étape 12 y répond directement.
- **Recette de l'étape 12 faite en usage réel** : 3 modules sont passés par le brouillon puis ta
  validation (Paddington 2, tables, dictée 5).

---

## Backlog (idées notées, pas engagées)

| # | Idée | Origine | Priorité | Note |
|---|---|---|---|---|
| B1 | Pipeline sans Claude Code : robot de contrôle GitHub, puis POC de l'API Claude payée à l'usage | assessment du comité n° 1 (D7) | basse | l'assessment complet (options, SWOT, coûts) est dans l'historique de ce fichier, commit « Pilotage : retours du sponsor, assessment… » |
| B2 | Étape 12, unités 2 et 3 : fiche de contrôle dans l'app (modules JSON, puis HTML) | plan de l'étape 12 | basse | inutiles tant que la relecture dans la conversation suffit (D5) |
| B3 | Fusion des sauvegardes : restaurer un export **sans écraser** la progression déjà sur l'appareil (utile si un même enfant joue sur plusieurs appareils) | sponsor, 6 oct. | basse | à ressortir seulement si un enfant joue sur deux appareils. Synchronisation en ligne étudiée et écartée : iCloud (CloudKit JS : compte Apple Developer 99 $/an), Cloudflare Workers + D1 gratuit (le plus solide), Supabase (pause après une semaine), Firebase ; toutes lèvent « statique, aucun tiers, aucun compte » pour un besoin couvert par l'export envoyé par SMS. En attendant : ne restaurer l'export d'un enfant que sur un appareil vide ou le sien, car la restauration écrase tout. |
| B4 | Évolution « dictée » : rendre répétable le module de D8 (contrôle de couverture par un outil de `tools/`, skill adapté : une photo de liste suffit) | sponsor et Claude, 7 oct. | à décider au comité n° 2 | seulement si le module de D8 a servi ; la forme reste à concevoir à partir de son retour d'usage. Leçons de l'ancienne méthode : phrases nouvelles à chaque séance, courtes, au présent, sans les mots *** ; couverture vérifiée par programme, jamais par le LLM. |

---

## Actions

| # | Action | Porteur | Échéance | Statut |
|---|---|---|---|---|
| A2 | Au prochain `/nouveau-module` : vérifier que la réponse cite des exemples tirés à relire (recette G.5) | Sponsor | comité n° 2 | à confirmer (constaté sur Paddington 2) |
| A3 | Jouer le module circuit sur l'iPhone (recette 8.5 à 8.8), seulement s'il doit être envoyé à un enfant | Sponsor | si besoin | à faire |
| A9 | Relire le nouveau `README.md` (environ 10 minutes) : comprends-tu comment tout marche, et ce que tu dois faire ? | Sponsor | comité n° 2 | à faire |
| A10 | Chaque nouvelle liste de mots : photo + `/nouveau-module` « dictée » ; tu relis puis « valide » (première fois faite : dictée 5) | Sponsor, puis Claude | chaque semaine | en cours |
| A13 | Sur l'appareil du CM1 : créer un profil à son prénom ; ton profil reste pour tes essais | Sponsor | avant sa prochaine séance | à faire |
| A14 | Proposer à la 6e 10 questions « S'entraîner > Décrire », niveau Échauffement, dans Zootopia | Sponsor | cette semaine | à faire |

Actions closes : A1 (support lu), A5 (décisions du comité n° 1 appliquées), A6 (README refondu), A7 (étape 12 allégée livrée), A8 (premiers modules CM1 publiés en brouillon puis validés : tables, dictée 5), A4 et A12 (exports des deux appareils, 11 oct., analysés : revue d'usage n° 1), A11 (grille du dessin facile au doigt, sur l'iPhone).

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
| 6 oct. 2026 | (hors comité) | Pas de synchronisation en ligne de la progression : coût (serveur ou tiers, contraintes à lever, données des enfants hors de la maison) trop élevé pour le besoin ; l'export par SMS et l'accès physique aux appareils suffisent. Fusion des sauvegardes au backlog (B3), priorité basse. |
| 7 oct. 2026 | (hors comité) | D8 : listes de mots de la dictée (CE2/CM1) : option B, un module HTML « dictée » fait avec `/nouveau-module` (service courant). Le parent dicte depuis le téléphone, l'enfant écrit sur papier, le parent touche les mots ratés. Écartées pour l'instant : A (consigne à coller dans un LLM : couverture invérifiable) et C (évolution répétable, au backlog B4) : on la conçoit seulement après l'usage de B. |
