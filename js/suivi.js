// Contrat de suivi des modules HTML (modules/<id>.html, voir docs/module-html.md).
//
// Pourquoi : un module HTML est une page autonome générée par un LLM (schémas,
// animations, questions tirées au hasard), impossible à décrire en JSON. Elle
// garde son propre affichage, mais ses réponses doivent arriver dans le même
// journal que les modules JSON (js/events.js) pour compter dans le bilan.
// La page et miniprof sont servis par le même site : ils partagent donc le
// même localStorage.
//
// La page charge ce fichier avec <script type="module" src="../js/suivi.js">,
// puis appelle window.miniprof au moment d'une réponse :
//   miniprof.profil()                    prénom du profil courant, ou null ;
//   miniprof.debutEvaluation(niveau)     clé commune aux réponses d'une évaluation ;
//   miniprof.reponse(r) / reponse([r…])  enregistre une ou plusieurs réponses, avec
//     r = { competence, juste, mode: "e"|"v", difficulte, question, reponse, duree, evaluation }.
// L'id du module est lu dans la fiche de la page (#miniprof-module) : la page
// ne peut pas écrire au nom d'un autre module par erreur.

import { currentProfile } from "./profiles.js";
import { addEvents, maintenant } from "./events.js";
import { el } from "./ui.js";

// Adresse de l'app, calculée depuis ce fichier (js/ est à la racine du site) :
// marche sur GitHub Pages (/miniprof/) comme en local.
const RACINE = new URL("../", import.meta.url).href;

function lireFiche() {
  const bloc = document.getElementById("miniprof-module");
  try {
    const fiche = JSON.parse(bloc.textContent);
    return fiche && typeof fiche.id === "string" ? fiche : null;
  } catch (e) {
    console.warn("miniprof : fiche du module illisible", e);
    return null;
  }
}

const fiche = lireFiche();

// Une réponse de la page -> un événement au format de js/events.js.
// Défensif : la page est générée, on ne garde que des valeurs du bon type.
function versEvenement(r) {
  const mode = r.mode === "v" ? "v" : "e";
  return {
    date: maintenant(),
    module: fiche.id,
    question: String(r.question || r.competence),
    skill: String(r.competence),
    difficulty: Number(r.difficulte) || 1,
    mode: mode,
    juste: r.juste === true,
    duree: Math.round(Number(r.duree) || 0),
    reponse: r.reponse === undefined ? null : r.reponse,
    evaluation: mode === "v" && typeof r.evaluation === "string" ? r.evaluation : null,
  };
}

// Renvoie true si c'est enregistré. Sans profil (ou sans fiche), rien n'est
// enregistré : l'enfant peut quand même réviser, le bandeau l'a prévenu.
function reponse(r) {
  const profil = currentProfile();
  if (!profil || !fiche) return false;
  const liste = (Array.isArray(r) ? r : [r]).filter((x) => x && typeof x.competence === "string");
  if (liste.length === 0) return false;
  return addEvents(profil.id, liste.map(versEvenement));
}

// Même clé que les évaluations des modules JSON : "<date de début>/<niveau>".
function debutEvaluation(niveau) {
  return maintenant() + "/" + (niveau ? String(niveau) : "mixte");
}

function profil() {
  const p = currentProfile();
  return p ? p.name : null;
}

// Bandeau en haut de la page : qui est enregistré, et les liens vers miniprof.
// Styles en ligne : la page a ses propres styles, qu'on ne connaît pas.
function bandeau() {
  const p = currentProfile();
  const style = "display:flex;flex-wrap:wrap;gap:4px 12px;align-items:center;justify-content:center;"
    + "padding:6px 12px;font:600 0.9rem system-ui,-apple-system,sans-serif;"
    + "background:#1f3b57;color:#fff;";
  const lien = (href, texte) => el("a", { href: href, style: "color:#fff;text-decoration:underline" }, texte);
  const contenu = p
    ? [el("span", {}, "Tu es " + p.name), lien(RACINE + "#/", "changer"),
      fiche ? lien(RACINE + "#/module/" + encodeURIComponent(fiche.id) + "/bilan", "mon bilan") : null,
      lien(RACINE + "#/biblio", "mes modules")]
    : [el("span", {}, "Choisis ton profil pour que tes résultats soient gardés :"),
      lien(RACINE + "#/", "choisir")];
  return el("div", { class: "miniprof-bandeau", style: style }, ...contenu);
}

window.miniprof = { profil, reponse, debutEvaluation, racine: RACINE, module: fiche ? fiche.id : null };
document.body.prepend(bandeau());
