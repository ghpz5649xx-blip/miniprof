// Problèmes signalés par les enfants : « cette question (ou sa réponse) me semble fausse ».
//
// Pourquoi une liste à part de flags.js : flags.js retire une question du tirage (modules
// JSON, id de question stable). Les modules HTML tirent leurs questions au hasard, sans id :
// pour que le parent et Claude retrouvent le problème, on garde une COPIE de ce que l'enfant
// voyait (énoncé, choix, réponse attendue, réponse donnée) avec son commentaire facultatif.
// Les lignes de flags.js ne changent pas (les anciens signalements restent intacts).
//
// Stockage : miniprof.v1.signalements = liste d'objets (peu nombreux, lisibles) :
//   { id, date (s), module, profil (id ou null), question (id ou null), enonce,
//     choix: [libellés], attendue, reponse, commentaire }
// Les textes sont du texte brut (pas de HTML), coupés pour ne pas remplir le stockage.
// Lu par js/backup.js (export, restauration) puis par tools/analyse.py.

import { readKey, writeKey } from "./storage.js";
import { maintenant } from "./events.js";
import { APERCU } from "./open-module.js";

const MAX_TEXTE = 400;
const MAX_CHOIX = 8;
const MAX_COMMENTAIRE = 300;

function texte(valeur, max) {
  return valeur === undefined || valeur === null ? "" : String(valeur).trim().slice(0, max);
}

function lignes() {
  const tout = readKey("signalements", []);
  // Défensif : on ne garde que les objets bien formés.
  return Array.isArray(tout)
    ? tout.filter((s) => s !== null && typeof s === "object" && typeof s.id === "string")
    : [];
}

// Enregistre un signalement. `r` : { module, question, enonce, choix, attendue, reponse }
// (tout facultatif sauf module). Renvoie son id, ou null si l'écriture échoue.
// Appelé par les modules JSON (question-view.js) et par suivi.js (modules HTML) : la page
// HTML est générée, on ne garde que des textes courts.
export function addSignalement(r, profilId) {
  if (r.module === APERCU) return "apercu"; // module en aperçu : rien n'est enregistré
  const id = maintenant() + "-" + Math.random().toString(36).slice(2, 6);
  const choix = Array.isArray(r.choix) ? r.choix.slice(0, MAX_CHOIX).map((c) => texte(c, 80)) : [];
  const ligne = {
    id: id,
    date: maintenant(),
    module: texte(r.module, 100),
    profil: profilId || null,
    question: r.question ? texte(r.question, 100) : null,
    enonce: texte(r.enonce, MAX_TEXTE),
    choix: choix,
    attendue: texte(r.attendue, 100),
    reponse: texte(r.reponse, 100),
    commentaire: "",
  };
  return writeKey("signalements", lignes().concat([ligne])) ? id : null;
}

// Ajoute (ou remplace) le commentaire d'un signalement déjà enregistré.
export function commentSignalement(id, commentaire) {
  if (id === "apercu") return true;
  const liste = lignes();
  const ligne = liste.find((s) => s.id === id);
  if (!ligne) return false;
  ligne.commentaire = texte(commentaire, MAX_COMMENTAIRE);
  return writeKey("signalements", liste);
}

// Pour la sauvegarde (js/backup.js).
export function allSignalements() {
  return lignes();
}

export function replaceSignalements(nouvelles) {
  return writeKey("signalements", nouvelles);
}
