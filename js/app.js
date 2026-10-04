// Point d'entrée de l'app : choisit l'écran à afficher selon l'adresse.
//
// Navigation par « hash » (la partie après # dans l'adresse) :
//   #/                 choix du profil
//   #/biblio           bibliothèque des modules
//   #/module/<id>      accueil d'un module
//   #/module/<id>/apprendre[/<compétence>]   leçon (voir screens/lesson.js)
// Pourquoi : changer d'écran = changer d'adresse. Le bouton « retour » du
// navigateur ou du téléphone marche tout seul, et recharger la page garde
// l'écran courant. Aucun serveur n'est nécessaire (GitHub Pages ignore le #).

import { currentProfile } from "./profiles.js";
import { showProfiles } from "./screens/profiles.js";
import { showLibrary } from "./screens/library.js";
import { showModuleHome } from "./screens/module-home.js";
import { showLesson } from "./screens/lesson.js";

function route() {
  const hash = location.hash;

  // Première ouverture (aucun #) : si un profil a déjà été choisi sur cet
  // appareil, on va directement à sa bibliothèque.
  if (hash === "" || hash === "#") {
    location.replace(currentProfile() ? "#/biblio" : "#/");
    return; // replace() redéclenche route() via l'événement hashchange
  }

  // Les écrans suivants ont besoin d'un profil : sinon, retour au choix.
  if (hash !== "#/" && !currentProfile()) {
    location.replace("#/");
    return;
  }

  const parties = hash.slice(2).split("/"); // "#/module/abc" -> ["module", "abc"]
  if (hash === "#/") {
    showProfiles();
  } else if (parties[0] === "biblio") {
    showLibrary();
  } else if (parties[0] === "module" && parties[1] && parties[2] === "apprendre") {
    showLesson(decodeURIComponent(parties[1]), parties[3] ? decodeURIComponent(parties[3]) : null);
  } else if (parties[0] === "module" && parties[1] && parties[2]) {
    // Activité pas encore construite (ex. « entrainement ») : accueil du module.
    location.replace("#/module/" + parties[1]);
  } else if (parties[0] === "module" && parties[1]) {
    showModuleHome(decodeURIComponent(parties[1]));
  } else {
    // Adresse inconnue (lien abîmé) : bibliothèque.
    location.replace("#/biblio");
  }
}

window.addEventListener("hashchange", route);
route();
