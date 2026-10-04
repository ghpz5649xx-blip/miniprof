// Bibliothèque : les modules listés dans modules/index.json, groupés par matière.
//
// L'index ne contient que des métadonnées légères (titre, niveau…), produites
// par tools/build_index.py : on n'ouvre le fichier complet d'un module qu'au clic.

import { el, clear, topBar, message, richText } from "../ui.js";
import { currentProfile } from "../profiles.js";
import { readJson } from "../loader.js";

// Libellés affichés pour les valeurs de "subject" du schéma.
const MATIERES = {
  "maths": "Mathématiques",
  "francais": "Français",
  "histoire-geo": "Histoire-géographie",
  "sciences": "Sciences",
  "anglais": "Anglais",
  "emc": "Enseignement moral et civique",
  "autre": "Autre",
};

export function showLibrary() {
  const app = clear();
  const profil = currentProfile();
  app.append(
    topBar("Bonjour " + profil.name + " !", null,
      el("a", { class: "btn btn-secondary btn-small", href: "#/" }, "Changer de profil")),
  );
  const zone = el("div", {}, el("p", { class: "muted" }, "Chargement des modules…"));
  app.append(zone);

  // readJson est asynchrone : la liste s'affiche quand le fichier est arrivé.
  readJson("modules/index.json")
    .then((index) => {
      // Si l'enfant a changé d'écran pendant le chargement, on n'affiche rien.
      if (location.hash !== "#/biblio") return;
      zone.replaceChildren(listeModules(index));
    })
    .catch((erreur) => {
      if (location.hash !== "#/biblio") return;
      zone.replaceChildren(message("error", "La liste des modules est illisible. " + erreur.message));
    });
}

function listeModules(index) {
  const modules = index && Array.isArray(index.modules) ? index.modules : [];
  if (modules.length === 0) {
    return message("info", "Aucun module pour l'instant.");
  }
  // Le bilan, en tête : l'enfant voit d'abord ce qu'il a à travailler.
  const contenu = el("div", {},
    el("a", { class: "card card-link", href: "#/bilan" },
      el("span", { class: "card-title" }, "Mon bilan"),
      el("span", { class: "card-text" }, "Ce qui est réussi, ce qu'il reste à travailler"),
    ),
  );
  // L'index est déjà trié par matière puis niveau : on crée un titre à chaque
  // changement de matière.
  let matiereCourante = null;
  for (const m of modules) {
    if (m.subject !== matiereCourante) {
      matiereCourante = m.subject;
      contenu.append(el("h2", { class: "section-title" }, MATIERES[m.subject] || String(m.subject)));
    }
    contenu.append(
      el("a", { class: "card card-link", href: "#/module/" + encodeURIComponent(m.id) },
        el("span", { class: "card-title" }, richText(m.title)),
        el("span", { class: "badge" }, String(m.level)),
        el("span", { class: "card-text" }, richText(m.description || "")),
      ),
    );
  }
  return contenu;
}
