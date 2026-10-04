// Écran « S'entraîner » : des questions à volonté, avec indice et correction.
//
// Adresse : #/module/<id>/entrainement/<niveau>[/<compétence>]
// (réglage choisi sur screens/practice-setup.js ; sans compétence : tout mélangé).
//
// Déroulé d'une question :
//   Valider juste            -> bravo, « Question suivante » ;
//   1er essai faux           -> message ciblé (common_errors) ou générique,
//                               puis Réessayer / Un indice / Voir la correction ;
//   2e essai faux, ou « Voir la correction » -> correction, « Question suivante ».
// Seul le 1er essai compte dans les statistiques de la séance.
// Les statistiques et les questions déjà posées sont gardées en mémoire
// seulement : recharger la page recommence une séance.

import { el, clear, topBar, message, richText } from "../ui.js";
import { openModule } from "../open-module.js";
import { renderQuestion, isCorrect, findCommonError, correctAnswerText } from "../question-view.js";
import { questionsDuNiveau, retenirReglage } from "./practice-setup.js";

// Nombre de questions récentes qu'on évite de reposer.
const SANS_REPETER = 10;
// Réussites du premier coup d'affilée pour proposer le niveau suivant.
const SERIE_NIVEAU_SUIVANT = 5;

const BRAVOS = ["Bravo !", "Bien joué !", "Exact !", "Super !", "C'est juste !"];
const ERREUR_GENERIQUE = "Relis bien l'énoncé, puis réessaie. Un indice peut t'aider.";

export function showPractice(id, niveauTexte, skill) {
  const app = clear();
  const reglage = "#/module/" + id + "/entrainement";
  app.append(topBar("S'entraîner", reglage));
  const zone = el("div", {});
  app.append(zone);

  // Le niveau vient de l'adresse, que n'importe qui peut modifier.
  const niveau = Number(niveauTexte);
  if (![1, 2, 3, 4].includes(niveau)) {
    location.replace(reglage);
    return;
  }

  openModule(id, zone, (module) => {
    if (skill && !module.skills.some((s) => s && s.id === skill)) {
      zone.replaceChildren(retourReglage("Cette compétence n'existe pas dans ce module.", reglage));
      return;
    }
    const banque = questionsDuNiveau(module, niveau, skill);
    if (banque.length === 0) {
      zone.replaceChildren(retourReglage("Pas de question de ce niveau pour cette compétence.", reglage));
      return;
    }
    retenirReglage(id, niveau, skill);

    // Statistiques de la séance (premier essai seulement).
    let faites = 0;     // questions auxquelles l'enfant a répondu
    let reussies = 0;   // réussies du premier coup
    let serie = 0;      // réussites du premier coup d'affilée
    const recentes = []; // id des dernières questions posées, la plus récente à la fin

    function questionSuivante() {
      const q = tirerQuestion(banque, recentes);
      recentes.push(q.id);
      if (recentes.length > SANS_REPETER) recentes.shift();
      afficherQuestion(q);
    }

    function afficherQuestion(q) {
      let essai = 1;
      const vue = renderQuestion(q, valider);
      const entete = el("p", { class: "step-count" });
      const zoneIndice = el("div", {});
      const zoneRetour = el("div", {});
      const boutons = el("div", { class: "actions" });

      function majEntete() {
        entete.textContent = "Niveau " + niveau + " : " + reussies + " réussie" + (reussies > 1 ? "s" : "")
          + " du premier coup sur " + faites;
      }

      // Libellé de la compétence de la question (utile en « Tout mélangé »).
      const competence = module.skills.find((s) => s && s.id === q.skill);
      // « Revoir la méthode » seulement si la leçon parle de cette compétence.
      const aUneLecon = module.lesson.some((b) => b.skill === q.skill);

      majEntete();
      zone.replaceChildren(el("div", {},
        entete,
        competence ? el("p", { class: "muted" }, richText(String(competence.label))) : null,
        el("div", { class: "card" }, vue.element),
        zoneIndice,
        zoneRetour,
        boutons,
        aUneLecon
          ? el("a", { class: "btn btn-link", href: "#/module/" + id + "/apprendre/" + encodeURIComponent(q.skill) }, "Revoir la méthode")
          : null,
      ));
      window.scrollTo(0, 0);

      function boutonIndice() {
        return el("button", { class: "btn btn-secondary", onclick: montrerIndice }, "Un indice");
      }
      function montrerIndice() {
        zoneIndice.replaceChildren(message("hint", "**Indice**\n" + q.hint));
      }

      // État « saisie » : l'enfant répond.
      function modeSaisie() {
        vue.deverrouiller();
        boutons.replaceChildren(
          el("button", { class: "btn btn-primary", onclick: valider }, "Valider"),
          boutonIndice(),
        );
      }

      function valider() {
        const lu = vue.lire();
        // Réponse incomplète : simple consigne, l'essai ne compte pas.
        if (lu.consigne) {
          zoneRetour.replaceChildren(message("hint", lu.consigne));
          vue.focus();
          return;
        }
        const juste = isCorrect(q, lu.reponse);
        if (essai === 1) {
          faites = faites + 1;
          if (juste) {
            reussies = reussies + 1;
            serie = serie + 1;
          } else {
            serie = 0;
          }
          // Étape 6 : enregistrer ici l'événement du premier essai.
        }
        if (juste) {
          terminer(true);
        } else if (essai === 1) {
          premiereErreur(lu.reponse);
        } else {
          terminer(false);
        }
      }

      // 1er essai faux : on bloque la saisie le temps de lire le message.
      function premiereErreur(reponse) {
        essai = 2;
        majEntete();
        vue.verrouiller();
        zoneRetour.replaceChildren(
          message("error", "**Pas tout à fait.**\n" + (findCommonError(q, reponse) || ERREUR_GENERIQUE)));
        const reessayer = el("button", {
          class: "btn btn-primary",
          onclick: () => { zoneRetour.replaceChildren(); modeSaisie(); vue.focus(); },
        }, "Réessayer");
        boutons.replaceChildren(
          reessayer,
          boutonIndice(),
          el("button", { class: "btn btn-secondary", onclick: () => terminer(false) }, "Voir la correction"),
        );
        reessayer.focus(); // Entrée = Réessayer
      }

      // Fin de la question : bravo ou correction, puis question suivante.
      function terminer(juste) {
        majEntete();
        vue.verrouiller();
        vue.montrerCorrection();
        if (juste) {
          const bravo = BRAVOS[Math.floor(Math.random() * BRAVOS.length)];
          zoneRetour.replaceChildren(message("ok", bravo + (essai === 2 ? "\nTu as trouvé au deuxième essai." : "")));
        } else {
          zoneRetour.replaceChildren(message("info",
            "**Correction**\nBonne réponse : " + correctAnswerText(q) + "\n" + q.explanation));
        }

        const suivante = el("button", { class: "btn btn-primary", onclick: questionSuivante }, "Question suivante");
        boutons.replaceChildren(suivante);

        // Montée de niveau proposée (jamais imposée), s'il y a des questions
        // au niveau suivant pour ce réglage.
        if (serie >= SERIE_NIVEAU_SUIVANT && niveau < 4
            && questionsDuNiveau(module, niveau + 1, skill).length > 0) {
          zoneRetour.append(message("ok",
            "Tu enchaînes " + serie + " réussites du premier coup : tu peux passer au niveau suivant !"));
          boutons.append(el("a", {
            class: "btn btn-secondary",
            href: "#/module/" + id + "/entrainement/" + (niveau + 1) + (skill ? "/" + encodeURIComponent(skill) : ""),
          }, "Niveau suivant"));
        }
        suivante.focus(); // Entrée = Question suivante
      }

      modeSaisie();
      vue.focus();
    }

    questionSuivante();
  });
}

// Tire une question au hasard en évitant les plus récentes. Si la banque est
// trop petite pour cela, on évite au moins de reposer la toute dernière.
function tirerQuestion(banque, recentes) {
  let possibles = banque.filter((q) => !recentes.includes(q.id));
  if (possibles.length === 0) possibles = banque.filter((q) => q.id !== recentes[recentes.length - 1]);
  if (possibles.length === 0) possibles = banque; // une seule question
  return possibles[Math.floor(Math.random() * possibles.length)];
}

function retourReglage(texte, reglage) {
  return el("div", {},
    message("info", texte),
    el("a", { class: "btn btn-primary", href: reglage }, "Choisir un autre réglage"),
  );
}
