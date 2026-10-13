# Programmes officiels

Référence pour créer les modules : à consulter pour savoir ce qui se travaille en CM1, CM2 et 6e.
Chaque programme a deux fichiers : le PDF (l'original, il fait foi) et un `.md` (le texte extrait,
page par page avec `<!-- page N -->`, plus facile à chercher et à lire pour Claude). Dans le
texte extrait, la mise en page (colonnes, tableaux) peut être imparfaite et un symbole peut
manquer (par exemple la case vide d'une égalité à trous en maths).

| Fichier | Programme | Date du PDF |
|---|---|---|
| `francais-cycle3` | Français, cycle 3 (CM1, CM2, 6e) | avril 2025 |
| `maths-cycle3` | Mathématiques, cycle 3 | avril 2025 |
| `histoire-geographie-cycle3` | Histoire-géographie, cycle 3 | avril 2026 |
| `langues-vivantes-cours-moyen-cycle3` | Langues vivantes étrangères et régionales, cours moyen | février 2026 |
| `anglais-6e` | Anglais, classes de collège (6e) | mai 2025 |
| `education-vie-affective-relationnelle-primaire` | Éducation à la vie affective et relationnelle, école élémentaire | février 2025 |

**Manquant : sciences et technologie du cycle 3** (programme de juin 2026). Voir plus bas.

## Source

Documents officiels du ministère de l'Éducation nationale, téléchargés par le sponsor depuis
Eduscol (https://eduscol.education.gouv.fr/4356/enseigner-au-cycle-3) le 14 octobre 2026.
Claude n'a pas pu les télécharger lui-même : Eduscol bloque les accès automatiques (erreur 403).

Un ancien programme (cycle 3 « en vigueur à la rentrée 2023 », 108 pages) a été retiré le
14 octobre 2026 : il était remplacé par ceux-ci (maths et français 2025, histoire-géographie
et sciences 2026). Les repères annuels de progression et les attendus de fin d'année d'Eduscol
ne sont pas dans ce dossier.

## Sciences et technologie : à ajouter (priorité basse)

Le PDF d'Eduscol (« Annexe 2 – programme de sciences et technologie du cycle 3 », arrêté
MENE2611650A, juin 2026) est une **image scannée, sans texte**, et il pèse 18 Mo : Claude ne
peut pas le lire, et il ne faut pas l'ajouter au dépôt (public, l'historique garde tout).
Mode opératoire, sur le Mac du sponsor :

1. Télécharger le PDF depuis Eduscol et l'ouvrir dans **Aperçu**.
2. Menu Édition > Tout sélectionner, puis Édition > Copier (le « Texte en direct » reconnaît le
   texte de l'image). Si rien n'est sélectionné, essayer sur quelques pages à la fois.
3. Coller dans un fichier texte et l'enregistrer sous `sciences-technologie-cycle3.md` (avec une
   ligne d'en-tête : titre, source, date).
4. Le mettre dans `programmes/` (le **seul** fichier `.md`, pas le PDF), puis demander à Claude
   de l'ajouter à la table ci-dessus et de pousser.

Autres pistes si le texte en direct est mauvais : réparer `tesseract` sur le Mac (il lui manque
`libtiff`, `brew` ne gère plus les Mac Intel), ou ouvrir l'accès réseau de l'environnement cloud
de Claude (tâche du sponsor dans `pilotage.md`) pour qu'il cherche une version avec du texte.

## Si un programme change

Remplacer le PDF et son `.md` (même nom, ou nom avec l'année) et mettre à jour la table. Ne pas
modifier le texte à la main : c'est une copie du document officiel.
