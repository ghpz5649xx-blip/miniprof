// Écran « Sauvegarde » (#/sauvegarde) : exporter toutes les données de
// l'appareil dans un fichier, ou les remplacer par une sauvegarde.
//
// Accessible sans profil (voir app.js) : sur un nouvel appareil, on restaure
// avant d'avoir créé qui que ce soit. La logique est dans js/backup.js.

import { el, clear, topBar, message } from "../ui.js";
import { currentProfile } from "../profiles.js";
import { readJsonFile } from "../loader.js";
import { MESSAGE_ECHEC_SAUVEGARDE } from "../storage.js";
import { downloadBackup, lastExport, storageRatio, checkBackup, restoreBackup } from "../backup.js";

// Sauvegarde lue et contrôlée, en attente de confirmation (ou null).
let aRestaurer = null;

// retour : { type: "ok" | "error" | "info", texte } affiché en haut, ou rien.
export function showBackup(retour) {
  const app = clear();
  app.append(topBar("Sauvegarde", currentProfile() ? "#/biblio" : "#/"));
  if (retour) app.append(message(retour.type, retour.texte));

  app.append(blocExport());
  app.append(blocRestauration());
  app.append(el("p", { class: "muted" },
    "Le fichier reste sur ton appareil : rien n'est envoyé sur Internet."));
}

function blocExport() {
  const derniere = lastExport();
  const pourcent = Math.round(storageRatio() * 100);
  return el("section", { class: "card" },
    el("h2", { class: "card-title" }, "Exporter"),
    el("p", {}, "Toutes les données de cet appareil (profils, résultats, questions signalées) dans un fichier."),
    el("p", { class: "muted" },
      "Dernier export : " + (derniere ? new Date(derniere * 1000).toLocaleDateString("fr-FR") : "jamais")
      + " · stockage utilisé : " + pourcent + " %"),
    el("button", {
      class: "btn btn-primary",
      onclick: () => {
        aRestaurer = null;
        const ok = downloadBackup();
        showBackup(ok
          ? { type: "ok", texte: "Fichier téléchargé. Range-le en lieu sûr (ordinateur, clé USB, cloud)." }
          : { type: "error", texte: MESSAGE_ECHEC_SAUVEGARDE });
      },
    }, "Exporter mes données"),
  );
}

function blocRestauration() {
  const bloc = el("section", { class: "card" },
    el("h2", { class: "card-title" }, "Restaurer une sauvegarde"),
  );

  // 2e temps : la sauvegarde est lue, on demande confirmation dans la page.
  if (aRestaurer) {
    bloc.append(
      message("info", aRestaurer.resume),
      message("hint", "Les données actuelles de cet appareil seront **remplacées**."),
      el("div", { class: "actions" },
        el("button", {
          class: "btn btn-danger",
          onclick: () => {
            const ok = restoreBackup(aRestaurer.data);
            aRestaurer = null;
            showBackup(ok
              ? { type: "ok", texte: "Sauvegarde restaurée." }
              : { type: "error", texte: MESSAGE_ECHEC_SAUVEGARDE });
          },
        }, "Confirmer : remplacer les données"),
        el("button", {
          class: "btn btn-secondary",
          onclick: () => { aRestaurer = null; showBackup(); },
        }, "Annuler"),
      ),
    );
    return bloc;
  }

  // 1er temps : choisir le fichier.
  const champ = el("input", { type: "file", id: "fichier-sauvegarde", accept: ".json,application/json" });
  champ.addEventListener("change", () => {
    const fichier = champ.files[0];
    if (!fichier) return;
    const monAdresse = location.hash;
    readJsonFile(fichier)
      .then((data) => {
        if (location.hash !== monAdresse) return; // parti entre-temps
        const resultat = checkBackup(data);
        if (!resultat.ok) {
          showBackup({ type: "error", texte: resultat.errors.join("\n") });
          return;
        }
        aRestaurer = { data: data, resume: resultat.resume };
        showBackup();
      })
      .catch((erreur) => {
        if (location.hash !== monAdresse) return;
        showBackup({ type: "error", texte: erreur.message });
      });
  });
  bloc.append(
    el("label", { for: "fichier-sauvegarde" }, "Choisis un fichier « miniprof-….export.json » :"),
    champ,
  );
  return bloc;
}
