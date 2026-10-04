// Écran « Évaluation » : une série de questions sans aide, puis le résultat.
//
// Adresse : #/module/<id>/evaluation/<mixte|1..4>
// (réglage choisi sur screens/exam-setup.js).
//
// Pendant l'évaluation : ni indice, ni correction, ni « Revoir la méthode ».
// Chaque réponse est gardée en mémoire. À la fin seulement, toutes les réponses
// sont enregistrées d'un coup dans le journal de l'enfant (js/events.js), puis
// le résultat (screens/exam-result.js) s'affiche à la même adresse.
// Quitter l'écran (← Retour, bouton retour du navigateur, recharger) abandonne
// l'évaluation : rien n'est enregistré, une évaluation à moitié faite ne
// fausse pas le bilan.

import { el, clear, topBar, message } from "../ui.js";
import { openModule } from "../open-module.js";
import { renderQuestion, isCorrect } from "../question-view.js";
import { composerEvaluation, retenirReglageEval } from "./exam-setup.js";
import { afficherResultat } from "./exam-result.js";
import { currentProfile } from "../profiles.js";
import { addEvents, maintenant } from "../events.js";

export function showExam(id, niveauTexte) {
  const app = clear();
  const reglage = "#/module/" + id + "/evaluation";
  app.append(topBar("Évaluation", reglage));
  const zone = el("div", {});
  app.append(zone);

  // Le niveau vient de l'adresse, que n'importe qui peut modifier.
  const niveau = niveauTexte === "mixte" ? "mixte" : Number(niveauTexte);
  if (niveau !== "mixte" && ![1, 2, 3, 4].includes(niveau)) {
    location.replace(reglage);
    return;
  }

  openModule(id, zone, (module) => {
    retenirReglageEval(id, niveau);

    // Appelée au départ, et par « Recommencer » sur l'écran de résultat
    // (l'adresse ne change pas : il faut relancer nous-mêmes).
    function demarrer() {
      const questions = composerEvaluation(id, module, niveau);
      if (questions.length === 0) {
        zone.replaceChildren(
          message("info", "Pas de question de ce niveau dans ce module."),
          el("a", { class: "btn btn-primary", href: reglage }, "Choisir un autre niveau"),
        );
        return;
      }
      const reponses = []; // { q, reponse, juste, duree (ms) } dans l'ordre des questions
      const debut = Date.now();

      function afficherQuestion(n) {
        const q = questions[n];
        const derniere = n === questions.length - 1;
        const vue = renderQuestion(q, valider);
        const zoneConsigne = el("div", {});
        const affichee = Date.now(); // pour la durée enregistrée

        function valider() {
          const lu = vue.lire();
          // Réponse incomplète : simple consigne, on reste sur la question.
          if (lu.consigne) {
            zoneConsigne.replaceChildren(message("hint", lu.consigne));
            vue.focus();
            return;
          }
          reponses.push({ q: q, reponse: lu.reponse, juste: isCorrect(q, lu.reponse), duree: Date.now() - affichee });
          if (derniere) {
            afficherResultat(zone, {
              id: id, module: module, reponses: reponses,
              duree: Date.now() - debut, recommencer: demarrer,
              enregistre: enregistrer(id, niveau, debut, reponses),
            });
          } else {
            afficherQuestion(n + 1);
          }
        }

        zone.replaceChildren(el("div", {},
          pastilles(questions.length, n),
          el("p", { class: "step-count" }, "Question " + (n + 1) + " sur " + questions.length),
          el("div", { class: "card" }, vue.element),
          zoneConsigne,
          el("div", { class: "actions" },
            el("button", { class: "btn btn-primary", onclick: valider },
              derniere ? "Valider et terminer" : "Valider et continuer")),
        ));
        window.scrollTo(0, 0);
        vue.focus();
      }

      afficherQuestion(0);
    }

    demarrer();
  });
}

// Enregistre toutes les réponses d'une évaluation (une seule écriture).
// Clé d'évaluation commune "<début en s>/<niveau>" : le bilan s'en sert pour
// regrouper les réponses et retrouver note, date et niveau.
// Renvoie true si c'est enregistré.
function enregistrer(id, niveau, debut, reponses) {
  const cle = Math.round(debut / 1000) + "/" + niveau;
  const date = maintenant();
  return addEvents(currentProfile().id, reponses.map((r) => ({
    date: date, module: id, question: r.q.id, skill: r.q.skill, difficulty: r.q.difficulty,
    mode: "v", juste: r.juste, duree: Math.round(r.duree / 1000), reponse: r.reponse, evaluation: cle,
  })));
}

// Barre de progression : une pastille par question (faite / en cours / à venir).
function pastilles(total, enCours) {
  const liste = el("ol", { class: "exam-dots", "aria-hidden": "true" });
  for (let i = 0; i < total; i++) {
    const etat = i < enCours ? "dot-done" : i === enCours ? "dot-current" : "dot-todo";
    liste.append(el("li", { class: "dot " + etat }));
  }
  return liste;
}
