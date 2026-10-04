// Sauvegarde et restauration de toutes les données de l'appareil (risque R1 :
// perte des données locales), et rappel de sauvegarde (risques R1 et R4).
//
// Ce fichier ne fait aucun affichage : l'écran est dans screens/backup.js.
//
// Format du fichier exporté (lu aussi par tools/analyse.py) :
//   {
//     "format": "miniprof-sauvegarde", "version": 1,
//     "exported_at": 1791000000,                 (secondes depuis 1970)
//     "profiles": [{ "id": "p…", "name": "Léa" }, ...],
//     "events": { "p…": [ligne, ligne, ...], ... }, (lignes compactes de js/events.js)
//     "flags": [[module, question, date, profil], ...]  (voir js/flags.js)
//   }
// Les lignes sont copiées telles quelles : pas de conversion, donc rien à
// garder synchronisé à part l'ordre des colonnes, documenté dans events.js.

import { readKey, writeKey, removeKey, usedChars } from "./storage.js";
import { listProfiles } from "./profiles.js";
import { rawLines, replaceLines, maintenant } from "./events.js";
import { allFlags, replaceFlags } from "./flags.js";

const FORMAT = "miniprof-sauvegarde";
const VERSION = 1;

// Rappel (docs/besoins.md, C3).
const QUOTA_CARACTERES = 5000000;  // ≈ 5 Mo par site : la limite la plus basse des navigateurs
const SEUIL_QUOTA = 0.7;
const JOURS_SANS_EXPORT = 14;
const UN_JOUR = 24 * 3600;         // en secondes

// Toutes les données de l'appareil, en un objet prêt à écrire dans un fichier.
export function buildBackup() {
  const profils = listProfiles();
  const evenements = {};
  for (const p of profils) evenements[p.id] = rawLines(p.id);
  return {
    format: FORMAT,
    version: VERSION,
    exported_at: maintenant(),
    profiles: profils,
    events: evenements,
    flags: allFlags(),
  };
}

// Fait télécharger la sauvegarde par le navigateur, puis note la date.
// Synchrone : on fabrique un fichier en mémoire (Blob) et on « clique » un
// lien de téléchargement vers lui.
export function downloadBackup() {
  const data = buildBackup();
  const texte = JSON.stringify(data);
  const blob = new Blob([texte], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const lien = document.createElement("a");
  lien.href = url;
  // ".export.json" : ignoré par Git (.gitignore), ce sont des données personnelles.
  lien.download = "miniprof-" + new Date().toISOString().slice(0, 10) + ".export.json";
  document.body.append(lien);
  lien.click();
  lien.remove();
  // On ne libère pas l'adresse du Blob (URL.revokeObjectURL) : la libérer
  // tout de suite fait échouer le téléchargement sur certains navigateurs, et
  // attendre demanderait un minuteur. Elle disparaît à la fermeture de la page.
  return writeKey("last_export", data.exported_at);
}

// Date (s) du dernier export, ou null.
export function lastExport() {
  const date = readKey("last_export", null);
  return typeof date === "number" ? date : null;
}

// Part du stockage utilisée, de 0 à 1 (estimation).
export function storageRatio() {
  return usedChars() / QUOTA_CARACTERES;
}

// Contrôle un fichier de sauvegarde avant de remplacer quoi que ce soit.
// Renvoie { ok: true, resume: "texte" } ou { ok: false, errors: ["…"] }.
export function checkBackup(data) {
  const errors = [];
  if (data === null || typeof data !== "object" || data.format !== FORMAT) {
    return { ok: false, errors: ["Ce fichier n'est pas une sauvegarde miniprof."] };
  }
  if (data.version !== VERSION) {
    return { ok: false, errors: [`Version de sauvegarde inconnue (${data.version}) : mets l'app à jour.`] };
  }
  const profils = data.profiles;
  if (!Array.isArray(profils) || !profils.every((p) => p !== null && typeof p === "object"
    && typeof p.id === "string" && p.id !== "" && typeof p.name === "string" && p.name !== "")) {
    errors.push("La liste des profils est abîmée.");
  }
  if (data.events === null || typeof data.events !== "object" || Array.isArray(data.events)
    || !Object.values(data.events).every(Array.isArray)) {
    errors.push("Les résultats sont abîmés.");
  }
  if (!Array.isArray(data.flags)) {
    errors.push("La liste des questions signalées est abîmée.");
  }
  if (errors.length > 0) return { ok: false, errors };

  // Résumé affiché avant confirmation : le parent vérifie que c'est le bon fichier.
  const lignes = [];
  if (typeof data.exported_at === "number") {
    lignes.push("Sauvegarde du " + new Date(data.exported_at * 1000).toLocaleString("fr-FR"));
  }
  if (profils.length === 0) lignes.push("Aucun profil.");
  for (const p of profils) {
    const n = Array.isArray(data.events[p.id]) ? data.events[p.id].length : 0;
    lignes.push(p.name + " : " + n + " réponse(s)");
  }
  lignes.push(data.flags.length + " question(s) signalée(s)");
  return { ok: true, resume: lignes.join("\n") };
}

// Remplace toutes les données de l'appareil par celles de la sauvegarde
// (déjà contrôlée par checkBackup). Renvoie true si tout est écrit.
export function restoreBackup(data) {
  // 1. Effacer les résultats des profils actuels (ils seraient orphelins).
  for (const p of listProfiles()) removeKey("events." + p.id);
  // 2. Écrire le contenu de la sauvegarde.
  let ok = writeKey("profiles", data.profiles);
  for (const p of data.profiles) {
    const lignes = Array.isArray(data.events[p.id]) ? data.events[p.id] : [];
    ok = replaceLines(p.id, lignes) && ok;
  }
  ok = replaceFlags(data.flags) && ok;
  // Ces données existent déjà dans un fichier : le rappel repart de sa date.
  if (typeof data.exported_at === "number") ok = writeKey("last_export", data.exported_at) && ok;
  // 3. Le profil choisi n'existe peut-être plus : on repassera par le choix.
  const courant = readKey("current", null);
  if (!data.profiles.some((p) => p.id === courant)) removeKey("current");
  return ok;
}

// Texte du rappel de sauvegarde, ou null s'il n'y a rien à rappeler.
export function backupReminder() {
  if (storageRatio() > SEUIL_QUOTA) {
    return "Le stockage de cet appareil est presque plein : exporte tes données.";
  }
  // Rien à perdre tant qu'aucune réponse n'est enregistrée.
  const reponses = listProfiles().some((p) => rawLines(p.id).length > 0);
  if (!reponses) return null;
  const derniere = lastExport();
  if (derniere === null) {
    return "Tes résultats n'ont jamais été sauvegardés : pense à les exporter.";
  }
  const jours = Math.floor((maintenant() - derniere) / UN_JOUR);
  if (jours >= JOURS_SANS_EXPORT) {
    return "Pas de sauvegarde depuis " + jours + " jours : pense à exporter tes résultats.";
  }
  return null;
}
