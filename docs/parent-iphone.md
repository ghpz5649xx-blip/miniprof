# Créer un module depuis l'iPhone

Des photos d'une leçon → une page de révision en ligne → l'URL envoyée à l'enfant par SMS.
Claude Code fait tout (page, contrôles, publication) avec le skill `/nouveau-module`
(`.claude/skills/nouveau-module/SKILL.md`). Comptez 5 à 10 minutes, relecture comprise.

## Une seule fois
1. **Connecter GitHub** (plus simple dans Safari que dans l'app) : ouvrir https://claude.ai/code,
   se connecter avec le compte Claude, suivre « Connect GitHub » → page GitHub « Authorize » →
   retour sur claude.ai/code. Un environnement « Default » est créé tout seul (accès réseau
   « Trusted » : suffisant, il laisse installer `jsonschema`).
2. **Installer l'app GitHub de Claude sur le dépôt** : https://github.com/apps/claude/installations/new
   → compte `ghpz5649xx-blip` → « Only select repositories » → `miniprof` → « Install ». Sans
   elle, une session peut lire le dépôt (il est public) mais risque de ne pas pouvoir pousser.
3. Dans l'app Claude (iPhone), onglet **Code** : le dépôt `ghpz5649xx-blip/miniprof` apparaît
   dans le choix du dépôt. Pas d'onglet Code : vérifier que l'app est à jour et le compte (offre
   Pro ou Max).
4. Facultatif : l'app **GitHub** sur l'iPhone, pour fusionner une PR si une session pousse un
   jour sur une branche.

Variante depuis le Mac, si `gh` y est connecté : lancer `claude`, puis `/web-setup`.

## À chaque leçon
1. Prendre les photos de la leçon et des exercices (cahier, manuel). Cadrer la page entière, sans
   prénom ni visage si possible : les photos restent dans la conversation, elles ne vont jamais
   dans le dépôt (il est public).
2. Ouvrir une **nouvelle session** Claude Code (onglet Code), dépôt `miniprof`, branche `main`
   (branche de départ : la session crée la sienne). Si l'app demande un environnement :
   « Default ».
3. Joindre les photos et écrire, par exemple :
   `/nouveau-module 6e, la leçon sur les fractions, surtout les exercices 3 et 4`
   (le niveau suffit ; Claude Code le devine sinon). **Taper la commande en entier** : l'app ne
   la propose pas au premier message (le dépôt n'est pas encore copié dans la session), mais
   elle marche une fois envoyée.
4. Attendre la réponse : l'URL `https://ghpz5649xx-blip.github.io/miniprof/modules/<id>.html`,
   les compétences, **2 ou 3 points à relire**, et une question par compétence et par niveau
   avec sa bonne réponse. Le module est publié **en brouillon** : il n'apparaît pas encore dans
   la bibliothèque des enfants.
5. Rien à fusionner en temps normal : partie de `main`, la session y pousse directement
   (constaté le 2026-10-06). **Seulement si** elle annonce une branche `claude/…` et un lien de
   PR : dans l'app GitHub, ouvrir la PR → « Merge pull request » → « Confirm ».
6. Attendre environ **une minute** (publication GitHub Pages), ouvrir l'URL, relire les points
   signalés et les questions-réponses, faire 2 ou 3 questions par niveau. Une erreur ? La dire
   dans la même session (« la question sur … attend 3/4 au lieu de 2/3 ») : Claude Code corrige
   et republie, même adresse.
7. Tout est juste : répondre **valide** dans la même session (ou, plus tard, dans une nouvelle
   session : `/nouveau-module valide <id>`). Le module apparaît alors dans la bibliothèque des
   enfants.
8. Envoyer l'URL par SMS. Sur le téléphone de l'enfant, la page demande de choisir son profil
   (une fois) ; ses réponses vont ensuite dans son bilan miniprof.

## Bon à savoir
- **Corriger un module plus tard** (la session est fermée) : nouvelle session, sans photo,
  `/nouveau-module corrige le module <id> : <ce qui ne va pas>`. Même adresse, même historique
  (constaté le 2026-10-06).
- **Refaire un module** (photos plus nettes, autre approche) : `/nouveau-module` avec les photos,
  en précisant « refais le module <titre> ». Le même id est gardé, donc l'historique de l'enfant
  aussi.
- Le bilan de tous les modules est dans miniprof : https://ghpz5649xx-blip.github.io/miniprof/
  → profil → « Mon bilan ».
- Une page publiée est visible par toute personne qui a l'URL (comme tout le site).

## À vérifier lors du premier essai (recette 10.x de `docs/recette.md`)
- Les photos s'envoient bien dans Claude Code depuis l'iPhone.
- Le skill `/nouveau-module` : ✔ (2026-10-06, iPhone) pas d'autocomplétion au premier message,
  mais la commande tapée en entier marche.
- Où arrive le push : ✔ (2026-10-06) directement sur `main` (module `anglais-6e-zootopia-animaux`),
  alors que la documentation de Claude Code parle d'une branche par session. Le skill gère les
  deux cas.
