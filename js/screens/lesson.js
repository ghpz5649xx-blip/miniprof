// Écran « Apprendre » : la leçon du module, un bloc à la fois.
//
// Adresses :
//   #/module/<id>/apprendre           toute la leçon
//   #/module/<id>/apprendre/<skill>   seulement les blocs d'une compétence
//                                     (pour « Revoir la méthode » depuis l'entraînement)
//
// Le numéro du bloc affiché n'est PAS dans l'adresse : passer au bloc suivant
// ne recharge pas le module. Recharger la page reprend la leçon au début.
//
// Trois types de blocs (voir "bloc" dans schema/module.schema.json) :
//   text           : une explication ;
//   worked_example : un exemple résolu, chaque étape avec son « pourquoi » ;
//   guided_steps   : des phrases à trous que l'enfant complète une par une.

import { el, clear, topBar, message, richText } from "../ui.js";
import { openModule } from "../open-module.js";
import { parseNumber, isCorrectSimple } from "../answers.js";

// Caractère qui marque l'emplacement de la réponse dans une phrase à trous.
const TROU = "▢";

export function showLesson(id, skill) {
  const app = clear();
  const accueilModule = "#/module/" + id;
  app.append(topBar("Apprendre", accueilModule));
  const zone = el("div", {});
  app.append(zone);

  openModule(id, zone, (module) => {
    let blocs = module.lesson;
    let sousTitre = null;
    if (skill) {
      const competence = module.skills.find((s) => s && s.id === skill);
      if (!competence) {
        zone.replaceChildren(pasDeLecon("Cette compétence n'existe pas dans ce module.", accueilModule));
        return;
      }
      blocs = blocs.filter((b) => b.skill === skill);
      sousTitre = "Revoir : " + competence.label;
    }
    if (blocs.length === 0) {
      zone.replaceChildren(pasDeLecon("Il n'y a pas de leçon pour cela dans ce module.", accueilModule));
      return;
    }

    // n = numéro du bloc affiché (0 pour le premier).
    let n = 0;
    function afficherBloc() {
      window.scrollTo(0, 0);
      if (n >= blocs.length) {
        zone.replaceChildren(finDeLecon(id));
        return;
      }
      const bloc = blocs[n];
      const suite = () => { n = n + 1; afficherBloc(); };
      // Enveloppé dans el() : contrairement à replaceChildren(), el() ignore
      // les enfants null (sinon le mot « null » s'afficherait).
      zone.replaceChildren(el("div", {},
        sousTitre ? el("p", { class: "muted" }, richText(sousTitre)) : null,
        el("p", { class: "step-count" }, "Étape " + (n + 1) + " sur " + blocs.length),
        el("h2", {}, richText(bloc.title)),
        contenuBloc(bloc, suite),
      ));
      // Focus sur le premier champ, sinon sur le bouton principal : Entrée
      // suffit pour avancer. Fait ici, car focus() n'a d'effet que sur un
      // élément déjà dans la page. preventScroll : on reste en haut du bloc.
      const cible = zone.querySelector("input, .btn-primary");
      if (cible) cible.focus({ preventScroll: true });
    }
    afficherBloc();
  });
}

function contenuBloc(bloc, suite) {
  if (bloc.type === "text") return blocTexte(bloc, suite);
  if (bloc.type === "worked_example") return blocExemple(bloc, suite);
  return blocMiniEtapes(bloc, suite);
}

// Bouton « Continuer » qui passe au bloc suivant.
function boutonContinuer(suite) {
  return el("div", { class: "actions" },
    el("button", { class: "btn btn-primary", onclick: suite }, "Continuer"));
}

// --- Bloc « text » ---------------------------------------------------------

function blocTexte(bloc, suite) {
  return el("div", {},
    el("div", { class: "card" }, el("p", {}, richText(bloc.body))),
    boutonContinuer(suite),
  );
}

// --- Bloc « worked_example » ----------------------------------------------
// Tout est affiché d'un coup : l'enfant lit le raisonnement à son rythme.

function blocExemple(bloc, suite) {
  const liste = el("ol", { class: "thoughts" });
  for (const etape of bloc.steps) {
    liste.append(
      el("li", { class: "card" },
        el("p", {}, richText(etape.thought)),
        etape.why ? el("p", { class: "why" }, "Pourquoi : ", richText(etape.why)) : null,
      ),
    );
  }
  return el("div", {},
    bloc.intro ? el("p", {}, richText(bloc.intro)) : null,
    liste,
    bloc.conclusion ? message("ok", bloc.conclusion) : null,
    boutonContinuer(suite),
  );
}

// --- Bloc « guided_steps » --------------------------------------------------
// Une phrase à trous à la fois. Juste : la phrase complétée rejoint la liste
// des étapes réussies et la suivante apparaît. Faux : l'indice s'affiche et
// l'enfant réessaie autant qu'il veut (c'est une leçon, pas une évaluation).

function blocMiniEtapes(bloc, suite) {
  const reussies = el("ol", { class: "done-list" });
  const etapeEnCours = el("div", {});
  const contenu = el("div", {},
    bloc.intro ? el("p", {}, richText(bloc.intro)) : null,
    reussies,
    etapeEnCours,
  );

  function afficherEtape(i) {
    if (i >= bloc.steps.length) {
      const continuer = boutonContinuer(suite);
      etapeEnCours.replaceChildren(el("div", {},
        bloc.conclusion ? message("ok", bloc.conclusion) : null,
        continuer,
      ));
      continuer.querySelector("button").focus();
      return;
    }

    const etape = bloc.steps[i];
    const attendNombre = typeof etape.answer === "number";
    const retour = el("div", {});
    const saisie = el("input", {
      type: "text",
      class: "gap-input",
      // Clavier numérique sur téléphone quand la réponse est un nombre.
      inputmode: attendNombre ? "decimal" : null,
      autocomplete: "off",
      "aria-label": "Ta réponse",
      onkeydown: (e) => {
        if (e.key === "Enter") { e.preventDefault(); valider(); }
      },
    });

    function valider() {
      const texte = saisie.value.trim();
      // Saisie vide ou pas un nombre : simple consigne, ce n'est pas une erreur.
      if (texte === "") {
        retour.replaceChildren(message("hint", "Écris ta réponse."));
        saisie.focus();
        return;
      }
      if (attendNombre && parseNumber(texte) === null) {
        retour.replaceChildren(message("hint", "Écris un nombre."));
        saisie.select();
        return;
      }
      if (isCorrectSimple(texte, etape.answer)) {
        // On garde ce que l'enfant a tapé (« 3,5 » plutôt que « 3.5 »).
        reussies.append(
          el("li", {}, phraseATrou(etape.prompt, el("strong", {}, texte)), " ✓"),
        );
        afficherEtape(i + 1);
        return;
      }
      retour.replaceChildren(message("hint", "Pas encore.\n" + (etape.hint || "")));
      saisie.select();
    }

    etapeEnCours.replaceChildren(
      el("p", { class: "gap-line" }, phraseATrou(etape.prompt, saisie)),
      el("div", { class: "actions" },
        el("button", { class: "btn btn-primary", onclick: valider }, "Valider")),
      retour,
    );
    // Sans effet pour la 1re étape (bloc pas encore dans la page) : c'est
    // afficherBloc() qui s'en charge.
    saisie.focus();
  }

  afficherEtape(0);
  return contenu;
}

// Phrase « 10 × 19 = ▢ » : le ▢ est remplacé par `noeud` (un champ de saisie,
// ou la réponse en gras). Sans ▢, le nœud est ajouté à la fin de la phrase.
// Seul le premier ▢ est remplacé.
function phraseATrou(prompt, noeud) {
  const texte = String(prompt);
  const position = texte.indexOf(TROU);
  const fragment = document.createDocumentFragment();
  if (position === -1) {
    fragment.append(richText(texte), " ", noeud);
  } else {
    fragment.append(
      richText(texte.slice(0, position)),
      noeud,
      richText(texte.slice(position + TROU.length)),
    );
  }
  return fragment;
}

// --- Fin de leçon et cas particuliers -------------------------------------

function finDeLecon(id) {
  return el("div", { class: "hero" },
    el("h2", {}, "Bravo, tu as fini la leçon !"),
    el("p", {}, "Maintenant, entraîne-toi pour bien retenir."),
    el("div", { class: "actions" },
      el("a", { class: "btn btn-primary", href: "#/module/" + id + "/entrainement" }, "Je m'entraîne"),
      el("a", { class: "btn btn-secondary", href: "#/module/" + id }, "Accueil du module"),
    ),
  );
}

function pasDeLecon(texte, accueilModule) {
  return el("div", {},
    message("info", texte),
    el("a", { class: "btn btn-primary", href: accueilModule }, "Accueil du module"),
  );
}
