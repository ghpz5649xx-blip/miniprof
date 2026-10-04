// Accueil d'un module : titre, description, et les 4 activités.
// Les activités pas encore construites sont visibles mais désactivées.

import { el, clear, topBar, message, richText } from "../ui.js";
import { openModule } from "../open-module.js";

// `page` : sous-adresse de l'activité (#/module/<id>/<page>), ou null tant
// que l'activité n'est pas construite.
const ACTIVITES = [
  { titre: "Apprendre", texte: "La leçon, pas à pas", page: "apprendre" },
  { titre: "S'entraîner", texte: "Des questions à volonté, avec indices et corrections", page: "entrainement" },
  { titre: "Évaluation", texte: "10 questions, sans aide, avec une note à la fin", page: "evaluation" },
  { titre: "Bilan", texte: "Ce qui est réussi, ce qu'il reste à travailler", page: null, etape: 6 },
];

export function showModuleHome(id) {
  const app = clear();
  app.append(topBar("Module", "#/biblio"));
  const zone = el("div", {});
  app.append(zone);
  openModule(id, zone, (module, warnings) => {
    zone.replaceChildren(contenuModule(id, module, warnings));
  });
}

// `id` : celui de l'adresse, déjà vérifié par openModule (plus sûr que
// module.id, écrit dans le fichier).
function contenuModule(id, module, warnings) {
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
    if (a.page) {
      grille.append(
        el("a", { class: "card card-link card-activity", href: "#/module/" + id + "/" + a.page },
          el("span", { class: "card-title" }, a.titre),
          el("span", { class: "card-text" }, a.texte),
        ),
      );
    } else {
      // Bouton désactivé tant que l'activité n'est pas construite.
      grille.append(
        el("button", { class: "card card-activity", disabled: true },
          el("span", { class: "card-title" }, a.titre),
          el("span", { class: "card-text" }, a.texte),
          el("span", { class: "badge" }, "Bientôt (étape " + a.etape + ")"),
        ),
      );
    }
  }
  contenu.append(grille);
  return contenu;
}
