from __future__ import annotations
from typing import Dict, List, Tuple

# Durees demandees:
# - 1h: Communication Professionnelle 2, Intermediate English 2
# - 2h: Conception Orientee Objet, Modeles Statistiques, Programmation Lineaire
# - 3h: le reste
SUBJECT_DURATION_MINUTES: Dict[str, int] = {
    "Programmation Python et Framework": 180,
    "Conception Orientée Objet": 120,
    "Modèles Statistiques": 120,
    "Programmation Linéaire": 120,
    "Communication Professionnelle 2": 60,
    "Intermediate English 2": 60,
    "Programmation Java": 180,
    "SQL Server": 180,
    "Recherche Scientifique": 180,
    "Réseaux Informatiques 2": 180,
}

SUBJECTS_ORDER: List[str] = [
    "Programmation Python et Framework",
    "Conception Orientée Objet",
    "Modèles Statistiques",
    "Programmation Linéaire",
    "Communication Professionnelle 2",
    "Intermediate English 2",
    "Programmation Java",
    "SQL Server",
    "Recherche Scientifique",
    "Réseaux Informatiques 2",
]


def minutes_for_subject(subject: str) -> int:
    if subject not in SUBJECT_DURATION_MINUTES:
        raise KeyError(f"Matiere inconnue: {subject}")
    return SUBJECT_DURATION_MINUTES[subject]

