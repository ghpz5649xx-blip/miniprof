// Écran de réglage de « S'entraîner » : choix du niveau et de la compétence.
//
// Adresse : #/module/<id>/entrainement
// « Commencer » mène à #/module/<id>/entrainement/<niveau>[/<compétence>]
// (voir screens/practice.js). Sans compétence dans l'adresse : tout mélangé.

import { el, clear, topBar, message, richText, chip } from "../ui.js";
import { openModule } from "../open-module.js";
import { withoutFlagged } from "../flags.js";

// Les 4 niveaux = la "difficulty" des questions du module.
const NIVEAUX = [
  { n: 1, texte: "Pour démarrer" },
  { n: 2, texte: "Un peu plus dur" },
  { n: 3, texte: "Difficile" },
  { n: 4, texte: "Pour les champions" },
];

// Dernier réglage utilisé, pour le retrouver en revenant sur cet écran
// (bouton « ← Retour » pendant l'entraînement). Gardé en mémoire seulement :
// recharger la page revient au niveau 1, tout mélangé.
let dernier = { id: null, niveau: 1, skill: null };

// Appelée par l'écran d'entraînement, y compris après « Niveau suivant ».
export function retenirReglage(id, niveau, skill) {
  dernier = { id: id, niveau: niveau, skill: skill };
}

// Questions de la banque pour un niveau et une compétence (null = toutes),
// sans les questions signalées (js/flags.js). `id` : celui de l'adresse.
export function questionsDuNiveau(id, module, niveau, skill) {
  return withoutFlagged(id, module.questions).filter((q) => q.difficulty === niveau && (!skill || q.skill === skill));
}

export function showPracticeSetup(id) {
  const app = clear();
  app.append(topBar("S'entraîner", "#/module/" + id));
  const zone = el("div", {});
  app.append(zone);

  openModule(id, zone, (module) => {
    // Réglage de départ : le dernier utilisé pour ce module, sinon niveau 1.
    let niveau = 1;
    let skill = null;
    if (dernier.id === id) {
      niveau = dernier.niveau;
      // La compétence a pu disparaître du module entre-temps.
      skill = module.skills.some((s) => s && s.id === dernier.skill) ? dernier.skill : null;
    }

    // Réaffiche tout l'écran à chaque clic (plus simple que de modifier
    // chaque bouton), puis remet le focus sur le bouton cliqué pour qu'un
    // utilisateur au clavier ne perde pas sa place.
    function afficher(cleFocus) {
      zone.replaceChildren(contenu());
      if (cleFocus) {
        const bouton = zone.querySelector('[data-cle="' + cleFocus + '"]');
        if (bouton) bouton.focus();
      }
    }

    function contenu() {
      const niveaux = el("div", { class: "chips", role: "group", "aria-label": "Niveau" });
      for (const nv of NIVEAUX) {
        const nombre = questionsDuNiveau(id, module, nv.n, skill).length;
        niveaux.append(chip("niveau-" + nv.n, nv.n === niveau, "Niveau " + nv.n,
          nv.texte + " · " + nombre + " question" + (nombre > 1 ? "s" : ""),
          () => { niveau = nv.n; afficher("niveau-" + nv.n); }));
      }

      const competences = el("div", { class: "chips", role: "group", "aria-label": "Compétence" },
        chip("tout", skill === null, "Tout mélangé", null, () => { skill = null; afficher("tout"); }));
      // Clé = position dans la liste, pas l'id : un id mal écrit dans le module
      // ne peut pas casser la recherche du bouton (querySelector).
      module.skills.forEach((s, i) => {
        if (!s || typeof s.id !== "string") return;
        competences.append(chip("skill-" + i, skill === s.id, richText(String(s.label)), null,
          () => { skill = s.id; afficher("skill-" + i); }));
      });

      // Rien à proposer pour ce réglage : on le dit au lieu d'un écran vide.
      const nombre = questionsDuNiveau(id, module, niveau, skill).length;
      const adresse = "#/module/" + id + "/entrainement/" + niveau + (skill ? "/" + encodeURIComponent(skill) : "");
      const depart = nombre > 0
        ? el("div", { class: "actions" }, el("a", { class: "btn btn-primary", href: adresse }, "Commencer"))
        : message("info", "Pas de question de ce niveau pour cette compétence : choisis un autre niveau.");

      return el("div", {},
        el("h2", { class: "section-title" }, "Niveau"),
        niveaux,
        el("h2", { class: "section-title" }, "Compétence"),
        competences,
        depart,
      );
    }

    afficher(null);
    // Entrée lance directement l'entraînement avec le réglage proposé.
    const commencer = zone.querySelector(".btn-primary");
    if (commencer) commencer.focus({ preventScroll: true });
  });
}
