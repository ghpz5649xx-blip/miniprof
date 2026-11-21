// Affichage d'une fiche Markdown dans l'écran d'admin (plan P014).
// Pourquoi un petit lecteur maison : pas de bibliothèque ni de requête vers un tiers, et chaque
// morceau est construit nœud par nœud (jamais d'innerHTML), comme dans l'app.
// Couvre ce que les fiches utilisent : titres, paragraphes, gras, italique, code, liens, images
// du dépôt, listes (imbriquées, sur plusieurs lignes), tableaux, citations, blocs de code, filets.

function el(balise, texte) {
  const e = document.createElement(balise);
  if (texte !== undefined) e.textContent = texte;
  return e;
}

// --- Dans une ligne : gras, italique, code, liens, images ------------------------------------

// Une seule expression, essayée de gauche à droite ; à position égale, la première alternative
// gagne (le gras passe avant l'italique). Les « _ » collés à un mot (flag_notes) ne comptent pas.
const EN_LIGNE = new RegExp([
  /!\[([^\]]*)\]\(([^)\s]+)\)/.source,           // 1-2 image
  /\[([^\]]+)\]\(([^)\s]+)\)/.source,            // 3-4 lien
  /`([^`]+)`/.source,                            // 5 code
  /\*\*(.+?)\*\*/.source,                        // 6 gras
  /(?<![\w*])\*(?![\s*])(.+?)(?<!\s)\*(?!\w)/.source, // 7 italique *…*
  /(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)/.source,    // 8 italique _…_
].join("|"), "g");

// Les images sont des fichiers du dépôt, servis par tools/admin.py ; `dossier` est celui de la fiche.
function image(alt, src, dossier) {
  if (/^[a-z]+:/i.test(src)) {
    // Une image d'un autre site ferait une requête vers un tiers : on montre seulement son texte.
    return el("span", `[image externe non affichée : ${alt || src}]`);
  }
  const img = el("img");
  img.alt = alt;
  img.src = "/fichier/" + (src.startsWith("/") ? src.slice(1) : dossier + src);
  return img;
}

function lien(texte, cible, dossier) {
  if (!/^https?:\/\//i.test(cible)) {
    // Lien vers un fichier du dépôt : on l'affiche, sans le rendre cliquable.
    const span = el("span");
    enLigne(texte, span, dossier);
    span.append(" (", el("code", cible), ")");
    return span;
  }
  const a = el("a");
  a.href = cible;
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  enLigne(texte, a, dossier);
  return a;
}

function enLigne(texte, parent, dossier) {
  let position = 0;
  for (const m of texte.matchAll(EN_LIGNE)) {
    parent.append(texte.slice(position, m.index));
    position = m.index + m[0].length;
    if (m[1] !== undefined || m[2] !== undefined) parent.append(image(m[1], m[2], dossier));
    else if (m[3] !== undefined) parent.append(lien(m[3], m[4], dossier));
    else if (m[5] !== undefined) parent.append(el("code", m[5]));
    else {
      const e = el(m[6] !== undefined ? "strong" : "em");
      enLigne(m[6] ?? m[7] ?? m[8], e, dossier);
      parent.append(e);
    }
  }
  parent.append(texte.slice(position));
}

// --- Blocs ------------------------------------------------------------------------------------

const RE_TITRE = /^(#{1,6})\s+(.*)$/;
const RE_ELEMENT = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/;
const RE_FILET = /^\s*([-*_])(\s*\1){2,}\s*$/;
const RE_SEPARATEUR_TABLEAU = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;

function estTableau(lignes, i) {
  return lignes[i].trim().startsWith("|") && i + 1 < lignes.length && RE_SEPARATEUR_TABLEAU.test(lignes[i + 1]);
}

// Une ligne qui ouvre un autre bloc arrête un paragraphe ou un élément de liste.
function ouvreUnBloc(lignes, i) {
  const l = lignes[i];
  return RE_TITRE.test(l) || l.trimStart().startsWith("```") || l.startsWith(">")
    || RE_FILET.test(l) || estTableau(lignes, i);
}

function cellules(ligne) {
  // « \| » reste un trait dans la cellule.
  return ligne.trim().replace(/^\|/, "").replace(/\|$/, "")
    .split(/(?<!\\)\|/).map(c => c.trim().replace(/\\\|/g, "|"));
}

function tableau(lignes, i, dossier) {
  const table = el("table");
  const tr = el("tr");
  for (const c of cellules(lignes[i])) {
    const th = el("th");
    enLigne(c, th, dossier);
    tr.append(th);
  }
  table.append(el("thead"));
  table.firstChild.append(tr);
  const tbody = el("tbody");
  i += 2;
  while (i < lignes.length && lignes[i].trim().startsWith("|")) {
    const ligne = el("tr");
    for (const c of cellules(lignes[i])) {
      const td = el("td");
      enLigne(c, td, dossier);
      ligne.append(td);
    }
    tbody.append(ligne);
    i++;
  }
  table.append(tbody);
  // Un tableau large défile dans son cadre au lieu d'élargir la page.
  const cadre = el("div");
  cadre.className = "cadre-tableau";
  cadre.append(table);
  return [cadre, i];
}

// Une liste au retrait `retrait` ; un élément plus en retrait ouvre une sous-liste.
function liste(lignes, i, retrait, dossier) {
  const ordonnee = /\d/.test(RE_ELEMENT.exec(lignes[i])[2]);
  const ul = el(ordonnee ? "ol" : "ul");
  while (i < lignes.length) {
    const m = RE_ELEMENT.exec(lignes[i]);
    if (!m || m[1].length !== retrait || /\d/.test(m[2]) !== ordonnee) break;
    const li = el("li");
    let texte = m[3];
    i++;
    // Les lignes suivantes, sans marqueur de liste, continuent l'élément.
    while (i < lignes.length && lignes[i].trim() && !RE_ELEMENT.test(lignes[i]) && !ouvreUnBloc(lignes, i)) {
      texte += " " + lignes[i].trim();
      i++;
    }
    enLigne(texte, li, dossier);
    // Sous-liste : un élément plus en retrait, éventuellement après une ligne vide.
    let j = i;
    while (j < lignes.length && !lignes[j].trim()) j++;
    const suite = j < lignes.length ? RE_ELEMENT.exec(lignes[j]) : null;
    if (suite && suite[1].length > retrait) {
      const [sousListe, apres] = liste(lignes, j, suite[1].length, dossier);
      li.append(sousListe);
      i = apres;
    }
    ul.append(li);
    // Une ligne vide entre deux éléments du même niveau ne coupe pas la liste.
    j = i;
    while (j < lignes.length && !lignes[j].trim()) j++;
    const prochain = j < lignes.length ? RE_ELEMENT.exec(lignes[j]) : null;
    if (prochain && prochain[1].length === retrait) i = j;
  }
  return [ul, i];
}

function blocs(lignes, dossier) {
  const fragment = document.createDocumentFragment();
  let i = 0;
  while (i < lignes.length) {
    const ligne = lignes[i];
    if (!ligne.trim()) { i++; continue; }

    if (ligne.trimStart().startsWith("```")) {
      const code = [];
      i++;
      while (i < lignes.length && !lignes[i].trimStart().startsWith("```")) code.push(lignes[i++]);
      i++; // la ligne qui ferme le bloc
      const pre = el("pre");
      pre.append(el("code", code.join("\n")));
      fragment.append(pre);
      continue;
    }
    const titre = RE_TITRE.exec(ligne);
    if (titre) {
      const h = el("h" + titre[1].length);
      enLigne(titre[2], h, dossier);
      fragment.append(h);
      i++;
      continue;
    }
    if (RE_FILET.test(ligne) && !RE_ELEMENT.test(ligne)) {
      fragment.append(el("hr"));
      i++;
      continue;
    }
    if (ligne.startsWith(">")) {
      const cites = [];
      while (i < lignes.length && lignes[i].startsWith(">")) cites.push(lignes[i++].replace(/^>\s?/, ""));
      const bq = el("blockquote");
      bq.append(blocs(cites, dossier));
      fragment.append(bq);
      continue;
    }
    if (estTableau(lignes, i)) {
      const [t, apres] = tableau(lignes, i, dossier);
      fragment.append(t);
      i = apres;
      continue;
    }
    const element = RE_ELEMENT.exec(ligne);
    if (element) {
      const [l, apres] = liste(lignes, i, element[1].length, dossier);
      fragment.append(l);
      i = apres;
      continue;
    }
    // Paragraphe : jusqu'à une ligne vide ou un autre bloc.
    const texte = [ligne.trim()];
    i++;
    while (i < lignes.length && lignes[i].trim() && !RE_ELEMENT.test(lignes[i]) && !ouvreUnBloc(lignes, i)) {
      texte.push(lignes[i++].trim());
    }
    const p = el("p");
    enLigne(texte.join(" "), p, dossier);
    fragment.append(p);
  }
  return fragment;
}

// `dossier` : chemin de la fiche dans le dépôt (ex. « plans/ »), pour trouver ses images.
export function afficherMarkdown(texte, conteneur, dossier = "plans/") {
  conteneur.replaceChildren(blocs(texte.replace(/\r\n/g, "\n").split("\n"), dossier));
}
