// Accueil d'un module : titre, description, les 4 activités, la dernière note
// d'évaluation, et les questions signalées (avec « Rétablir »).

import { el, clear, topBar, message, richText } from "../ui.js";
import { openModule } from "../open-module.js";
import { currentProfile } from "../profiles.js";
import { listEvents } from "../events.js";
import { dernieresEvaluations } from "../stats.js";
import { flaggedIds, unflagQuestion } from "../flags.js";
import { MESSAGE_ECHEC_SAUVEGARDE } from "../storage.js";

// `page` : sous-adresse de l'activité (#/module/<id>/<page>).
const ACTIVITES = [
  { titre: "Apprendre", texte: "La leçon, pas à pas", page: "apprendre" },
  { titre: "S'entraîner", texte: "Des questions à volonté, avec indices et corrections", page: "entrainement" },
  { titre: "Évaluation", texte: "10 questions, sans aide, avec une note à la fin", page: "evaluation" },
  { titre: "Bilan", texte: "Ce qui est réussi, ce qu'il reste à travailler", page: "bilan" },
];

export function showModuleHome(id) {
  const app = clear();
  app.append(topBar("Module", "#/biblio"));
  const zone = el("div", {});
  app.append(zone);
  openModule(id, zone, (module, warnings) => {
    // Réaffichée après « Rétablir » une question signalée.
    function afficher(erreur) {
      zone.replaceChildren(contenuModule(id, module, warnings, erreur, afficher));
    }
    afficher(null);
  });
}

// `id` : celui de l'adresse, déjà vérifié par openModule (plus sûr que
// module.id, écrit dans le fichier).
function contenuModule(id, module, warnings, erreur, reafficher) {
  const contenu = el("div", {},
    erreur ? message("error", erreur) : null,
    el("header", { class: "hero" },
      el("h2", {}, richText(module.title)),
      el("p", {}, richText(module.description)),
      el("p", { class: "muted" }, String(module.level) + " · " + module.questions.length + " questions"),
    ),
  );
  for (const w of warnings) contenu.append(message("hint", w));

  // Dernière évaluation de l'enfant sur ce module, recalculée depuis son journal.
  const evenements = listEvents(currentProfile().id).filter((e) => e.module === id);
  const derniere = dernieresEvaluations(evenements, 1)[0];

  const grille = el("div", { class: "stack" });
  for (const a of ACTIVITES) {
    grille.append(
      el("a", { class: "card card-link card-activity", href: "#/module/" + id + "/" + a.page },
        el("span", { class: "card-title" }, a.titre),
        el("span", { class: "card-text" }, a.texte),
        a.page === "evaluation" && derniere
          ? el("span", { class: "badge" }, "Dernière note : " + derniere.note + " / " + derniere.total)
          : null,
      ),
    );
  }
  contenu.append(grille);
  const bloc = signalees(id, module, reafficher);
  if (bloc) contenu.append(bloc);
  return contenu;
}

// Bloc dépliable « Questions signalées (n) », ou null s'il n'y en a pas.
// « Rétablir » remet la question dans les tirages (après correction du module,
// ou si le signalement était une erreur).
function signalees(id, module, reafficher) {
  const ids = flaggedIds(id);
  if (ids.length === 0) return null;
  const bloc = el("details", { class: "card correction flagged" },
    el("summary", {}, "Questions signalées (" + ids.length + ")"),
    el("p", { class: "muted" }, "Elles ne sont plus posées. Un adulte vérifie la réponse dans le module, puis les rétablit."),
  );
  for (const qid of ids) {
    // La question a pu disparaître du module depuis le signalement.
    const q = module.questions.find((x) => x.id === qid);
    bloc.append(el("div", { class: "flagged-row" },
      el("p", {}, el("strong", {}, String(qid) + " : "), q ? richText(q.prompt) : "question absente du module"),
      el("button", {
        class: "btn btn-secondary btn-small",
        onclick: () => {
          const ok = unflagQuestion(id, qid);
          reafficher(ok ? null : MESSAGE_ECHEC_SAUVEGARDE);
          // Le bloc reste ouvert s'il reste des questions signalées.
          const nouveau = document.querySelector(".flagged");
          if (nouveau) nouveau.open = true;
        },
      }, "Rétablir"),
    ));
  }
  return bloc;
}
