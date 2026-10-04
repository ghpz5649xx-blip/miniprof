// Affichage d'une question de la banque et correction de la réponse.
//
// Utilisé par l'entraînement et par l'évaluation : les deux
// affichent les questions de la même façon, seuls les boutons autour changent.
//
// Trois types de questions (voir "question" dans schema/module.schema.json) :
//   number : une ou plusieurs cases numériques (« quotient », « reste »…) ;
//   choice : un QCM ;
//   text   : une réponse courte.
//
// La réponse lue a une forme différente selon le type :
//   number : { q: 5, r: 3 }  (clé de la case -> nombre tapé)
//   choice : "b"             (id du choix)
//   text   : "Paris"         (texte tapé)

import { el, richText, message } from "./ui.js";
import { parseNumber, isCorrectSimple } from "./answers.js";
import { flagQuestion } from "./flags.js";
import { currentProfile } from "./profiles.js";
import { MESSAGE_ECHEC_SAUVEGARDE } from "./storage.js";

// Crée l'affichage de la question `q`. `auValider` est appelée quand
// l'enfant appuie sur Entrée dans une case.
// Renvoie un objet :
//   element             : à insérer dans la page ;
//   lire()              -> { consigne: "…" } si la réponse est incomplète,
//                          sinon { reponse: … } ;
//   focus()             : met le curseur dans la case à compléter ;
//   verrouiller()       : empêche de modifier la réponse ;
//   deverrouiller()     : l'autorise à nouveau ;
//   montrerCorrection() : colore la réponse (vert juste, rouge faux) et
//                         surligne le bon choix d'un QCM.
// Pourquoi un objet de fonctions : l'écran appelant n'a pas à connaître le
// détail (cases, boutons de choix…) de chaque type de question.
export function renderQuestion(q, auValider) {
  let vue;
  if (q.type === "number") vue = vueNombres(q, auValider);
  else if (q.type === "choice") vue = vueChoix(q);
  else vue = vueTexte(q, auValider);
  vue.element = el("div", {},
    el("p", { class: "question-prompt" }, richText(q.prompt)),
    vue.saisie,
  );
  return vue;
}

// Vrai si la réponse (lue par lire()) est juste.
export function isCorrect(q, reponse) {
  if (q.type === "number") return q.fields.every((f) => reponse[f.key] === f.answer);
  if (q.type === "choice") return String(reponse) === String(q.answer);
  return q.accepted.some((a) => isCorrectSimple(reponse, a));
}

// Message ciblé si la réponse correspond à une erreur fréquente prévue par
// le module (`common_errors`), sinon null.
export function findCommonError(q, reponse) {
  const erreurs = Array.isArray(q.common_errors) ? q.common_errors : [];
  for (const e of erreurs) {
    // Défensif : une erreur mal écrite dans le module est ignorée.
    if (!e || typeof e !== "object" || typeof e.message !== "string") continue;
    if (correspond(q, e.when, reponse)) return e.message;
  }
  return null;
}

function correspond(q, when, reponse) {
  if (q.type === "number") {
    // { "r": 27 } : seules les cases citées doivent correspondre.
    if (!when || typeof when !== "object") return false;
    const cles = Object.keys(when);
    return cles.length > 0 && cles.every((cle) => reponse[cle] === when[cle]);
  }
  if (q.type === "choice") return String(when) === String(reponse);
  if (typeof when !== "string" && typeof when !== "number") return false;
  return isCorrectSimple(reponse, when);
}

// Bonne réponse en texte, pour l'encadré de correction.
export function correctAnswerText(q) {
  if (q.type === "number") return casesEnTexte(q, (f) => f.answer);
  if (q.type === "choice") return libelleChoix(q, q.answer);
  return String(q.accepted[0]);
}

// Réponse de l'enfant (lue par lire()) en texte, pour les corrections de
// l'évaluation : même présentation que la bonne réponse, pour comparer.
export function answerText(q, reponse) {
  if (q.type === "number") return casesEnTexte(q, (f) => reponse[f.key]);
  if (q.type === "choice") return libelleChoix(q, reponse);
  return String(reponse);
}

// « quotient = 5, reste = 3 » ; `valeur(f)` donne le nombre de la case f.
function casesEnTexte(q, valeur) {
  return q.fields.map((f) => f.label + " = " + nombreEnTexte(valeur(f)) + (f.unit ? " " + f.unit : "")).join(", ");
}

// Libellé du choix d'id `id` (l'id lui-même si on ne le trouve pas).
function libelleChoix(q, id) {
  const choix = q.choices.find((c) => String(c.id) === String(id));
  return choix ? choix.label : String(id);
}

// 3.5 -> « 3,5 » : l'écriture française qu'apprend l'enfant.
function nombreEnTexte(n) {
  return String(n).replace(".", ",").replace("-", "−");
}

// « Cette question me semble fausse » : signale la question (elle ne sera plus
// tirée) et se remplace par un remerciement. `id` : celui du module (adresse).
export function boutonSignaler(id, q) {
  const zone = el("div", {});
  const bouton = el("button", {
    class: "btn btn-link",
    onclick: () => {
      const ok = flagQuestion(id, q.id, currentProfile().id);
      zone.replaceChildren(ok
        ? message("info", "Merci ! Cette question ne te sera plus posée, un adulte va la vérifier.")
        : message("error", MESSAGE_ECHEC_SAUVEGARDE));
    },
  }, "Cette question me semble fausse");
  zone.append(bouton);
  return zone;
}

// Entrée dans une case = bouton « Valider ».
function surEntree(auValider) {
  return (e) => {
    if (e.key === "Enter") { e.preventDefault(); auValider(); }
  };
}

// --- Cases numériques -------------------------------------------------------

function vueNombres(q, auValider) {
  // Clavier numérique sur téléphone. Mais le clavier numérique de l'iPhone n'a
  // pas de signe moins : si une réponse est négative, on garde le clavier normal.
  const negatif = q.fields.some((f) => f.answer < 0);
  const champs = q.fields.map(() => el("input", {
    type: "text",
    class: "field-input",
    inputmode: negatif ? null : "decimal",
    autocomplete: "off",
    onkeydown: surEntree(auValider),
  }));
  // <label> autour de la case : cliquer sur « quotient » place le curseur
  // dans sa case, et les lecteurs d'écran annoncent le libellé.
  const lignes = q.fields.map((f, i) =>
    el("label", { class: "field-row" },
      el("span", { class: "field-label" }, richText(f.label)),
      champs[i],
      f.unit ? el("span", {}, richText(f.unit)) : null,
    ),
  );

  return {
    saisie: el("div", {}, ...lignes),
    lire() {
      const valeurs = {};
      for (let i = 0; i < q.fields.length; i++) {
        const texte = champs[i].value.trim();
        if (texte === "") {
          return { consigne: q.fields.length > 1 ? "Remplis toutes les cases." : "Écris ta réponse." };
        }
        const n = parseNumber(texte);
        if (n === null) {
          return { consigne: q.fields.length > 1 ? "Écris un nombre dans chaque case." : "Écris un nombre." };
        }
        valeurs[q.fields[i].key] = n;
      }
      return { reponse: valeurs };
    },
    focus() {
      // La première case vide ou mal remplie, sinon la première : sa saisie
      // est sélectionnée pour être corrigée directement.
      const cible = champs.find((c) => parseNumber(c.value) === null) || champs[0];
      cible.focus();
      cible.select();
    },
    verrouiller() { champs.forEach((c) => { c.disabled = true; }); },
    deverrouiller() { champs.forEach((c) => { c.disabled = false; }); },
    montrerCorrection() {
      q.fields.forEach((f, i) => {
        champs[i].classList.add(parseNumber(champs[i].value) === f.answer ? "is-ok" : "is-ko");
      });
    },
  };
}

// --- QCM ------------------------------------------------------------------

function vueChoix(q) {
  let choisi = null; // id du choix sélectionné
  const boutons = [];
  for (const c of q.choices) {
    const bouton = el("button", {
      type: "button",
      class: "btn choice",
      // aria-pressed : le choix sélectionné est annoncé aux lecteurs d'écran
      // et sert aussi de repère pour le style (css/style.css).
      "aria-pressed": "false",
      onclick: () => {
        choisi = c.id;
        boutons.forEach((b) => b.setAttribute("aria-pressed", String(b === bouton)));
      },
    }, richText(c.label));
    boutons.push(bouton);
  }

  return {
    saisie: el("div", { class: "stack" }, ...boutons),
    lire() {
      return choisi === null ? { consigne: "Choisis une réponse." } : { reponse: choisi };
    },
    focus() { boutons[0].focus(); },
    verrouiller() { boutons.forEach((b) => { b.disabled = true; }); },
    deverrouiller() { boutons.forEach((b) => { b.disabled = false; }); },
    montrerCorrection() {
      q.choices.forEach((c, i) => {
        if (String(c.id) === String(q.answer)) boutons[i].classList.add("is-ok");
        else if (c.id === choisi) boutons[i].classList.add("is-ko");
      });
    },
  };
}

// --- Réponse courte -------------------------------------------------------

function vueTexte(q, auValider) {
  const champ = el("input", {
    type: "text",
    class: "field-input field-input-wide",
    autocomplete: "off",
    // Pas de correction automatique du téléphone : elle changerait la réponse.
    autocapitalize: "off",
    autocorrect: "off",
    spellcheck: "false",
    "aria-label": "Ta réponse",
    onkeydown: surEntree(auValider),
  });

  return {
    saisie: el("div", { class: "field-row" }, champ),
    lire() {
      const texte = champ.value.trim();
      return texte === "" ? { consigne: "Écris ta réponse." } : { reponse: texte };
    },
    focus() { champ.focus(); champ.select(); },
    verrouiller() { champ.disabled = true; },
    deverrouiller() { champ.disabled = false; },
    montrerCorrection() {
      const juste = q.accepted.some((a) => isCorrectSimple(champ.value, a));
      champ.classList.add(juste ? "is-ok" : "is-ko");
    },
  };
}
