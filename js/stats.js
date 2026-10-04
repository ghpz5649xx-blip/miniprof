// Calculs du bilan à partir du journal des tentatives (js/events.js).
//
// Rien n'est stocké : tout est recalculé à chaque affichage, ce qui reste
// rapide (quelques milliers d'événements au plus). Ce fichier ne fait que des
// calculs, aucun affichage : l'écran est dans screens/report.js.

// Seuils de « à travailler » (docs/besoins.md, C2).
const SEUIL_FAIBLE = 0.6;      // moins de 60 % de réussite
const BAISSE_POINTS = 15;      // ou une baisse de plus de 15 points...
const ESSAIS_RECENTS = 10;     // ...entre les 10 derniers essais...
const MIN_POUR_BAISSE = 5;     // ...et les précédents, s'il y en a au moins 5 de chaque côté

// Taux de réussite (0 à 1) d'une liste d'événements.
function taux(evenements) {
  return evenements.filter((e) => e.juste).length / evenements.length;
}

// « N questions traitées, dont M réussies du premier coup » : en entraînement,
// seul le premier essai est enregistré, donc juste = réussi du premier coup.
export function syntheseGlobale(evenements) {
  const reussies = evenements.filter((e) => e.juste).length;
  return {
    total: evenements.length,
    reussies: reussies,
    pourcent: evenements.length > 0 ? Math.round((reussies / evenements.length) * 100) : 0,
  };
}

// Une ligne par couple (module, compétence) travaillé, dans l'ordre du
// premier essai : { module, skill, justes, total, taux, aTravailler, niveau }.
// `niveau` : difficulté du dernier essai raté (sinon du dernier essai), pour
// que « Travailler ce point » reprenne là où c'était difficile.
// Les événements doivent être du plus ancien au plus récent (listEvents).
export function scoresParCompetence(evenements) {
  const groupes = []; // { module, skill, essais: [...] }
  for (const e of evenements) {
    let g = groupes.find((x) => x.module === e.module && x.skill === e.skill);
    if (!g) {
      g = { module: e.module, skill: e.skill, essais: [] };
      groupes.push(g);
    }
    g.essais.push(e);
  }

  return groupes.map((g) => {
    const recents = g.essais.slice(-ESSAIS_RECENTS);
    const avant = g.essais.slice(0, -ESSAIS_RECENTS);
    const enBaisse = recents.length >= MIN_POUR_BAISSE && avant.length >= MIN_POUR_BAISSE
      && (taux(avant) - taux(recents)) * 100 > BAISSE_POINTS;
    const t = taux(g.essais);
    const ratees = g.essais.filter((e) => !e.juste);
    const reference = ratees.length > 0 ? ratees[ratees.length - 1] : g.essais[g.essais.length - 1];
    return {
      module: g.module,
      skill: g.skill,
      justes: g.essais.filter((e) => e.juste).length,
      total: g.essais.length,
      taux: t,
      enBaisse: enBaisse,
      aTravailler: t < SEUIL_FAIBLE || enBaisse,
      niveau: reference.difficulty,
    };
  });
}

// Les `n` dernières évaluations, la plus récente d'abord :
// { module, date (s), niveau ("mixte" ou "1".."4"), note, total }.
// Une évaluation = les événements "v" qui ont la même clé d'évaluation.
export function dernieresEvaluations(evenements, n) {
  const evaluations = [];
  for (const e of evenements) {
    if (e.mode !== "v" || typeof e.evaluation !== "string") continue;
    let ev = evaluations.find((x) => x.cle === e.evaluation && x.module === e.module);
    if (!ev) {
      // Clé "<date de début>/<niveau>" (voir js/events.js).
      const [debut, niveau] = e.evaluation.split("/");
      ev = { cle: e.evaluation, module: e.module, date: Number(debut) || e.date, niveau: niveau || "?", note: 0, total: 0 };
      evaluations.push(ev);
    }
    ev.total = ev.total + 1;
    if (e.juste) ev.note = ev.note + 1;
  }
  return evaluations.slice(-n).reverse();
}
