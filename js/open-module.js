// Ouverture d'un module par les écrans qui en ont besoin (accueil du module,
// leçon, et plus tard entraînement et évaluation).
//
// Pourquoi un fichier à part : chaque écran doit faire les mêmes contrôles
// (id valide, fichier lisible, module utilisable) et afficher les mêmes
// messages d'erreur. On l'écrit une seule fois ici.

import { el, message } from "./ui.js";
import { readJson } from "./loader.js";
import { checkModule } from "./check-module.js";

// Même règle que les id de module dans le schéma. On la vérifie car l'id vient
// de l'adresse de la page, que n'importe qui peut modifier.
const ID_VALIDE = /^[a-z0-9]+(-[a-z0-9]+)*$/;

// Charge le module `id`, puis appelle afficher(module, warnings).
// - `zone` : élément de la page qui affiche « Chargement… » puis, en cas de
//   problème, le message d'erreur ;
// - afficher() n'est appelée que si le module est utilisable et si l'enfant
//   est toujours sur le même écran.
export function openModule(id, zone, afficher) {
  const monAdresse = location.hash;
  zone.replaceChildren(el("p", { class: "muted" }, "Chargement du module…"));

  if (!ID_VALIDE.test(id)) {
    zone.replaceChildren(message("error", "Adresse de module invalide."));
    return;
  }

  // Le fichier s'appelle toujours <id>.json (vérifié par build_index.py).
  readJson("modules/" + id + ".json")
    .then((data) => {
      if (location.hash !== monAdresse) return; // l'enfant est parti entre-temps
      const resultat = checkModule(data);
      if (!resultat.ok) {
        zone.replaceChildren(erreurModule(resultat.errors.join("\n")));
        return;
      }
      afficher(resultat.module, resultat.warnings);
    })
    .catch((erreur) => {
      if (location.hash !== monAdresse) return;
      zone.replaceChildren(erreurModule(erreur.message));
    });
}

// Message d'erreur + retour : les autres modules restent accessibles.
function erreurModule(texte) {
  return el("div", {},
    message("error", "Ce module ne peut pas s'ouvrir.\n" + texte),
    el("a", { class: "btn btn-primary", href: "#/biblio" }, "Retour à la bibliothèque"),
  );
}
