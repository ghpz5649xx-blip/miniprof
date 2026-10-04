// Chargement des fichiers JSON (index des modules, modules).
//
// C'est la SEULE fonction asynchrone de l'app : un navigateur ne peut lire un
// fichier du site qu'avec fetch(), qui est forcément asynchrone. Tout le reste
// du code est synchrone et ne dépend pas de ce fichier.

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
  try {
    return await reponse.json();
  } catch (e) {
    throw new Error(`Le fichier « ${url} » n'est pas un JSON valide : lance validate.py dessus.`);
  }
}
