// Journal des tentatives d'un enfant : un « événement » par réponse.
//
// Pourquoi des événements bruts et pas des compteurs : tout (taux de réussite,
// notes, bilan) est recalculé à partir du journal (js/stats.js). Une erreur de
// calcul se corrige donc dans le code, sans données abîmées à réparer.
//
// Stockage : miniprof.v1.events.<id du profil> = liste de lignes. Une clé par
// profil : un enfant ne voit que son historique, et supprimer un profil
// supprime sa clé.
//
// Une ligne est un tableau court (pas un objet) pour économiser la place
// (risque R4 : ≈ 5 Mo par site) :
//   [date, module, question, compétence, difficulté, mode, juste, durée, réponse, évaluation]
//   date       : secondes depuis 1970 (Date.now() / 1000) ;
//   mode       : "e" (entraînement, premier essai seulement) ou "v" (évaluation) ;
//   juste      : 1 ou 0 ;
//   durée      : secondes passées sur la question ;
//   réponse    : telle que lue par question-view.js ({ q: 5, r: 3 }, "b", "Paris") ;
//   évaluation : null en entraînement ; en évaluation "<date de début>/<mixte|1..4>",
//                commun aux réponses d'une même évaluation (pour retrouver la note).
// Le reste du code ne manipule que des objets nommés : seuls versLigne() et
// depuisLigne() connaissent l'ordre des cases.

import { readKey, writeKey, removeKey } from "./storage.js";

// Une réponse tapée très longue ne doit pas remplir le stockage.
const MAX_TEXTE = 100;

function cle(profilId) {
  return "events." + profilId;
}

// Date en secondes, le format des événements.
export function maintenant() {
  return Math.round(Date.now() / 1000);
}

function versLigne(e) {
  const reponse = typeof e.reponse === "string" ? e.reponse.slice(0, MAX_TEXTE) : e.reponse;
  return [e.date, e.module, e.question, e.skill, e.difficulty, e.mode, e.juste ? 1 : 0,
    e.duree, reponse, e.evaluation || null];
}

function depuisLigne(l) {
  return {
    date: l[0], module: l[1], question: l[2], skill: l[3], difficulty: l[4],
    mode: l[5], juste: l[6] === 1, duree: l[7], reponse: l[8], evaluation: l[9] || null,
  };
}

// Lignes stockées telles quelles (liste vide si rien ou illisible).
function lignes(profilId) {
  const tout = readKey(cle(profilId), []);
  return Array.isArray(tout) ? tout : [];
}

// Événements d'un profil, du plus ancien au plus récent. Défensif : une ligne
// abîmée (modifiée à la main, import raté) est ignorée au lieu de faire
// planter le bilan.
export function listEvents(profilId) {
  return lignes(profilId)
    .filter((l) => Array.isArray(l) && typeof l[0] === "number" && typeof l[1] === "string"
      && typeof l[3] === "string" && (l[5] === "e" || l[5] === "v"))
    .map(depuisLigne);
}

// Ajoute des événements (objets nommés, voir depuisLigne). Plusieurs d'un coup
// pour l'évaluation : une seule écriture, donc tout ou rien.
// Renvoie true si c'est enregistré ; sinon l'appelant prévient l'enfant.
export function addEvents(profilId, evenements) {
  const tout = lignes(profilId).concat(evenements.map(versLigne));
  return writeKey(cle(profilId), tout);
}

export function deleteEvents(profilId) {
  return removeKey(cle(profilId));
}
