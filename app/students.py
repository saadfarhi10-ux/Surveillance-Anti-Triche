from __future__ import annotations

from typing import Dict, List


STUDENTS_IDS: Dict[str, str] = {
    "C-2026-000001": "Achik Ibtissame",
    "C-2026-000002": "El Kharraz Aya",
    "C-2026-000003": "Sassioui Fatima Ezzahra",

    "C-2026-000004": "Alami Reda",
    "C-2026-000005": "Belbiad Abderrahmane",
    "C-2026-000006": "Berrqia Anas",

    "C-2026-000007": "Anouch Haitam",
    "C-2026-000008": "Misbah Imad",
    "C-2026-000009": "El Baamrani Mohamed Saad",

    "C-2026-000010": "Rachid Amine",
    "C-2026-000011": "Farhi Saad",

    "C-2026-000012": "Assni Adam",
    "C-2026-000013": "Khay Mohammed",

    "C-2026-000014": "Bitit Nizar",
    "C-2026-000015": "Erraouii Rayane",

    "C-2026-000016": "Hmadate Hamza",
    "C-2026-000017": "Benzakri Alae",

    "C-2026-000018": "Aboulouafa Yasmine",
    "C-2026-000019": "Machou Imane",
    "C-2026-000020": "Haouach Chaimaa",

    "C-2026-000021": "Boulaiz Ilyass",
    "C-2026-000022": "Kharibach Ilyass",
    "C-2026-000023": "Azoui Mouad",

    "C-2026-000024": "Ailoul Youssef",
    "C-2026-000025": "Fetouaki Youssef",
    "C-2026-000026": "Mrahi Saad",
}


STUDENTS_ORDER: List[str] = list(STUDENTS_IDS.values())


def normalize_student_id(student_id: str) -> str:
    return student_id.strip().upper()


def is_valid_student(student_id: str, full_name: str) -> bool:
    sid = normalize_student_id(student_id)
    name = full_name.strip()

    return STUDENTS_IDS.get(sid) == name