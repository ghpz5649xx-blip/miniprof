// Écran « Évaluation » : une série de questions sans aide, puis le résultat.
//
// Adresse : #/module/<id>/evaluation/<mixte|1..4>
// (réglage choisi sur screens/exam-setup.js).
//
// Pendant l'évaluation : ni indice, ni correction, ni « Revoir la méthode ».
// Chaque réponse est gardée en mémoire ; le résultat (screens/exam-result.js)
// s'affiche à la même adresse. Quitter l'écran (← Retour, bouton retour du
// navigateur, recharger) abandonne l'évaluation : rien n'est enregistré.

import { el, clear, topBar, message } from "../ui.js";
import { openModule } from "../open-module.js";
import { renderQuestion, isCorrect } from "../question-view.js";
import { composerEvaluation, retenirReglageEval } from "./exam-setup.js";
import { afficherResultat } from "./exam-result.js";

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
      const questions = composerEvaluation(module, niveau);
      if (questions.length === 0) {
        zone.replaceChildren(
          message("info", "Pas de question de ce niveau dans ce module."),
          el("a", { class: "btn btn-primary", href: reglage }, "Choisir un autre niveau"),
        );
        return;
      }
      const reponses = []; // { q, reponse, juste } dans l'ordre des questions
      const debut = Date.now();

      function afficherQuestion(n) {
        const q = questions[n];
        const derniere = n === questions.length - 1;
        const vue = renderQuestion(q, valider);
        const zoneConsigne = el("div", {});

        function valider() {
          const lu = vue.lire();
          // Réponse incomplète : simple consigne, on reste sur la question.
          if (lu.consigne) {
            zoneConsigne.replaceChildren(message("hint", lu.consigne));
            vue.focus();
            return;
          }
          reponses.push({ q: q, reponse: lu.reponse, juste: isCorrect(q, lu.reponse) });
          // Étape 6 : enregistrer ici l'événement de la réponse.
          if (derniere) {
            afficherResultat(zone, {
              id: id, module: module, reponses: reponses,
              duree: Date.now() - debut, recommencer: demarrer,
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

// Barre de progression : une pastille par question (faite / en cours / à venir).
function pastilles(total, enCours) {
  const liste = el("ol", { class: "exam-dots", "aria-hidden": "true" });
  for (let i = 0; i < total; i++) {
    const etat = i < enCours ? "dot-done" : i === enCours ? "dot-current" : "dot-todo";
    liste.append(el("li", { class: "dot " + etat }));
  }
  return liste;
}
