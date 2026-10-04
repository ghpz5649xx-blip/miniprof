// Petites fonctions d'affichage partagées par tous les écrans.
//
// RÈGLE DE SÉCURITÉ : le texte d'un module n'est pas fiable (il vient d'un LLM).
// On ne construit JAMAIS la page avec innerHTML : chaque texte devient un nœud
// texte (createTextNode / textContent), que le navigateur n'interprète pas.
// Un "<script>" dans un module s'affiche donc tel quel, sans s'exécuter.

// Crée un élément HTML.
//   el("button", { class: "btn", onclick: maFonction }, "Texte", autreElement)
// - attrs : attributs ; ceux qui commencent par "on" sont des événements ;
//   une valeur false / null / undefined est ignorée (pratique pour "disabled").
// - enfants : textes (convertis en nœuds texte) ou éléments ; null est ignoré.
export function el(tag, attrs, ...enfants) {
  const node = document.createElement(tag);
  for (const [nom, valeur] of Object.entries(attrs || {})) {
    if (valeur === false || valeur === null || valeur === undefined) continue;
    if (nom.startsWith("on")) {
      node.addEventListener(nom.slice(2), valeur);
    } else if (valeur === true) {
      node.setAttribute(nom, "");
    } else {
      node.setAttribute(nom, valeur);
    }
  }
  for (const enfant of enfants) {
    if (enfant === null || enfant === undefined || enfant === false) continue;
    node.append(typeof enfant === "string" ? document.createTextNode(enfant) : enfant);
  }
  return node;
}

// Transforme un texte de module en contenu affichable, avec la seule mise en
// forme autorisée : **gras** et retours à la ligne (\n).
// Renvoie un fragment à insérer dans un élément : el("p", {}, richText(t)).
export function richText(texte) {
  const fragment = document.createDocumentFragment();
  const lignes = String(texte).split("\n");
  lignes.forEach((ligne, i) => {
    if (i > 0) fragment.append(document.createElement("br"));
    // split avec une parenthèse capturante : les morceaux impairs sont ceux
    // qui étaient entre ** et **.
    const morceaux = ligne.split(/\*\*(.+?)\*\*/);
    morceaux.forEach((morceau, j) => {
      if (morceau === "") return;
      if (j % 2 === 1) {
        const gras = document.createElement("strong");
        gras.textContent = morceau;
        fragment.append(gras);
      } else {
        fragment.append(document.createTextNode(morceau));
      }
    });
  });
  return fragment;
}

// Vide la zone principale de l'app et la renvoie, prête à recevoir un écran.
export function clear() {
  const app = document.getElementById("app");
  app.replaceChildren();
  window.scrollTo(0, 0);
  return app;
}

// Barre du haut d'un écran : bouton « ← Retour » (lien vers `retour`, une
// adresse du type "#/biblio"), titre, et éventuellement un élément à droite.
export function topBar(titre, retour, aDroite) {
  return el("header", { class: "topbar" },
    retour ? el("a", { class: "btn btn-back", href: retour }, "← Retour") : null,
    el("h1", { class: "topbar-title" }, titre),
    aDroite || null,
  );
}

// Encadré coloré : type = "ok" (vert), "error" (rouge), "info" (bleu), "hint" (orange).
// role="alert" fait lire le message par les lecteurs d'écran.
export function message(type, texte) {
  return el("div", { class: "msg msg-" + type, role: "alert" }, richText(texte));
}

// Puce de choix (niveau, compétence…) : la puce choisie a aria-pressed="true",
// ce qui la surligne (css/style.css) et l'annonce aux lecteurs d'écran.
// `cle` sert à retrouver le bouton pour lui rendre le focus après un réaffichage.
// Utilisée par les réglages de l'entraînement et de l'évaluation.
export function chip(cle, choisi, titre, texte, auClic) {
  return el("button", {
    type: "button",
    class: "btn chip",
    "aria-pressed": String(choisi),
    "data-cle": cle,
    onclick: auClic,
  },
    el("span", { class: "chip-title" }, titre),
    texte ? el("span", { class: "chip-text" }, texte) : null,
  );
}
