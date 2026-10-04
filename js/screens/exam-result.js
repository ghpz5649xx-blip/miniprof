// Résultat d'une évaluation : note, temps, réussite par compétence,
// corrections dépliables et boutons pour la suite.
//
// Affiché par screens/exam.js à la fin de l'évaluation, à la même adresse,
// une fois les réponses enregistrées. Recharger la page relance une nouvelle
// évaluation (le résultat reste visible dans le bilan).

import { el, richText, message } from "../ui.js";
import { correctAnswerText, answerText, boutonSignaler } from "../question-view.js";
import { MESSAGE_ECHEC_SAUVEGARDE } from "../storage.js";

// `evalFinie` : { id, module, reponses: [{ q, reponse, juste }], duree (ms),
//                 recommencer: fonction qui relance une évaluation,
//                 enregistre: false si l'enregistrement a échoué }
export function afficherResultat(zone, evalFinie) {
  const { id, module, reponses } = evalFinie;
  const total = reponses.length;
  const note = reponses.filter((r) => r.juste).length;
  const parCompetence = scoresParCompetence(module, reponses);

  zone.replaceChildren(el("div", {},
    evalFinie.enregistre ? null : message("error", MESSAGE_ECHEC_SAUVEGARDE),
    el("header", { class: "hero" },
      el("p", { class: "exam-score" }, note + " / " + total),
      el("p", {}, appreciation(note / total)),
      el("p", { class: "muted" }, "Temps : " + dureeEnTexte(evalFinie.duree)),
    ),
    el("h2", { class: "section-title" }, "Par compétence"),
    el("div", { class: "card" }, ...parCompetence.map(barreCompetence)),
    el("h2", { class: "section-title" }, "Les corrections"),
    ...reponses.map((r, i) => correction(r, i, id, module)),
    boutons(evalFinie, parCompetence, note < total),
  ));
  window.scrollTo(0, 0);
  const premier = zone.querySelector(".actions .btn");
  if (premier) premier.focus({ preventScroll: true });
}

// Mêmes paliers que le prototype, en proportion : une évaluation peut avoir
// moins de 10 questions (voir composerEvaluation).
function appreciation(taux) {
  if (taux >= 0.9) return "Excellent ! Tu maîtrises ce module.";
  if (taux >= 0.7) return "Très bien ! Encore un petit effort sur ce qui reste.";
  if (taux >= 0.5) return "C'est un bon début. Entraîne-toi sur les points ratés.";
  return "Pas de panique : reprends « Apprendre », puis entraîne-toi.";
}

// 185000 -> « 3 min 05 s »
function dureeEnTexte(ms) {
  const secondes = Math.round(ms / 1000);
  const min = Math.floor(secondes / 60);
  const s = secondes % 60;
  return min > 0 ? min + " min " + String(s).padStart(2, "0") + " s" : s + " s";
}

// Une ligne par compétence présente dans l'évaluation, dans l'ordre du module :
// { skill, label, justes, total, ratees: [questions ratées] }
function scoresParCompetence(module, reponses) {
  const lignes = [];
  for (const s of module.skills) {
    if (!s || typeof s.id !== "string") continue;
    const siennes = reponses.filter((r) => r.q.skill === s.id);
    if (siennes.length === 0) continue;
    lignes.push({
      skill: s.id,
      label: String(s.label),
      justes: siennes.filter((r) => r.juste).length,
      total: siennes.length,
      ratees: siennes.filter((r) => !r.juste).map((r) => r.q),
    });
  }
  return lignes;
}

// Barre de réussite d'une compétence. `ligne` : { label, justes, total },
// et `detail` facultatif (texte à droite, « x/y » sinon).
// Aussi utilisée par le bilan (screens/report.js).
export function barreCompetence(ligne) {
  const taux = ligne.justes / ligne.total;
  const couleur = taux < 0.5 ? "bar-ko" : taux < 0.8 ? "bar-mid" : "bar-ok";
  const remplissage = el("div", { class: "bar-fill " + couleur });
  // Largeur posée par JS et non par un attribut style="…" : la politique de
  // sécurité (CSP) de index.html interdit les attributs style.
  remplissage.style.width = Math.round(taux * 100) + "%";
  return el("div", { class: "skill-score" },
    el("div", { class: "row" },
      el("span", { class: "grow" }, richText(ligne.label)),
      el("strong", {}, ligne.detail || ligne.justes + "/" + ligne.total),
    ),
    el("div", { class: "bar" }, remplissage),
  );
}

// Une correction dépliable (<details> : le navigateur gère l'ouverture seul).
function correction(r, i, id, module) {
  const competence = module.skills.find((s) => s && s.id === r.q.skill);
  return el("details", { class: "card correction" },
    el("summary", {},
      (r.juste ? "✓ " : "✗ ") + (i + 1) + ". ",
      competence ? richText(String(competence.label)) : null,
    ),
    el("p", {}, richText(r.q.prompt)),
    el("p", {}, el("strong", {}, "Ta réponse : "), richText(answerText(r.q, r.reponse))),
    r.juste ? null : el("p", {}, el("strong", {}, "Bonne réponse : "), richText(correctAnswerText(r.q))),
    el("p", { class: "muted" }, richText(r.q.explanation)),
    boutonSignaler(id, r.q),
  );
}

function boutons(evalFinie, parCompetence, aTravailler) {
  const id = evalFinie.id;
  const zone = el("div", { class: "actions" });

  if (aTravailler) {
    // Compétence la plus faible (la première en cas d'égalité) : on propose
    // de l'entraîner au niveau de sa première question ratée, qui existe
    // forcément dans la banque.
    let faible = null;
    for (const l of parCompetence) {
      if (l.ratees.length > 0 && (!faible || l.justes / l.total < faible.justes / faible.total)) faible = l;
    }
    const adresse = "#/module/" + id + "/entrainement/" + faible.ratees[0].difficulty
      + "/" + encodeURIComponent(faible.skill);
    zone.append(el("a", { class: "btn btn-primary", href: adresse }, "Travailler : ", richText(faible.label)));
  }

  zone.append(
    el("button", { class: "btn btn-secondary", onclick: evalFinie.recommencer }, "Recommencer"),
    el("a", { class: "btn btn-secondary", href: "#/module/" + id }, "Accueil"),
  );
  return zone;
}
