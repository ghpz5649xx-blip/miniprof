// Écran de réglage de l'« Évaluation » : choix « Mixte » ou d'un niveau.
//
// Adresse : #/module/<id>/evaluation
// « Lancer l'évaluation » mène à #/module/<id>/evaluation/<mixte|1..4>
// (voir screens/exam.js).
//
// Ce fichier contient aussi composerEvaluation() : le nombre de questions
// affiché ici et l'évaluation réelle viennent ainsi du même calcul.

import { el, clear, topBar, message, chip } from "../ui.js";
import { openModule } from "../open-module.js";
import { withoutFlagged } from "../flags.js";

const NB_QUESTIONS = 10;
// Mixte : difficulté croissante, pour mettre en confiance avant les questions dures.
const MIXTE = [2, 2, 2, 3, 3, 3, 3, 4, 4, 4];

const NIVEAUX = [
  { n: "mixte", titre: "Mixte", texte: "Du facile au difficile" },
  { n: 1, titre: "Niveau 1", texte: "Pour démarrer" },
  { n: 2, titre: "Niveau 2", texte: "Un peu plus dur" },
  { n: 3, titre: "Niveau 3", texte: "Difficile" },
  { n: 4, titre: "Niveau 4", texte: "Pour les champions" },
];

// Dernier réglage utilisé (bouton « ← Retour » pendant l'évaluation).
// Gardé en mémoire seulement, comme pour l'entraînement.
let dernier = { id: null, niveau: "mixte" };

export function retenirReglageEval(id, niveau) {
  dernier = { id: id, niveau: niveau };
}

// Choisit les questions d'une évaluation. `niveau` : "mixte" ou 1 à 4.
// Pour chaque place, on prend la compétence la moins représentée jusque-là :
// l'évaluation couvre ainsi toutes les compétences du module.
// Niveau fixe : uniquement des questions de ce niveau ; s'il y en a moins de
// 10, l'évaluation est plus courte (mélanger des niveaux fausserait la note).
// Mixte : si une difficulté manque, on prend la plus proche.
// Les questions signalées (js/flags.js) ne sont jamais prises.
// `id` : celui du module, tiré de l'adresse.
export function composerEvaluation(id, module, niveau) {
  const banque = withoutFlagged(id, module.questions);
  const cibles = niveau === "mixte" ? MIXTE : Array(NB_QUESTIONS).fill(niveau);
  const prises = [];
  const parCompetence = {}; // id de compétence -> nombre de questions déjà prises
  for (const d of cibles) {
    const difficultes = niveau === "mixte" ? difficultesProches(d) : [d];
    const q = choisir(banque, prises, parCompetence, difficultes);
    if (!q) break; // plus aucune question disponible
    prises.push(q);
    parCompetence[q.skill] = (parCompetence[q.skill] || 0) + 1;
  }
  // Un remplacement par une difficulté proche peut casser l'ordre croissant :
  // on le rétablit (sort garde l'ordre des questions de même difficulté).
  if (niveau === "mixte") prises.sort((a, b) => a.difficulty - b.difficulty);
  return prises;
}

// 3 -> [3, 2, 4, 1] : la plus proche d'abord, la plus facile en cas d'égalité.
function difficultesProches(d) {
  return [1, 2, 3, 4].sort((a, b) => Math.abs(a - d) - Math.abs(b - d) || a - b);
}

// Une question pas encore prise, de la première difficulté qui en a,
// parmi les compétences les moins représentées. null s'il n'y en a pas.
function choisir(banque, prises, parCompetence, difficultes) {
  for (const d of difficultes) {
    const libres = banque.filter((q) => q.difficulty === d && !prises.includes(q));
    if (libres.length === 0) continue;
    const minimum = Math.min(...libres.map((q) => parCompetence[q.skill] || 0));
    const candidates = libres.filter((q) => (parCompetence[q.skill] || 0) === minimum);
    return candidates[Math.floor(Math.random() * candidates.length)];
  }
  return null;
}

export function showExamSetup(id) {
  const app = clear();
  app.append(topBar("Évaluation", "#/module/" + id));
  const zone = el("div", {});
  app.append(zone);

  openModule(id, zone, (module) => {
    let niveau = dernier.id === id ? dernier.niveau : "mixte";

    // Même principe que le réglage de l'entraînement : tout réafficher à
    // chaque clic, puis rendre le focus au bouton cliqué.
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
        const nombre = composerEvaluation(id, module, nv.n).length;
        niveaux.append(chip("niveau-" + nv.n, nv.n === niveau, nv.titre,
          nv.texte + " · " + nombre + " question" + (nombre > 1 ? "s" : ""),
          () => { niveau = nv.n; afficher("niveau-" + nv.n); }));
      }

      const depart = composerEvaluation(id, module, niveau).length > 0
        ? el("div", { class: "actions" },
          el("a", { class: "btn btn-primary", href: "#/module/" + id + "/evaluation/" + niveau }, "Lancer l'évaluation"))
        : message("info", "Pas de question de ce niveau dans ce module : choisis un autre niveau.");

      return el("div", {},
        message("info", "**Prête ou prêt pour l'évaluation ?**\n" + NB_QUESTIONS
          + " questions, sans indice. Tu vois les corrections à la fin.\nPrends un brouillon et un stylo."),
        el("h2", { class: "section-title" }, "Niveau"),
        niveaux,
        depart,
      );
    }

    afficher(null);
    // Entrée lance directement l'évaluation avec le réglage proposé.
    const lancer = zone.querySelector(".btn-primary");
    if (lancer) lancer.focus({ preventScroll: true });
  });
}
