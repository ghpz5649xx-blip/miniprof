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
//     r = { competence, juste, mode: "e"|"v", difficulte, question, reponse, duree, evaluation } ;
//   miniprof.signaler(s)                 l'enfant signale la question affichée : copie de ce qu'il
//     voyait, s = { enonce, choix: [libellés], attendue, reponse } (textes bruts) ; renvoie l'id
//     du signalement, ou null s'il n'est pas enregistré ;
//   miniprof.commenter(id, texte)        ajoute son commentaire facultatif à ce signalement.
// L'id du module est lu dans la fiche de la page (#miniprof-module) : la page
// ne peut pas écrire au nom d'un autre module par erreur.

import { profilActif } from "./profiles.js";
import { toucher, garderSession, adresseChoix } from "./activite.js";
import { addEvents, maintenant } from "./events.js";
import { addSignalement, commentSignalement } from "./signalements.js";
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

// Page de ce module, pour y revenir après le choix du profil ("modules/<id>.html").
function adresseDeRetour() {
  const chemin = location.href.split(/[?#]/)[0];
  return chemin.startsWith(RACINE) ? chemin.slice(RACINE.length) : null;
}

// Profil absent ou pas utilisé depuis 30 minutes (plan P008) : choix du profil, puis retour ici.
// Une question perdue plutôt qu'un résultat chez la mauvaise personne.
function redemanderProfil() {
  location.replace(adresseChoix(adresseDeRetour()));
}
if (fiche && !profilActif()) redemanderProfil();
// Page restée ouverte : le toucher suivant n'atteint pas la page (js/activite.js).
garderSession(() => false, redemanderProfil);

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

// Renvoie true si c'est enregistré. Sans profil actif (ou sans fiche), rien n'est enregistré
// (la page a normalement déjà renvoyé vers le choix du profil, voir plus haut).
function reponse(r) {
  const profil = profilActif();
  if (!profil || !fiche) return false;
  toucher(false);
  const liste = (Array.isArray(r) ? r : [r]).filter((x) => x && typeof x.competence === "string");
  if (liste.length === 0) return false;
  return addEvents(profil.id, liste.map(versEvenement));
}

// Signalement d'une question (js/signalements.js). Les questions d'un module HTML n'ont pas
// d'id stable : on garde l'énoncé, les choix et les réponses. Enregistré même sans profil
// (profil null) : un problème de question compte pour tout le monde.
function signaler(s) {
  if (!fiche || s === null || typeof s !== "object") return null;
  const profil = profilActif();
  return addSignalement({
    module: fiche.id, enonce: s.enonce, choix: s.choix, attendue: s.attendue, reponse: s.reponse,
  }, profil ? profil.id : null);
}

function commenter(id, texte) {
  return typeof id === "string" && commentSignalement(id, texte);
}

// Même clé que les évaluations des modules JSON : "<date de début>/<niveau>".
function debutEvaluation(niveau) {
  return maintenant() + "/" + (niveau ? String(niveau) : "mixte");
}

function profil() {
  const p = profilActif();
  return p ? p.name : null;
}

// Bandeau en haut de la page : qui est enregistré, et les liens vers miniprof.
// Styles en ligne : la page a ses propres styles, qu'on ne connaît pas.
function bandeau() {
  const p = profilActif();
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

window.miniprof = { profil, reponse, debutEvaluation, signaler, commenter, racine: RACINE, module: fiche ? fiche.id : null };
document.body.prepend(bandeau());
