// Dernière activité sur l'appareil : sert à redemander « Qui utilise miniprof ? » (plan P008).
//
// Pourquoi : un même téléphone passe d'un enfant à l'autre. Sans limite de temps, les résultats
// du second arrivaient dans le profil du premier. Règle : après 30 minutes sans utilisation, le
// profil courant n'est plus considéré comme choisi (voir profilActif() dans js/profiles.js).
//
// Stockage : miniprof.v1.derniere_activite = date en secondes (même format que les événements).
// Un appareil qui n'a pas cette clé (avant P008) redemande le profil une fois, puis tout roule.
// La clé n'est pas exportée : elle ne décrit que l'appareil, pas les résultats.

import { readKey, writeKey } from "./storage.js";
import { maintenant } from "./events.js";

export const DELAI = 30 * 60; // secondes
const PAS = 10; // on n'écrit pas plus d'une fois toutes les 10 s : le stockage reste tranquille

// Adresse de l'app, calculée depuis ce fichier (js/ est à la racine du site).
export const RACINE = new URL("../", import.meta.url).href;

export function toucher(force) {
  const derniere = readKey("derniere_activite", null);
  const maintenantS = maintenant();
  if (!force && typeof derniere === "number" && maintenantS - derniere < PAS) return true;
  return writeKey("derniere_activite", maintenantS);
}

export function activiteRecente() {
  const derniere = readKey("derniere_activite", null);
  return typeof derniere === "number" && maintenant() - derniere < DELAI;
}

// Adresse de retour acceptée : un écran de l'app ("#/module/…") ou une page de module
// ("modules/<id>.html"). Rien d'autre : le paramètre vient de l'adresse, donc d'un lien qu'on
// ne maîtrise pas (pas de redirection vers un autre site).
export function retourValide(retour) {
  return typeof retour === "string"
    && (/^#\/[A-Za-z0-9_\-\/%.]*$/.test(retour) || /^modules\/[A-Za-z0-9_-]+\.html$/.test(retour));
}

// Adresse de « Qui utilise miniprof ? » qui ramène ensuite à `retour`.
export function adresseChoix(retour) {
  return RACINE + "#/" + (retourValide(retour) ? "?retour=" + encodeURIComponent(retour) : "");
}

// Adresse demandée dans l'adresse courante de l'app (#/?retour=…), ou null.
export function retourDemande() {
  const requete = location.hash.split("?")[1];
  if (!requete) return null;
  const retour = new URLSearchParams(requete).get("retour");
  return retourValide(retour) ? retour : null;
}

// Va à l'adresse de retour demandée, ou à `defaut` (un hash de l'app).
export function revenir(defaut) {
  const retour = retourDemande();
  if (retour === null) location.hash = defaut;
  else if (retour.startsWith("#/")) location.hash = retour;
  else location.href = RACINE + retour;
}

// Surveille l'écran : tant que quelqu'un touche la page dans les 30 minutes, l'activité est
// notée. Si la page est restée ouverte plus longtemps, le toucher suivant est intercepté AVANT
// que la page le voie (capture + stopImmediatePropagation) : aucune réponse n'est enregistrée,
// on envoie vers le choix du profil. Une question perdue plutôt qu'un résultat chez la
// mauvaise personne. `exempte()` : écrans qui n'ont pas besoin de profil. `rediriger()` : où aller.
export function garderSession(exempte, rediriger) {
  for (const type of ["pointerdown", "click", "keydown"]) {
    document.addEventListener(type, (evenement) => {
      if (exempte()) return;
      if (activiteRecente()) {
        toucher(false);
        return;
      }
      evenement.preventDefault();
      evenement.stopImmediatePropagation();
      rediriger();
    }, true);
  }
}
