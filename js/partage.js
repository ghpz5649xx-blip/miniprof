// Partage de la sauvegarde par la feuille de partage du système (Messages, AirDrop,
// Mail, Fichiers…), au lieu d'un simple téléchargement.
//
// Pourquoi : sur iPhone, le téléchargement range le fichier dans Fichiers, et le parent doit
// ensuite le retrouver pour l'envoyer. Ici, « Exporter » ouvre directement la feuille de partage.
//
// Seule exception à « asynchrone limité à la lecture de fichiers » (décidée par le sponsor,
// plan P003) : navigator.share() renvoie une promesse. Elle est confinée à ce fichier ; le
// reste de l'app ne voit qu'un rappel (`auResultat`). La date du dernier export n'est notée
// que si le partage a abouti (sinon l'enfant qui annule croirait avoir sauvegardé).
//
// Sans partage de fichiers (ordinateur, vieux navigateur), peutPartager() est faux et l'écran
// garde le téléchargement.

import { preparerSauvegarde, noterExport } from "./backup.js";

function fichierVide() {
  return new File(["{}"], "miniprof.export.json", { type: "application/json" });
}

// Vrai si le navigateur sait partager un fichier JSON.
export function peutPartager() {
  return typeof navigator !== "undefined" && typeof navigator.canShare === "function"
    && typeof navigator.share === "function" && navigator.canShare({ files: [fichierVide()] });
}

// À appeler directement dans le clic (le système exige un geste de l'utilisateur).
// auResultat("ok" | "annule" | "erreur", enregistre) : `enregistre` dit si la date du dernier
// export a pu être notée (seulement pour "ok").
export function partagerSauvegarde(auResultat) {
  const sauvegarde = preparerSauvegarde();
  const fichier = new File([sauvegarde.texte], sauvegarde.nom, { type: "application/json" });
  navigator.share({ files: [fichier], title: "Sauvegarde miniprof" }).then(
    () => auResultat("ok", noterExport(sauvegarde.date)),
    (erreur) => auResultat(erreur && erreur.name === "AbortError" ? "annule" : "erreur", false),
  );
}
