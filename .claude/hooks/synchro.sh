#!/bin/sh
# Lancé par Claude Code au démarrage (ou à la reprise) de chaque session : voir .claude/settings.json.
# Pourquoi : le parent travaille depuis l'iPhone (sessions dans le cloud) et depuis le Mac, dont
# le dossier local peut avoir des jours de retard sur origin/main.
# --ff-only : ne fusionne jamais et ne touche à rien en cas de commits locaux ou de divergence ;
# dans ce cas, on prévient au lieu de forcer. Ce que le script affiche est lu par Claude.
# Sort toujours en succès : un échec réseau ne doit pas empêcher d'ouvrir la session.

cd "$CLAUDE_PROJECT_DIR" || exit 0

branche=$(git branch --show-current)
if [ "$branche" != "main" ]; then
  echo "Synchro : branche $branche, pas de mise à jour automatique."
  exit 0
fi

if git pull --ff-only -q origin main 2>/dev/null; then
  echo "Synchro : à jour avec origin/main ($(git log -1 --format=%h))."
else
  echo "Synchro : ÉCHEC de git pull --ff-only (réseau, modifications locales ou divergence)."
  echo "Prévenir le parent avant de travailler."
fi
exit 0
