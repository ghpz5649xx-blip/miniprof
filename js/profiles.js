// Profils enfants : un prénom, sans mot de passe.
//
// Stockage :
//   miniprof.v1.profiles = [{ "id": "p1a2b3c", "name": "Léa" }, ...]
//   miniprof.v1.current  = "p1a2b3c"   (profil choisi en dernier sur cet appareil)
// L'id ne change jamais (on pourra renommer sans perdre l'historique, qui
// sera rattaché à l'id à l'étape 6).

import { readKey, writeKey } from "./storage.js";

export const MAX_NAME = 20;

export function listProfiles() {
  const profils = readKey("profiles", []);
  // Défensif : si le stockage a été abîmé, on repart d'une liste vide.
  return Array.isArray(profils) ? profils : [];
}

export function getProfile(id) {
  return listProfiles().find((p) => p.id === id) || null;
}

// Profil courant, ou null s'il n'existe plus (supprimé entre-temps).
export function currentProfile() {
  return getProfile(readKey("current", null));
}

export function setCurrent(id) {
  return writeKey("current", id);
}

// Crée un profil. Renvoie { ok: true, profile } ou { ok: false, error: "message" }.
export function createProfile(nomSaisi) {
  // Espaces en trop retirés : « Léa  » et « Léa » sont le même prénom.
  const name = String(nomSaisi).replace(/\s+/g, " ").trim();
  if (name === "") {
    return { ok: false, error: "Écris un prénom." };
  }
  if (name.length > MAX_NAME) {
    return { ok: false, error: `Le prénom doit faire au plus ${MAX_NAME} caractères.` };
  }
  const profils = listProfiles();
  const existe = profils.some((p) => p.name.toLowerCase() === name.toLowerCase());
  if (existe) {
    return { ok: false, error: `Le profil « ${name} » existe déjà.` };
  }
  // Id = "p" + date en base 36 : court, unique sur un appareil, jamais réutilisé.
  const profile = { id: "p" + Date.now().toString(36), name: name };
  profils.push(profile);
  if (!writeKey("profiles", profils)) {
    return { ok: false, error: "Impossible d'enregistrer le profil sur cet appareil." };
  }
  return { ok: true, profile: profile };
}

// Supprime un profil (pour l'instant : seulement la ligne du profil ; à
// l'étape 6, il faudra aussi supprimer ses événements).
export function deleteProfile(id) {
  const profils = listProfiles().filter((p) => p.id !== id);
  return writeKey("profiles", profils);
}
