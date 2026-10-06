// Bibliothèque : les modules listés dans modules/index.json, groupés par matière.
//
// L'index ne contient que des métadonnées légères (titre, niveau…), produites
// par tools/build_index.py : on n'ouvre le fichier complet d'un module qu'au clic.
//
// En haut : le rappel de sauvegarde s'il y a lieu (js/backup.js).
// En bas : l'aperçu d'un module local, pour le parent (js/open-module.js).

import { el, clear, topBar, message, richText } from "../ui.js";
import { currentProfile } from "../profiles.js";
import { readJson, readJsonFile } from "../loader.js";
import { backupReminder } from "../backup.js";
import { APERCU, setPreview } from "../open-module.js";

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
  const rappel = backupReminder();
  if (rappel) {
    app.append(el("div", { class: "msg msg-hint", role: "status" },
      rappel + " ", el("a", { href: "#/sauvegarde" }, "Sauvegarder")));
  }
  const zone = el("div", {}, el("p", { class: "muted" }, "Chargement des modules…"));
  app.append(zone);
  app.append(blocApercu());

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
  const tous = index && Array.isArray(index.modules) ? index.modules : [];
  // Un brouillon (modules/brouillons.json, tools/build_index.py) n'est pas encore
  // relu par le parent : les enfants ne le voient pas. Il reste dans l'index pour
  // le bilan et l'écran « Pour les parents ».
  const modules = tous.filter((m) => !m.brouillon);
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
      el("a", { class: "card card-link", href: adresseModule(m) },
        el("span", { class: "card-title" }, richText(m.title)),
        el("span", { class: "badge" }, String(m.level)),
        el("span", { class: "card-text" }, richText(m.description || "")),
      ),
    );
  }
  return contenu;
}

// Un module HTML (build_index.py, "kind": "html") est une page autonome : on
// l'ouvre directement. Un module JSON s'ouvre dans les écrans de l'app.
export function adresseModule(m) {
  if (m.kind === "html") return "modules/" + encodeURIComponent(m.file);
  return "#/module/" + encodeURIComponent(m.id);
}

// « Pour les parents » : ouvrir un module JSON de l'appareil sans le publier,
// pour le tester avant de le committer. Rien n'est enregistré pendant l'aperçu.
function blocApercu() {
  const erreur = el("div", {});
  const champ = el("input", { type: "file", id: "fichier-apercu", accept: ".json,application/json" });
  champ.addEventListener("change", () => {
    const fichier = champ.files[0];
    if (!fichier) return;
    readJsonFile(fichier)
      .then((data) => {
        if (location.hash !== "#/biblio") return; // parti entre-temps
        setPreview(data);
        location.hash = "#/module/" + APERCU;
      })
      .catch((e) => {
        if (location.hash !== "#/biblio") return;
        erreur.replaceChildren(message("error", e.message));
      });
  });
  return el("details", { class: "card correction parent-zone" },
    el("summary", {}, "Pour les parents : aperçu d'un module"),
    el("p", { class: "muted" },
      "Ouvre un fichier de module de cet appareil pour le tester avant de le publier. "
      + "Rien n'est enregistré, et l'aperçu disparaît si la page est rechargée."),
    el("label", { for: "fichier-apercu" }, "Fichier du module (.json) :"),
    champ,
    erreur,
  );
}
