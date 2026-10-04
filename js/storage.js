// Accès au stockage local du navigateur (localStorage).
//
// Pourquoi ce fichier : localStorage peut échouer (navigation privée, quota
// plein, stockage désactivé). On centralise les try/catch ici pour qu'une
// erreur ne fasse jamais planter un écran, et pour qu'un échec d'écriture soit
// signalé au lieu d'être silencieux (risque R4).
//
// Toutes les clés commencent par "miniprof.v1." : le "v1" permettra de changer
// le format plus tard sans confondre ancien et nouveau.

const PREFIXE = "miniprof.v1.";

// Lit une valeur JSON. Renvoie `defaut` si la clé est absente ou illisible.
export function readKey(cle, defaut) {
  try {
    const texte = localStorage.getItem(PREFIXE + cle);
    return texte === null ? defaut : JSON.parse(texte);
  } catch (e) {
    console.warn("Lecture impossible :", cle, e);
    return defaut;
  }
}

// Écrit une valeur JSON. Renvoie true si c'est enregistré, false sinon :
// l'appelant doit alors prévenir l'utilisateur.
export function writeKey(cle, valeur) {
  try {
    localStorage.setItem(PREFIXE + cle, JSON.stringify(valeur));
    return true;
  } catch (e) {
    console.warn("Écriture impossible :", cle, e);
    return false;
  }
}

export const MESSAGE_ECHEC_SAUVEGARDE =
  "Sauvegarde impossible sur cet appareil (stockage plein ou désactivé). " +
  "Exporte tes données pour ne rien perdre.";

// Supprime une clé (ex. les événements d'un profil supprimé).
export function removeKey(cle) {
  try {
    localStorage.removeItem(PREFIXE + cle);
    return true;
  } catch (e) {
    console.warn("Suppression impossible :", cle, e);
    return false;
  }
}
