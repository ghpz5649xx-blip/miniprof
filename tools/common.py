"""Fonctions partagées par les outils miniprof.

- lecture d'un fichier de module, même quand le LLM a entouré le JSON de texte ;
- détection des clés en double (que json.loads ignore silencieusement) ;
- validation contre le schéma, avec des messages en français ;
- normalisation des réponses texte (même règle que l'app, voir js/answers.js).
"""

import json
import re
import unicodedata
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "module.schema.json"


class ModuleIllisible(Exception):
    """Le fichier ne contient pas de JSON exploitable."""


# ---------------------------------------------------------------------------
# Lecture du fichier
# ---------------------------------------------------------------------------

def load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def extract_json(text):
    """Renvoie (texte_json, extrait).

    `extrait` vaut True si on a dû retirer du texte autour du JSON
    (phrase d'introduction du LLM, balises ```json ... ```).
    """
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped, False

    # Cas 1 : bloc de code Markdown ```json ... ``` (ou ``` sans langage)
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n\s*```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip(), True

    # Cas 2 : du texte avant/après -> on garde de la première { à la dernière }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start:end + 1], True

    raise ModuleIllisible("aucun objet JSON trouvé (pas d'accolade { … }).")


def _refuse_duplicate_keys(pairs):
    """Hook de json.loads : une clé présente deux fois est une erreur.

    Sans ce contrôle, Python garderait la dernière valeur sans rien dire,
    et une question pourrait perdre sa vraie réponse.
    """
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ModuleIllisible(f"la clé « {key} » apparaît deux fois dans le même objet.")
        obj[key] = value
    return obj


def parse_json(json_text):
    try:
        return json.loads(json_text, object_pairs_hook=_refuse_duplicate_keys)
    except json.JSONDecodeError as e:
        raise ModuleIllisible(
            f"JSON mal formé ligne {e.lineno}, colonne {e.colno} : {_fr_json_error(e.msg)}."
        ) from None


def _fr_json_error(msg):
    traductions = {
        "Expecting ',' delimiter": "il manque une virgule",
        "Expecting ':' delimiter": "il manque deux-points « : »",
        "Expecting value": "valeur attendue (virgule en trop ou guillemet manquant ?)",
        "Expecting property name enclosed in double quotes":
            "nom de champ attendu entre guillemets droits \" (virgule en trop avant } ?)",
        "Unterminated string starting at": "texte non fermé (guillemet manquant)",
        "Invalid control character at": "retour à la ligne dans un texte (écrire \\n)",
        "Illegal trailing comma": "virgule en trop avant } ou ]",
        "Extra data": "contenu en trop après la fin du JSON",
        "Invalid \\escape": "barre oblique inverse \\ invalide",
    }
    for en, fr in traductions.items():
        if msg.startswith(en):
            return fr
    return msg


def read_module(path):
    """Lit un fichier de module. Renvoie (data, extrait)."""
    text = Path(path).read_text(encoding="utf-8")
    json_text, extracted = extract_json(text)
    return parse_json(json_text), extracted


# ---------------------------------------------------------------------------
# Chemins lisibles : questions[3].fields[0].answer (question q004)
# ---------------------------------------------------------------------------

def format_path(path, data):
    parts = list(path)
    if not parts:
        return "(racine)"
    text = ""
    for p in parts:
        text += f"[{p}]" if isinstance(p, int) else (f".{p}" if text else p)
    # On ajoute l'id de la question ou de la compétence : plus facile à retrouver.
    if len(parts) >= 2 and parts[0] in ("questions", "skills") and isinstance(parts[1], int):
        try:
            ident = data[parts[0]][parts[1]].get("id")
            if ident:
                label = "question" if parts[0] == "questions" else "compétence"
                text += f" ({label} {ident})"
        except (IndexError, AttributeError, KeyError, TypeError):
            pass
    return text


# ---------------------------------------------------------------------------
# Validation par le schéma, messages en français
# ---------------------------------------------------------------------------

TYPES_FR = {
    "string": "un texte", "number": "un nombre", "integer": "un nombre entier",
    "array": "une liste [ … ]", "object": "un objet { … }", "boolean": "vrai/faux",
    "null": "null",
}

MOTIFS_FR = {
    "^[a-z0-9]+(-[a-z0-9]+)*$": "minuscules sans accents, chiffres, mots séparés par des tirets",
    "^[a-z0-9_-]+$": "minuscules sans accents, chiffres, - ou _",
}


def _type_fr(value):
    if isinstance(value, bool):
        return "vrai/faux"
    if isinstance(value, int) or isinstance(value, float):
        return "un nombre"
    if isinstance(value, str):
        return "un texte"
    if isinstance(value, list):
        return "une liste"
    if isinstance(value, dict):
        return "un objet"
    return "null"


def _court(value):
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 40 else text[:37] + "…"


def _resolve(data, path):
    obj = data
    for p in path:
        obj = obj[p]
    return obj


def _message_fr(error, data):
    """Traduit une erreur jsonschema. Renvoie (chemin, message)."""
    v = error.validator
    path = list(error.absolute_path)
    inst = error.instance

    if v == "required":
        missing = [k for k in error.validator_value if k not in inst]
        return path, "champ obligatoire manquant : " + ", ".join(f"« {k} »" for k in missing)
    if v == "additionalProperties":
        allowed = error.schema.get("properties", {})
        extras = [k for k in inst if k not in allowed]
        return path, "champ inconnu : " + ", ".join(f"« {k} »" for k in extras) + " (non prévu par le format)"
    if v is None:
        # Schéma « false » : champ interdit pour ce type de bloc / question.
        # jsonschema ne donne pas le nom du champ : on le retrouve dans l'objet parent.
        parent = _resolve(data, path)
        names = [k for k, val in parent.items() if val is inst] if isinstance(parent, dict) else []
        what = parent.get("type", "?") if isinstance(parent, dict) else "?"
        name = names[0] if names else "?"
        return path, f"champ « {name} » non prévu pour le type « {what} »"
    if v == "type":
        expected = error.validator_value
        expected = [expected] if isinstance(expected, str) else expected
        return path, (f"doit être {' ou '.join(TYPES_FR.get(t, t) for t in expected)}"
                      f" (reçu : {_type_fr(inst)} {_court(inst)})")
    if v == "enum":
        options = ", ".join(str(o) for o in error.validator_value)
        return path, f"valeur non autorisée {_court(inst)} ; valeurs possibles : {options}"
    if v == "const":
        return path, f"doit valoir {_court(error.validator_value)} (reçu : {_court(inst)})"
    if v == "minLength":
        return path, "texte vide"
    if v == "pattern":
        attendu = MOTIFS_FR.get(error.validator_value, error.validator_value)
        return path, f"format invalide {_court(inst)} (attendu : {attendu})"
    if v == "minItems":
        return path, f"la liste doit contenir au moins {error.validator_value} élément(s) (reçu : {len(inst)})"
    if v == "maxItems":
        return path, f"la liste doit contenir au plus {error.validator_value} élément(s) (reçu : {len(inst)})"
    if v == "minProperties":
        return path, "objet vide"
    if v == "minimum":
        return path, f"doit être supérieur ou égal à {error.validator_value} (reçu : {_court(inst)})"
    if v == "maximum":
        return path, f"doit être inférieur ou égal à {error.validator_value} (reçu : {_court(inst)})"
    if v == "anyOf":
        return path, f"doit être un nombre ou un texte non vide (reçu : {_court(inst)})"
    return path, error.message


def schema_errors(data, schema=None):
    """Liste des erreurs de schéma, en français, triées par chemin."""
    validator = jsonschema.Draft202012Validator(schema or load_schema())
    messages = []
    for error in validator.iter_errors(data):
        path, msg = _message_fr(error, data)
        messages.append((path, f"{format_path(path, data)} : {msg}"))
    messages.sort(key=lambda m: [str(p).zfill(6) for p in m[0]])
    # Une même erreur peut remonter deux fois (via allOf) : on dédoublonne.
    seen, result = set(), []
    for _, msg in messages:
        if msg not in seen:
            seen.add(msg)
            result.append(msg)
    return result


# ---------------------------------------------------------------------------
# Normalisation des réponses texte
# ---------------------------------------------------------------------------

def normalize_text(s):
    """Règle de comparaison tolérante. DOIT rester identique à normalizeText() de js/answers.js.

    minuscules, sans accents, apostrophes unifiées, espaces multiples réduits,
    ponctuation finale (. ! ? ; : ,) ignorée.
    """
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower().replace("’", "'").replace(" ", " ").replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[.!?;:,\s]+$", "", s)
    return s
