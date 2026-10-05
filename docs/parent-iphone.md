# Créer un module depuis l'iPhone

Des photos d'une leçon → une page de révision en ligne → l'URL envoyée à l'enfant par SMS.
Claude Code fait tout (page, contrôles, publication) avec le skill `/nouveau-module`
(`.claude/skills/nouveau-module/SKILL.md`). Comptez 5 à 10 minutes, relecture comprise.

## Une seule fois
1. Dans l'app Claude (iPhone), onglet **Code** (ou https://claude.ai/code dans Safari) :
   connecter GitHub et autoriser le dépôt `ghpz5649xx-blip/miniprof` (l'app GitHub de Claude
   doit pouvoir **pousser** sur le dépôt).
2. Installer l'app **GitHub** sur l'iPhone, connectée au même compte (pour fusionner une PR si la
   session pousse sur une branche, voir plus bas).

## À chaque leçon
1. Prendre les photos de la leçon et des exercices (cahier, manuel). Cadrer la page entière, sans
   prénom ni visage si possible : les photos restent dans la conversation, elles ne vont jamais
   dans le dépôt (il est public).
2. Ouvrir une **nouvelle session** Claude Code sur le dépôt `miniprof`.
3. Joindre les photos et écrire, par exemple :
   `/nouveau-module 6e, la leçon sur les fractions, surtout les exercices 3 et 4`
   (le niveau suffit ; Claude Code le devine sinon).
4. Attendre la réponse : l'URL `https://ghpz5649xx-blip.github.io/miniprof/modules/<id>.html`,
   les compétences, et **2 ou 3 points à relire**.
5. **Si la session a poussé sur une branche** (elle le dit, avec un lien de PR) : dans l'app
   GitHub, ouvrir la PR → « Merge pull request » → « Confirm ». Sinon, rien à faire.
6. Attendre environ **une minute** (publication GitHub Pages), ouvrir l'URL, relire les points
   signalés, faire 2 ou 3 questions par niveau. Une erreur ? La dire dans la même session
   (« la question sur … attend 3/4 au lieu de 2/3 ») : Claude Code corrige et republie, même
   adresse.
7. Envoyer l'URL par SMS. Sur le téléphone de l'enfant, la page demande de choisir son profil
   (une fois) ; ses réponses vont ensuite dans son bilan miniprof.

## Bon à savoir
- **Refaire un module** (photos plus nettes, autre approche) : `/nouveau-module` avec les photos,
  en précisant « refais le module <titre> ». Le même id est gardé, donc l'historique de l'enfant
  aussi.
- Le bilan de tous les modules est dans miniprof : https://ghpz5649xx-blip.github.io/miniprof/
  → profil → « Mon bilan ».
- Une page publiée est visible par toute personne qui a l'URL (comme tout le site).

## À vérifier lors du premier essai (recette 10.x de `docs/recette.md`)
- Les photos s'envoient bien dans Claude Code depuis l'iPhone.
- Le skill `/nouveau-module` est proposé dans une session web ou mobile.
- La session pousse sur `main` directement, ou sur une branche `claude/…` à fusionner. Noter
  ici ce qu'on a constaté : _à compléter_.
