// Lecture des fichiers JSON : ceux du site (index des modules, modules) et
// ceux choisis sur l'appareil (sauvegarde à restaurer, module en aperçu).
//
// Ce sont les SEULES fonctions asynchrones de l'app : un navigateur ne peut
// lire un fichier qu'avec fetch() ou file.text(), qui sont forcément
// asynchrones. Tout le reste du code (stockage, calculs, affichage) est
// synchrone ; les appelants utilisent .then() / .catch().

// Transforme un texte en données JSON. Synchrone. Lève une Error au message
// affichable tel quel. `nom` : nom du fichier, pour le message.
function parseOuErreur(texte, nom) {
  try {
    return JSON.parse(texte);
  } catch (e) {
    throw new Error(`Le fichier « ${nom} » n'est pas un JSON valide : lance validate.py dessus.`);
  }
}

// Lit un fichier JSON du site. Renvoie les données, ou lève une Error dont le
// message (en français) peut être affiché tel quel.
export async function readJson(url) {
  let reponse;
  try {
    // "no-cache" : le navigateur redemande toujours au serveur si le fichier a
    // changé. Sans cela, un module poussé sur GitHub Pages pourrait rester
    // invisible plusieurs minutes.
    reponse = await fetch(url, { cache: "no-cache" });
  } catch (e) {
    throw new Error(`Impossible de charger « ${url} » (pas de connexion ?).`);
  }
  if (!reponse.ok) {
    throw new Error(`Fichier « ${url} » introuvable (erreur ${reponse.status}).`);
  }
  return parseOuErreur(await reponse.text(), url);
}

// Lit un fichier choisi par l'utilisateur (<input type="file">). Rien n'est
// envoyé sur Internet : le fichier est lu dans la page. Même contrat que readJson.
export async function readJsonFile(file) {
  let texte;
  try {
    texte = await file.text();
  } catch (e) {
    throw new Error(`Impossible de lire le fichier « ${file.name} ».`);
  }
  return parseOuErreur(texte, file.name);
}
