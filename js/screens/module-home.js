// Accueil d'un module : titre, description, et les 4 activités.
// À l'étape 2, les activités sont visibles mais pas encore actives.

import { el, clear, topBar, message, richText } from "../ui.js";
import { readJson } from "../loader.js";
import { checkModule } from "../check-module.js";

// Même règle que les id de module dans le schéma. On la vérifie car l'id vient
// de l'adresse de la page, que n'importe qui peut modifier.
const ID_VALIDE = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const ACTIVITES = [
  { titre: "Apprendre", texte: "La leçon, pas à pas", etape: 3 },
  { titre: "S'entraîner", texte: "Des questions à volonté, avec indices et corrections", etape: 4 },
  { titre: "Évaluation", texte: "10 questions, sans aide, avec une note à la fin", etape: 5 },
  { titre: "Bilan", texte: "Ce qui est réussi, ce qu'il reste à travailler", etape: 6 },
];

export function showModuleHome(id) {
  const app = clear();
  const monAdresse = location.hash;
  app.append(topBar("Module", "#/biblio"));
  const zone = el("div", {}, el("p", { class: "muted" }, "Chargement du module…"));
  app.append(zone);

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
      zone.replaceChildren(contenuModule(resultat.module, resultat.warnings));
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

function contenuModule(module, warnings) {
  const contenu = el("div", {},
    el("header", { class: "hero" },
      el("h2", {}, richText(module.title)),
      el("p", {}, richText(module.description)),
      el("p", { class: "muted" }, String(module.level) + " · " + module.questions.length + " questions"),
    ),
  );
  for (const w of warnings) contenu.append(message("hint", w));

  const grille = el("div", { class: "stack" });
  for (const a of ACTIVITES) {
    // Bouton désactivé tant que l'activité n'est pas construite.
    grille.append(
      el("button", { class: "card card-activity", disabled: true },
        el("span", { class: "card-title" }, a.titre),
        el("span", { class: "card-text" }, a.texte),
        el("span", { class: "badge" }, "Bientôt (étape " + a.etape + ")"),
      ),
    );
  }
  contenu.append(grille);
  return contenu;
}
