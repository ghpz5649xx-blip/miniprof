// Écran « Bilan » d'un enfant : ce qui est réussi, ce qu'il reste à travailler.
//
// Adresses :
//   #/bilan                tous les modules (lien « Mon bilan » de la bibliothèque) ;
//   #/module/<id>/bilan    un seul module (carte « Bilan » de l'accueil du module).
//
// Tout est recalculé à partir du journal du profil courant (js/events.js,
// calculs dans js/stats.js) : un enfant ne voit que son propre bilan.
// Titres des modules et libellés des compétences : lus dans modules/index.json
// (un seul petit fichier, au lieu de télécharger chaque module).

import { el, clear, topBar, message, richText } from "../ui.js";
import { currentProfile } from "../profiles.js";
import { readJson } from "../loader.js";
import { listEvents } from "../events.js";
import { syntheseGlobale, scoresParCompetence, dernieresEvaluations } from "../stats.js";
import { barreCompetence } from "./exam-result.js";

const NB_EVALUATIONS = 10;

// `moduleId` : null pour le bilan de tous les modules.
export function showReport(moduleId) {
  const app = clear();
  const profil = currentProfile();
  const retour = moduleId ? "#/module/" + encodeURIComponent(moduleId) : "#/biblio";
  app.append(topBar("Bilan de " + profil.name, retour));
  const zone = el("div", {}, el("p", { class: "muted" }, "Chargement…"));
  app.append(zone);
  const monAdresse = location.hash;

  let evenements = listEvents(profil.id);
  if (moduleId) evenements = evenements.filter((e) => e.module === moduleId);

  // Si l'index est illisible, le bilan s'affiche quand même, avec les id à
  // la place des titres : les résultats de l'enfant comptent plus que les libellés.
  readJson("modules/index.json")
    .then((index) => {
      if (location.hash !== monAdresse) return; // l'enfant est parti entre-temps
      const modules = index && Array.isArray(index.modules) ? index.modules : [];
      zone.replaceChildren(contenu(moduleId, evenements, modules));
    })
    .catch(() => {
      if (location.hash !== monAdresse) return;
      zone.replaceChildren(contenu(moduleId, evenements, []));
    });
}

function contenu(moduleId, evenements, modules) {
  const mention = el("p", { class: "muted" }, "Les résultats sont enregistrés dans le navigateur de cet appareil.");
  if (evenements.length === 0) {
    return el("div", {},
      message("info", "Pas encore de résultat. Entraîne-toi ou fais une évaluation : ton bilan apparaîtra ici."),
      mention,
    );
  }

  const tousModules = moduleId === null;
  const synthese = syntheseGlobale(evenements);
  const scores = scoresParCompetence(evenements);

  return el("div", {},
    el("p", { class: "report-summary" },
      synthese.total + " question" + (synthese.total > 1 ? "s" : "") + " traitée" + (synthese.total > 1 ? "s" : "")
      + ", dont " + synthese.reussies + " réussie" + (synthese.reussies > 1 ? "s" : "")
      + " du premier coup (" + synthese.pourcent + " %)"),
    el("h2", { class: "section-title" }, "À travailler"),
    aTravailler(scores, modules, tousModules),
    el("h2", { class: "section-title" }, "Réussite par compétence"),
    ...parModule(moduleId, scores, modules, tousModules),
    el("h2", { class: "section-title" }, "Dernières évaluations"),
    evaluations(evenements, modules, tousModules),
    mention,
  );
}

// Entrée de l'index pour un module (null s'il n'y est plus).
function infoModule(modules, id) {
  return modules.find((m) => m && m.id === id) || null;
}

function titreModule(modules, id) {
  const m = infoModule(modules, id);
  return m ? String(m.title) : id;
}

// Libellé d'une compétence ; son id si le module ne la connaît plus.
function libelleCompetence(modules, moduleId, skill) {
  const m = infoModule(modules, moduleId);
  const s = m && Array.isArray(m.skills) ? m.skills.find((x) => x && x.id === skill) : null;
  return s ? String(s.label) : skill;
}

function aTravailler(scores, modules, tousModules) {
  const liste = scores.filter((s) => s.aTravailler);
  if (liste.length === 0) return message("ok", "Rien à signaler : continue comme ça !");
  // Les plus faibles d'abord.
  liste.sort((a, b) => a.taux - b.taux);
  return el("div", { class: "stack" }, ...liste.map((s) => {
    const raison = Math.round(s.taux * 100) + " % de réussite" + (s.enBaisse ? ", en baisse" : "");
    const adresse = "#/module/" + encodeURIComponent(s.module) + "/entrainement/" + s.niveau
      + "/" + encodeURIComponent(s.skill);
    return el("div", { class: "card" },
      el("span", { class: "card-title" }, richText(libelleCompetence(modules, s.module, s.skill))),
      tousModules ? el("span", { class: "card-text" }, richText(titreModule(modules, s.module))) : null,
      el("span", { class: "card-text" }, raison),
      el("div", { class: "actions" }, el("a", { class: "btn btn-primary", href: adresse }, "Travailler ce point")),
    );
  }));
}

// Une carte par module travaillé : une barre par compétence du module,
// ou « pas encore travaillé ».
function parModule(moduleId, scores, modules, tousModules) {
  // Modules à montrer : celui de l'adresse, ou tous ceux qui ont des résultats
  // (dans l'ordre de la bibliothèque, puis ceux qui n'y sont plus).
  let ids;
  if (!tousModules) {
    ids = [moduleId];
  } else {
    const travailles = scores.map((s) => s.module);
    ids = modules.map((m) => m.id).filter((id) => travailles.includes(id));
    for (const id of travailles) if (!ids.includes(id)) ids.push(id);
  }

  return ids.map((id) => {
    const m = infoModule(modules, id);
    const siens = scores.filter((s) => s.module === id);
    // Compétences du module, plus celles du journal qu'il ne connaît plus.
    const skills = m && Array.isArray(m.skills) ? m.skills.filter((s) => s && typeof s.id === "string").map((s) => s.id) : [];
    for (const s of siens) if (!skills.includes(s.skill)) skills.push(s.skill);

    const carte = el("div", { class: "card" },
      tousModules ? el("h3", { class: "report-module" }, richText(titreModule(modules, id))) : null);
    for (const skill of skills) {
      const label = libelleCompetence(modules, id, skill);
      const score = siens.find((s) => s.skill === skill);
      if (score) {
        carte.append(barreCompetence({
          label: label, justes: score.justes, total: score.total,
          detail: Math.round(score.taux * 100) + " % · " + score.justes + "/" + score.total,
        }));
      } else {
        carte.append(el("div", { class: "skill-score row" },
          el("span", { class: "grow" }, richText(label)),
          el("span", { class: "muted" }, "pas encore travaillé"),
        ));
      }
    }
    return carte;
  });
}

function evaluations(evenements, modules, tousModules) {
  const liste = dernieresEvaluations(evenements, NB_EVALUATIONS);
  if (liste.length === 0) return el("p", { class: "muted" }, "Pas encore d'évaluation.");
  return el("div", { class: "card" }, ...liste.map((ev) =>
    el("div", { class: "row report-exam" },
      el("span", { class: "grow" },
        dateEnTexte(ev.date) + " · " + (ev.niveau === "mixte" ? "Mixte" : "Niveau " + ev.niveau),
        tousModules ? el("span", { class: "card-text" }, richText(titreModule(modules, ev.module))) : null,
      ),
      el("strong", {}, ev.note + " / " + ev.total),
    ),
  ));
}

// Secondes depuis 1970 -> « 4 oct. 2026 »
function dateEnTexte(secondes) {
  return new Date(secondes * 1000).toLocaleDateString("fr-FR", { day: "numeric", month: "short", year: "numeric" });
}
