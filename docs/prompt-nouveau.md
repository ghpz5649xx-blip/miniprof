Tu es un professeur des écoles et de collège. Je t'envoie des photos d'un cours, d'exercices
et de contrôles d'un enfant. Crée un module d'entraînement au format JSON décrit plus bas.

Le module contient :
1. Les métadonnées : "id" (matiere-niveau-sujet, ex. maths-cm2-division-euclidienne),
   "version": 1, titre, matière, classe, description en une ou deux phrases pour l'enfant.
2. "skills" : 2 à 6 compétences travaillées dans le cours.
3. "lesson" : la leçon « Apprendre », qui montre le CHEMINEMENT DE PENSÉE pas à pas. Pour
   chaque compétence : un "worked_example" (chaque étape = ce que je pense/fais + pourquoi),
   puis un "guided_steps" (phrases à trous que l'enfant complète une par une, avec ▢ à
   l'endroit de la réponse et un indice). Des blocs "text" pour les définitions et
   « À retenir ».
4. "questions" : un premier lot de 40 à 60 questions, ids q001, q002…,
   réparties sur toutes les compétences et les 4 niveaux de difficulté.

Règles pédagogiques :
- Utilise le vocabulaire de la classe indiquée, avec des phrases courtes ; tutoie l'enfant.
- N'invente aucun contenu absent des photos : reste sur les notions, méthodes et types
  d'exercices du cours. Note dans "source_note" ce qui était illisible ou incertain.
- Indice ("hint") : il guide (méthode, question à se poser, rappel) sans jamais donner la
  réponse.
- Explication ("explanation") : courte, pas à pas, avec le calcul ou le raisonnement complet.
- Difficulté progressive de 1 (application directe) à 4 (problème en plusieurs étapes ou
  piège classique), avec des questions à chaque niveau pour chaque compétence.
- Varie les énoncés : pas deux questions identiques à un nombre près sans raison.
- "common_errors" (facultatif mais précieux) : les erreurs fréquentes des élèves et un
  message qui explique l'erreur sans donner la réponse.
- Mise en forme autorisée : **gras** et \n (retour à la ligne). Jamais de HTML ni de
  Markdown d'une autre sorte. Symboles unicode permis : × ÷ − ² √ ≤ ≥.

Exactitude (obligatoire) :
- VÉRIFIE CHAQUE CALCUL avant de répondre : refais chaque opération, et pour une
  division euclidienne vérifie dividende = diviseur × quotient + reste avec reste < diviseur.
- Dans un QCM, une seule bonne réponse ; "answer" est l'id d'un des choix.
- Une erreur de "common_errors" ne doit jamais être égale à la bonne réponse.
- Nombres : "answer" d'une case est un nombre JSON (3.5, pas "3,5").

Format (obligatoire) :
- Réponds UNIQUEMENT avec le JSON, sans texte avant ou après, sans ```.
- Le JSON doit respecter exactement le schéma ci-dessous (pas de champ en plus).
- Les "id" sont stables : ne change jamais un id existant.

Schéma JSON à respecter :
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "miniprof/module.schema.json",
  "title": "Module miniprof",
  "description": "Un module = une leçon pas à pas + une banque de questions sur un chapitre. Tous les textes acceptent **gras** et les retours à la ligne (\\n). Aucun HTML.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "id",
    "version",
    "title",
    "subject",
    "level",
    "description",
    "skills",
    "lesson",
    "questions"
  ],
  "properties": {
    "schema_version": {
      "const": 1,
      "description": "Toujours 1."
    },
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
      "description": "Identifiant stable du module : matiere-niveau-sujet, minuscules sans accents, mots séparés par des tirets. Ex. maths-cm2-division-euclidienne."
    },
    "version": {
      "type": "integer",
      "minimum": 1,
      "description": "Numéro de version, augmenté à chaque correction."
    },
    "title": {
      "$ref": "#/$defs/texte",
      "description": "Titre court du chapitre."
    },
    "subject": {
      "enum": [
        "maths",
        "francais",
        "histoire-geo",
        "sciences",
        "anglais",
        "emc",
        "autre"
      ],
      "description": "Matière."
    },
    "level": {
      "enum": [
        "CP",
        "CE1",
        "CE2",
        "CM1",
        "CM2",
        "6e",
        "5e",
        "4e",
        "3e"
      ],
      "description": "Classe."
    },
    "description": {
      "$ref": "#/$defs/texte",
      "description": "Une ou deux phrases pour l'enfant : ce qu'il va apprendre."
    },
    "skills": {
      "type": "array",
      "minItems": 1,
      "description": "Compétences travaillées (2 à 6 conseillées).",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "id",
          "label"
        ],
        "properties": {
          "id": {
            "$ref": "#/$defs/identifiant",
            "description": "Identifiant stable de la compétence."
          },
          "label": {
            "$ref": "#/$defs/texte",
            "description": "Libellé court, à l'infinitif (ex. « Poser la division »)."
          }
        }
      }
    },
    "lesson": {
      "type": "array",
      "minItems": 1,
      "description": "Leçon « Apprendre », dans l'ordre d'affichage. Au moins un bloc par compétence.",
      "items": {
        "$ref": "#/$defs/bloc"
      }
    },
    "questions": {
      "type": "array",
      "minItems": 1,
      "description": "Banque de questions.",
      "items": {
        "$ref": "#/$defs/question"
      }
    },
    "source_note": {
      "type": "string",
      "description": "Facultatif : ce qui a été lu sur les photos, ce qui était illisible ou absent."
    }
  },
  "$defs": {
    "texte": {
      "type": "string",
      "minLength": 1
    },
    "identifiant": {
      "type": "string",
      "pattern": "^[a-z0-9_-]+$"
    },
    "reponse_simple": {
      "description": "Un nombre (ex. 43, 3.5, -2) ou un texte court.",
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string",
          "minLength": 1
        }
      ]
    },
    "bloc": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type",
        "skill",
        "title"
      ],
      "properties": {
        "type": {
          "enum": [
            "text",
            "worked_example",
            "guided_steps"
          ],
          "description": "text = explication ; worked_example = exemple résolu commenté ; guided_steps = mini-étapes que l'enfant complète."
        },
        "skill": {
          "$ref": "#/$defs/identifiant",
          "description": "Compétence concernée (id présent dans skills)."
        },
        "title": {
          "$ref": "#/$defs/texte"
        },
        "body": {
          "$ref": "#/$defs/texte",
          "description": "Texte de l'explication (bloc text)."
        },
        "intro": {
          "$ref": "#/$defs/texte",
          "description": "Mise en situation avant les étapes."
        },
        "conclusion": {
          "$ref": "#/$defs/texte",
          "description": "Ce qu'il faut retenir à la fin des étapes."
        },
        "steps": {
          "type": "array",
          "minItems": 1
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "type": {
                "const": "text"
              }
            },
            "required": [
              "type"
            ]
          },
          "then": {
            "required": [
              "body"
            ],
            "properties": {
              "intro": false,
              "conclusion": false,
              "steps": false
            }
          }
        },
        {
          "if": {
            "properties": {
              "type": {
                "const": "worked_example"
              }
            },
            "required": [
              "type"
            ]
          },
          "then": {
            "required": [
              "steps"
            ],
            "properties": {
              "body": false,
              "steps": {
                "description": "Le cheminement de pensée, étape par étape.",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "thought",
                    "why"
                  ],
                  "properties": {
                    "thought": {
                      "$ref": "#/$defs/texte",
                      "description": "Ce que je fais ou pense (« Je cherche le plus grand multiple de 8… »)."
                    },
                    "why": {
                      "$ref": "#/$defs/texte",
                      "description": "Pourquoi je le fais."
                    }
                  }
                }
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "type": {
                "const": "guided_steps"
              }
            },
            "required": [
              "type"
            ]
          },
          "then": {
            "required": [
              "steps"
            ],
            "properties": {
              "body": false,
              "steps": {
                "description": "Phrases à trous complétées une par une par l'enfant.",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "prompt",
                    "answer",
                    "hint"
                  ],
                  "properties": {
                    "prompt": {
                      "$ref": "#/$defs/texte",
                      "description": "Phrase avec ▢ à l'endroit de la réponse (ex. « 10 × 19 = ▢ »)."
                    },
                    "answer": {
                      "$ref": "#/$defs/reponse_simple"
                    },
                    "hint": {
                      "$ref": "#/$defs/texte",
                      "description": "Aide affichée si la réponse est fausse."
                    }
                  }
                }
              }
            }
          }
        }
      ]
    },
    "question": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id",
        "skill",
        "difficulty",
        "type",
        "prompt",
        "hint",
        "explanation"
      ],
      "properties": {
        "id": {
          "$ref": "#/$defs/identifiant",
          "description": "Identifiant stable et unique dans le module (q001, q002…). Ne jamais le changer lors d'une correction."
        },
        "skill": {
          "$ref": "#/$defs/identifiant",
          "description": "Compétence évaluée (id présent dans skills)."
        },
        "difficulty": {
          "type": "integer",
          "minimum": 1,
          "maximum": 4,
          "description": "1 = facile … 4 = difficile."
        },
        "type": {
          "enum": [
            "number",
            "choice",
            "text"
          ],
          "description": "number = un ou plusieurs nombres ; choice = QCM ; text = réponse courte."
        },
        "prompt": {
          "$ref": "#/$defs/texte",
          "description": "Énoncé."
        },
        "hint": {
          "$ref": "#/$defs/texte",
          "description": "Indice (entraînement seulement) : guide sans donner la réponse."
        },
        "explanation": {
          "$ref": "#/$defs/texte",
          "description": "Correction courte, pas à pas."
        },
        "fields": {
          "type": "array",
          "minItems": 1,
          "maxItems": 4
        },
        "choices": {
          "type": "array",
          "minItems": 2,
          "maxItems": 6
        },
        "answer": {},
        "accepted": {
          "type": "array",
          "minItems": 1
        },
        "common_errors": {
          "type": "array",
          "description": "Facultatif : erreurs fréquentes et message ciblé à afficher.",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "when",
              "message"
            ],
            "properties": {
              "when": {},
              "message": {
                "$ref": "#/$defs/texte",
                "description": "Message affiché si la réponse correspond à cette erreur."
              }
            }
          }
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "type": {
                "const": "number"
              }
            },
            "required": [
              "type"
            ]
          },
          "then": {
            "required": [
              "fields"
            ],
            "properties": {
              "choices": false,
              "answer": false,
              "accepted": false,
              "fields": {
                "description": "Les cases à remplir (ex. quotient et reste).",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "key",
                    "label",
                    "answer"
                  ],
                  "properties": {
                    "key": {
                      "$ref": "#/$defs/identifiant",
                      "description": "Nom technique de la case (q, r…)."
                    },
                    "label": {
                      "$ref": "#/$defs/texte",
                      "description": "Libellé affiché (« quotient »)."
                    },
                    "answer": {
                      "type": "number",
                      "description": "Bonne réponse (nombre, décimal avec un point)."
                    },
                    "unit": {
                      "$ref": "#/$defs/texte",
                      "description": "Facultatif : unité affichée après la case (cm, €…)."
                    }
                  }
                }
              },
              "common_errors": {
                "items": {
                  "properties": {
                    "when": {
                      "type": "object",
                      "minProperties": 1,
                      "additionalProperties": {
                        "type": "number"
                      },
                      "description": "Valeurs de cases qui caractérisent l'erreur, ex. {\"r\": 27}."
                    }
                  }
                }
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "type": {
                "const": "choice"
              }
            },
            "required": [
              "type"
            ]
          },
          "then": {
            "required": [
              "choices",
              "answer"
            ],
            "properties": {
              "fields": false,
              "accepted": false,
              "choices": {
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "id",
                    "label"
                  ],
                  "properties": {
                    "id": {
                      "$ref": "#/$defs/identifiant",
                      "description": "a, b, c…"
                    },
                    "label": {
                      "$ref": "#/$defs/texte"
                    }
                  }
                }
              },
              "answer": {
                "$ref": "#/$defs/identifiant",
                "description": "id du bon choix."
              },
              "common_errors": {
                "items": {
                  "properties": {
                    "when": {
                      "$ref": "#/$defs/identifiant",
                      "description": "id du choix erroné."
                    }
                  }
                }
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "type": {
                "const": "text"
              }
            },
            "required": [
              "type"
            ]
          },
          "then": {
            "required": [
              "accepted"
            ],
            "properties": {
              "fields": false,
              "choices": false,
              "answer": false,
              "accepted": {
                "description": "Réponses acceptées (casse, accents et espaces ignorés).",
                "items": {
                  "$ref": "#/$defs/texte"
                }
              },
              "common_errors": {
                "items": {
                  "properties": {
                    "when": {
                      "$ref": "#/$defs/texte",
                      "description": "Réponse erronée fréquente."
                    }
                  }
                }
              }
            }
          }
        }
      ]
    }
  }
}

Exemple court (extrait d'un vrai module ; le tien sera plus complet) :
{
  "schema_version": 1,
  "id": "maths-cm2-division-euclidienne",
  "version": 1,
  "title": "Division euclidienne",
  "subject": "maths",
  "level": "CM2",
  "description": "Partager en parts égales, trouver le quotient et le reste, vérifier avec la preuve et résoudre des problèmes.",
  "skills": [
    {
      "id": "vocabulaire",
      "label": "Connaître le vocabulaire"
    },
    {
      "id": "multiples",
      "label": "Trouver le bon multiple"
    },
    {
      "id": "verifier",
      "label": "Repérer l'erreur"
    }
  ],
  "lesson": [
    {
      "type": "text",
      "skill": "vocabulaire",
      "title": "L'histoire de Nolan",
      "body": "Nolan est le capitaine de son équipe de rugby. Lui et ses 19 coéquipiers ont reçu **341** cartes de joueurs.\nIl propose : « Partagez-vous équitablement ces 341 cartes entre vous 19. Je prendrai le reste. »\nC'est une **division euclidienne** : on partage en parts égales, et ce qui ne peut pas être partagé s'appelle le reste.\n\n**Dividende** : 341, les cartes à partager.\n**Diviseur** : 19, le nombre de parts.\n**Quotient** : le nombre de cartes de chaque part.\n**Reste** : les cartes qui restent."
    },
    {
      "type": "worked_example",
      "skill": "vocabulaire",
      "title": "Lire une division euclidienne",
      "intro": "On lit l'égalité **347 = 8 × 43 + 3**, qui vient de la division euclidienne de 347 par 8.",
      "steps": [
        {
          "thought": "347 est le nombre que je partage : c'est le **dividende**.",
          "why": "Il est seul, à gauche du signe =."
        },
        {
          "thought": "8 est le nombre par lequel je divise : c'est le **diviseur**.",
          "why": "C'est le nombre de parts (ou la taille d'une part)."
        }
      ],
      "conclusion": "dividende = diviseur × quotient + reste"
    },
    {
      "type": "guided_steps",
      "skill": "multiples",
      "title": "La table de 19",
      "intro": "Pour chercher combien de fois 19 « rentre » dans 341, il faut connaître la table de 19. D'une ligne à la suivante, on ajoute 19.",
      "steps": [
        {
          "prompt": "2 × 19 = ▢",
          "answer": 38,
          "hint": "1 × 19 = 19 ; ensuite on ajoute 19 à chaque ligne."
        },
        {
          "prompt": "3 × 19 = ▢",
          "answer": 57,
          "hint": "Ajoute 19 au résultat précédent : 38 + 19."
        }
      ],
      "conclusion": "Tu connais maintenant la table de 19 : 19, 38, 57, 76, 95, 114, 133, 152, 171."
    },
    {
      "type": "worked_example",
      "skill": "verifier",
      "title": "Repérer l'erreur",
      "intro": "Un élève écrit : « 100 = 7 × 13 + 9 ». A-t-il juste ?",
      "steps": [
        {
          "thought": "Je vérifie le calcul : 7 × 13 = 91, et 91 + 9 = 100.",
          "why": "La preuve doit redonner le dividende."
        },
        {
          "thought": "Le calcul est juste. Je regarde le reste : 9 est-il plus petit que 7 ? Non.",
          "why": "Le reste doit toujours être plus petit que le diviseur."
        }
      ],
      "conclusion": "Deux vérifications : le calcul, puis reste < diviseur."
    }
  ],
  "questions": [
    {
      "id": "q009",
      "skill": "multiples",
      "difficulty": 1,
      "type": "number",
      "prompt": "Quel est le plus grand multiple de **4** qui ne dépasse pas **23** ?",
      "fields": [
        {
          "key": "m",
          "label": "ce multiple",
          "answer": 20
        }
      ],
      "hint": "Un multiple de 4 est un nombre de la table de 4.\nTable de 4 : 1 × 4 = 4, 2 × 4 = 8, 3 × 4 = 12, 4 × 4 = 16, 5 × 4 = 20, 6 × 4 = 24, 7 × 4 = 28, 8 × 4 = 32, 9 × 4 = 36.",
      "explanation": "4 × 5 = **20** ne dépasse pas 23.\nLe multiple suivant, 4 × 6 = 24, est trop grand.",
      "common_errors": [
        {
          "when": {
            "m": 24
          },
          "message": "24 dépasse 23. Il faut un multiple plus petit."
        }
      ]
    },
    {
      "id": "q020",
      "skill": "verifier",
      "difficulty": 1,
      "type": "choice",
      "prompt": "Un élève écrit : **« 26 = 4 × 6 + 2 »**.\nA-t-il bien fait la division euclidienne de **26** par **4** ?",
      "choices": [
        {
          "id": "a",
          "label": "Oui, c'est correct"
        },
        {
          "id": "b",
          "label": "Non : le calcul est faux"
        },
        {
          "id": "c",
          "label": "Non : le reste est trop grand"
        }
      ],
      "answer": "a",
      "hint": "Vérifie deux choses :\n1. Le reste est-il plus petit que le diviseur ?\n2. 4 × 6 + 2 donne-t-il bien 26 ?",
      "explanation": "Oui : 4 × 6 + 2 = 26 et 2 < 4. C'est correct."
    },
    {
      "id": "q033",
      "skill": "vocabulaire",
      "difficulty": 1,
      "type": "text",
      "prompt": "Dans l'égalité **347 = 8 × 43 + 3** (division euclidienne de 347 par 8), comment s'appelle le nombre **43** ?",
      "accepted": [
        "quotient",
        "le quotient"
      ],
      "hint": "C'est le nombre de fois que 8 « rentre » dans 347.",
      "explanation": "43 est le **quotient** : c'est le nombre de parts que l'on peut faire (ou la taille de chaque part).",
      "common_errors": [
        {
          "when": "reste",
          "message": "Le reste, c'est ce qu'il reste à la fin : ici 3."
        }
      ]
    }
  ]
}
