// Contrôle DÉFENSIF d'un module au moment de son ouverture.
//
// La validation complète de référence est tools/validate.py (à lancer avant de
// publier). Ici, on vérifie seulement ce qui ferait planter l'app : structure
// et types de base. Recouvrement avec validate.py, volontairement minimal :
//   - REQUIRED          ≡ "required" à la racine de schema/module.schema.json
//   - REQUIRED_QUESTION ≡ "required" de $defs.question dans le schéma
//   - TYPES_CONNUS      ≡ types de question du schéma
//   - BLOCS_CONNUS      ≡ types de bloc de leçon du schéma
// Ces listes sont comparées au schéma par tools/tests/test_sync.py :
// si on modifie le schéma sans les mettre à jour, le test échoue.

const REQUIRED = ["schema_version", "id", "version", "title", "subject", "level", "description", "skills", "lesson", "questions"];
const REQUIRED_QUESTION = ["id", "skill", "difficulty", "type", "prompt", "hint", "explanation"];

const SCHEMA_VERSION = 1;
const TYPES_CONNUS = ["number", "choice", "text"];
const BLOCS_CONNUS = ["text", "worked_example", "guided_steps"];

// Renvoie { ok, module, errors, warnings }.
// - ok = false : le module est inutilisable, `errors` dit pourquoi ;
// - ok = true  : `module` est utilisable ; les questions et les blocs de leçon
//   mal formés ont été retirés (et comptés dans `warnings`) au lieu de faire
//   planter l'écran. La leçon peut donc être vide : l'écran Apprendre le dit.
export function checkModule(data) {
  const errors = [];
  const warnings = [];

  if (data === null || typeof data !== "object" || Array.isArray(data)) {
    return { ok: false, module: null, errors: ["Le fichier n'est pas un module."], warnings };
  }
  for (const champ of REQUIRED) {
    if (!(champ in data)) errors.push(`Champ obligatoire manquant : « ${champ} ».`);
  }
  if (errors.length > 0) return { ok: false, module: null, errors, warnings };

  // Un module écrit pour un format plus récent : on refuse proprement (risque R8).
  if (data.schema_version !== SCHEMA_VERSION) {
    errors.push(`Format de module inconnu (schema_version ${data.schema_version}) : mets l'app à jour.`);
  }
  for (const champ of ["skills", "lesson", "questions"]) {
    if (!Array.isArray(data[champ]) || data[champ].length === 0) {
      errors.push(`« ${champ} » doit être une liste non vide.`);
    }
  }
  for (const champ of ["id", "title", "description"]) {
    if (typeof data[champ] !== "string") errors.push(`« ${champ} » doit être un texte.`);
  }
  if (errors.length > 0) return { ok: false, module: null, errors, warnings };

  // Questions : on garde les bonnes, on écarte les autres.
  const questions = data.questions.filter(questionUtilisable);
  const ecartees = data.questions.length - questions.length;
  if (ecartees > 0) {
    warnings.push(`${ecartees} question(s) mal formée(s) ignorée(s) : lance validate.py sur ce module.`);
  }
  if (questions.length === 0) {
    errors.push("Aucune question utilisable dans ce module.");
    return { ok: false, module: null, errors, warnings };
  }

  // Leçon : même principe, mais une leçon abîmée n'empêche pas de s'entraîner.
  const lesson = data.lesson.filter(blocUtilisable);
  const blocsEcartes = data.lesson.length - lesson.length;
  if (blocsEcartes > 0) {
    warnings.push(`${blocsEcartes} bloc(s) de leçon mal formé(s) ignoré(s) : lance validate.py sur ce module.`);
  }

  // Copie du module avec seulement les questions et blocs utilisables.
  const module = Object.assign({}, data, { questions: questions, lesson: lesson });
  return { ok: true, module, errors, warnings };
}

// Vrai si la question a ce qu'il faut pour être affichée sans planter.
function questionUtilisable(q) {
  if (q === null || typeof q !== "object") return false;
  for (const champ of REQUIRED_QUESTION) {
    if (!(champ in q)) return false;
  }
  if (typeof q.prompt !== "string" || !TYPES_CONNUS.includes(q.type)) return false;
  if (q.type === "number") return Array.isArray(q.fields) && q.fields.length > 0;
  if (q.type === "choice") return Array.isArray(q.choices) && q.choices.length >= 2 && "answer" in q;
  if (q.type === "text") return Array.isArray(q.accepted) && q.accepted.length > 0;
  return false;
}

// Vrai si le bloc de leçon a ce qu'il faut pour être affiché sans planter.
function blocUtilisable(b) {
  if (b === null || typeof b !== "object") return false;
  if (typeof b.title !== "string" || !BLOCS_CONNUS.includes(b.type)) return false;
  if (b.type === "text") return typeof b.body === "string";
  if (!Array.isArray(b.steps) || b.steps.length === 0) return false;
  if (b.type === "worked_example") {
    return b.steps.every((e) => e !== null && typeof e === "object" && typeof e.thought === "string");
  }
  // guided_steps : la réponse doit être un nombre ou un texte, sinon on ne
  // pourrait pas la comparer à la saisie.
  return b.steps.every((e) => e !== null && typeof e === "object" && typeof e.prompt === "string"
    && (typeof e.answer === "number" || typeof e.answer === "string"));
}
