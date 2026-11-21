# P014 — Écran d'admin du projet (Mac)

- **Statut** : exécuté le 21 nov. 2026 (feed-back possible jusqu'au 5 déc.).
- **Origine** : sponsor, 21 nov. 2026. Il crée les modules depuis l'iPhone et fait évoluer la
  plateforme depuis le Mac, avec un agent ; il veut piloter le projet dans un écran simple,
  accessible sur le Mac seulement, que l'agent relit. Lancé directement à sa demande, alors que
  P012 reste en cours.

## Besoin
Gérer ses tâches, les idées et leurs priorités, des consignes à l'agent et voir les plans, sans
éditer de Markdown, et que l'agent en tienne compte, y compris dans une session cloud.

## Décisions (sponsor, 21 nov. 2026)
- Pas une page de l'app : le site est public et un `localStorage` est illisible pour l'agent.
  Un **serveur local** Python (`tools/admin.py`, bibliothèque standard), qui n'écoute que sur
  `127.0.0.1` : l'iPhone ne peut pas le joindre.
- Données dans les **fichiers Markdown actuels**, toujours éditables à la main :
  `pilotage.md` (« Tâches du sponsor », nouvelle section « Consignes pour Claude ») et
  `plans/index.md` (« Idées (sans fiche) », avec une priorité et un ordre). Un élément par ligne.
- Données **sur GitHub** (dépôt public : jamais de prénom ni de donnée des enfants).
- **L'écran committe et pousse** à chaque enregistrement : `git commit -- pilotage.md
  plans/index.md` (rien d'autre), `pull --rebase --autostash`, `push` ; en cas d'échec, le
  commit reste local et l'écran le dit, sans rien forcer.

## Livré
- `tools/admin.py` : lecture/écriture des sections (refus d'écrire si une ligne écrite à la main
  est illisible, pour ne pas l'effacer), synchro Git, serveur (`Host` vérifié, POST en JSON
  seulement, contre un site qui voudrait écrire dans le dépôt).
- `tools/admin/page.html` : tâches (échues en tête, fait, abandonner, reporter, ajouter),
  consignes, idées (priorité, ordre, ajout, suppression), plans (fiche en lecture, feed-back qui
  devient une consigne). Publiée sur Pages avec le dépôt, elle y affiche seulement « ne marche
  que sur le Mac ».
- 21 nov. 2026, sur demande du sponsor : la fiche d'un plan s'affiche mise en forme (titres,
  gras, italique, listes, tableaux, citations, code, liens, images du dépôt) par
  `tools/admin/markdown.js`, un petit lecteur sans bibliothèque qui construit chaque élément
  nœud par nœud ; le serveur sert les seules images du dépôt (`/fichier/…`).
- `CLAUDE.md` : lecture des consignes en début de session, prochain sujet = haut des idées.

## Vérifié
- `tools/tests/test_admin.py` (17 tests) : les vrais fichiers relus et réécrits à l'identique,
  ajout/retrait/report, ordre et priorité des idées, échéance échue, ligne illisible qui bloque,
  synchro sur un dépôt temporaire (seuls les fichiers du pilotage committés, branche autre que
  main, origin injoignable), hôte étranger et POST non JSON refusés.
- Usage réel le 21 nov. : 12 enregistrements du sponsor poussés, dont certains après les commits
  d'une session module iPhone (rebase sans conflit).
- Rendu Markdown vu dans Chromium sur une fiche d'essai (toutes les formes) et sur P012.
- Captures de l'écran dans Chromium (lecture seule) ; page hors serveur : message attendu.

## À vérifier à la main (tâche du sponsor)
- Sur le Mac : `python3 tools/admin.py`, ajouter puis retirer une consigne, vérifier le commit
  « Pilotage : … » sur GitHub.
- Sur l'iPhone : https://ghpz5649xx-blip.github.io/miniprof/tools/admin/page.html n'affiche que
  le message « ne marche que sur le Mac », sans débordement.

## Feed-back
- **21 nov. 2026 (sponsor, écran d'admin)** : « afficher le feed-back en temps réel dans
  l'interface, avec sa date ». Fait : sous la fiche ouverte, les feed-backs envoyés et pas encore
  traités, avec leur date, dès l'envoi ; une fois traité, Claude l'écrit ici, dans la fiche.
- **21 nov. 2026 (sponsor, écran d'admin)** : « masquer les plans exécutés depuis au moins
  2 semaines dans un onglet Plans archivés ». Fait : onglets « Actifs » et « Archivés » ; un plan
  clos, abandonné, archivé, intégré, ou exécuté dont le délai de feed-back est passé, est archivé
  (calculé par `est_archive()` à chaque affichage).
