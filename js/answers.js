// Comparaison tolérante entre la saisie de l'enfant et la bonne réponse.
//
// Pourquoi tolérante : un enfant qui tape « 3,5 », « Éléphant » ou « 1 000 »
// a juste ; on ne veut pas le pénaliser pour une virgule, une majuscule ou un
// espace. Ces règles servent à la leçon (mini-étapes) et serviront aux questions.
//
// SYNCHRONISATION : normalizeText() DOIT rester identique à normalize_text()
// de tools/common.py. Les cas d'exemple communs sont dans
// tools/tests/fixtures/normalisation.json (testés en Python, et côté JS par
// l'extrait de console de docs/recette.md, étape 3).

// minuscules, sans accents, apostrophes unifiées, espaces multiples réduits,
// ponctuation finale (. ! ? ; : ,) ignorée.
export function normalizeText(s) {
  let t = String(s).normalize("NFD");
  t = t.replace(/\p{Mn}/gu, ""); // retire les accents séparés par NFD
  t = t.toLowerCase().replace(/’/g, "'").replace(/ /g, " ").replace(/ /g, " ");
  t = t.replace(/\s+/g, " ").trim();
  t = t.replace(/[.!?;:,\s]+$/, "");
  return t;
}

// Lit un nombre tapé par l'enfant. Renvoie le nombre, ou null si la saisie
// n'en est pas un. Espaces ignorés (« 1 000 »), virgule ou point (« 3,5 »),
// signe moins accepté (« -2 », y compris le vrai signe moins « − »).
export function parseNumber(s) {
  const t = String(s).replace(/\s/g, "").replace(",", ".").replace("−", "-");
  // Expression stricte : on refuse « 12abc » ou « 1.2.3 », que parseFloat
  // accepterait en partie.
  if (!/^-?(\d+(\.\d*)?|\.\d+)$/.test(t)) return null;
  return Number(t);
}

// Vrai si la saisie correspond à une réponse simple du module (un nombre ou
// un texte court, voir "reponse_simple" dans le schéma).
// Attention : pour une réponse numérique, vérifier d'abord avec parseNumber()
// que la saisie est bien un nombre, pour afficher « Écris un nombre. ».
export function isCorrectSimple(saisie, answer) {
  if (typeof answer === "number") return parseNumber(saisie) === answer;
  return normalizeText(saisie) === normalizeText(answer);
}
