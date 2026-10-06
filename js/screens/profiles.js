// Écran d'accueil : un gros bouton par enfant, ajout et suppression de profil.

import { el, clear, message } from "../ui.js";
import { listProfiles, createProfile, deleteProfile, setCurrent, MAX_NAME } from "../profiles.js";
import { MESSAGE_ECHEC_SAUVEGARDE } from "../storage.js";

// État de l'écran, gardé entre deux affichages :
// - modeGestion : vrai quand on affiche les boutons « Supprimer » ;
// - aConfirmer  : id du profil dont la suppression attend le 2e clic.
let modeGestion = false;
let aConfirmer = null;

// erreur : message à afficher ; saisie : prénom à remettre dans le champ
// (pour corriger sans tout retaper).
export function showProfiles(erreur, saisie) {
  const app = clear();
  const profils = listProfiles();

  app.append(
    el("header", { class: "hero" },
      el("h1", {}, "miniprof"),
      el("p", {}, profils.length > 0 ? "Qui es-tu ?" : "Bienvenue ! Crée ton profil pour commencer."),
    ),
  );
  if (erreur) app.append(message("error", erreur));

  const liste = el("div", { class: "stack" });
  for (const p of profils) {
    if (modeGestion) {
      liste.append(ligneGestion(p));
    } else {
      liste.append(el("button", { class: "btn btn-big", onclick: () => choisir(p.id) }, p.name));
    }
  }
  app.append(liste);

  if (!modeGestion) {
    const champ = formulaireAjout(app);
    if (saisie) champ.value = saisie;
    // Premier profil ou erreur à corriger : curseur directement dans le champ.
    if (profils.length === 0 || erreur) champ.focus();
  }

  if (profils.length > 0) {
    app.append(el("button", {
      class: "btn btn-link",
      onclick: () => { modeGestion = !modeGestion; aConfirmer = null; showProfiles(); },
    }, modeGestion ? "Terminé" : "Gérer les profils"));
  }
  // Toujours visible, même sans profil : c'est ici qu'on restaure ses
  // données sur un nouvel appareil.
  app.append(el("a", { class: "btn btn-link", href: "#/sauvegarde" }, "Sauvegarder ou restaurer les données"));
}

function choisir(id) {
  modeGestion = false;
  if (!setCurrent(id)) {
    showProfiles(MESSAGE_ECHEC_SAUVEGARDE);
    return;
  }
  location.hash = "#/biblio";
}

// Ajoute le formulaire « Ajouter un profil » à l'écran et renvoie son champ.
// Un <form> pour que la touche Entrée valide.
function formulaireAjout(app) {
  const champ = el("input", {
    type: "text", id: "nouveau-prenom", maxlength: String(MAX_NAME),
    autocomplete: "off", placeholder: "Prénom",
  });
  const form = el("form", { class: "card add-profile" },
    el("label", { for: "nouveau-prenom" }, "Ajouter un profil"),
    el("div", { class: "row" }, champ, el("button", { class: "btn btn-primary", type: "submit" }, "OK")),
  );
  form.addEventListener("submit", (event) => {
    event.preventDefault(); // pas de rechargement de page
    const resultat = createProfile(champ.value);
    if (!resultat.ok) {
      showProfiles(resultat.error, champ.value);
      return;
    }
    // On entre directement dans le profil créé : sinon l'enfant ne comprend pas
    // qu'il faut encore toucher son prénom (retour de la 1re utilisation, iPhone).
    choisir(resultat.profile.id);
  });
  app.append(form);
  return champ;
}

// Ligne du mode gestion : prénom + bouton Supprimer.
// Confirmation en deux clics : le 1er clic change le libellé, le 2e supprime.
function ligneGestion(p) {
  const enAttente = aConfirmer === p.id;
  return el("div", { class: "card row manage-row" },
    el("span", { class: "grow" }, p.name),
    el("button", {
      class: "btn " + (enAttente ? "btn-danger" : "btn-secondary"),
      onclick: () => {
        if (!enAttente) {
          aConfirmer = p.id;
          showProfiles();
          return;
        }
        aConfirmer = null;
        const ok = deleteProfile(p.id);
        if (listProfiles().length === 0) modeGestion = false;
        showProfiles(ok ? null : MESSAGE_ECHEC_SAUVEGARDE);
      },
    }, enAttente ? "Confirmer : supprimer " + p.name : "Supprimer"),
  );
}
