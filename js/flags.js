// Questions signalées « Cette question me semble fausse » (risque R3 : le LLM
// a pu se tromper dans une réponse).
//
// Une question signalée n'est plus tirée (entraînement et évaluation) jusqu'à
// ce qu'on la rétablisse depuis l'accueil du module. Le parent corrige ensuite
// le module en gardant le même id de question.
//
// Stockage : miniprof.v1.flags = [[module, question, date (s), id du profil], ...]
// Une seule liste pour l'appareil (pas une par profil) : une question fausse
// l'est pour tous les enfants. Le profil est noté pour savoir qui l'a signalée.

import { readKey, writeKey } from "./storage.js";
import { maintenant } from "./events.js";

function lignes() {
  const tout = readKey("flags", []);
  // Défensif : on ne garde que les lignes bien formées.
  return Array.isArray(tout) ? tout.filter((l) => Array.isArray(l) && l.length >= 2) : [];
}

// Id des questions signalées d'un module.
export function flaggedIds(moduleId) {
  return lignes().filter((l) => l[0] === moduleId).map((l) => l[1]);
}

// Les questions de la liste, sans les signalées.
export function withoutFlagged(moduleId, questions) {
  const signalees = flaggedIds(moduleId);
  return questions.filter((q) => !signalees.includes(q.id));
}

// Renvoie true si c'est enregistré.
export function flagQuestion(moduleId, questionId, profilId) {
  if (flaggedIds(moduleId).includes(questionId)) return true; // déjà signalée
  return writeKey("flags", lignes().concat([[moduleId, questionId, maintenant(), profilId]]));
}

export function unflagQuestion(moduleId, questionId) {
  return writeKey("flags", lignes().filter((l) => !(l[0] === moduleId && l[1] === questionId)));
}
