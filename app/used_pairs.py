from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Tuple


@dataclass(frozen=True)
class StudentSubjectPair:
    student_id: str
    subject: str


class UsedPairsStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _load_raw(self) -> List[dict]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data
        except json.JSONDecodeError:
            return []

    def load_pairs(self) -> Set[Tuple[str, str]]:
        pairs: Set[Tuple[str, str]] = set()
        for item in self._load_raw():
            sid = str(item.get("student_id", "")).strip()
            subj = str(item.get("subject", "")).strip()
            if sid and subj:
                pairs.add((sid, subj))
        return pairs

    def add_pair(self, student_id: str, subject: str) -> None:
        sid = student_id.strip()
        subj = subject.strip()
        rows = self._load_raw()
        rows.append({"student_id": sid, "subject": subj})
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    def used_subjects_for_student(self, student_id: str) -> Set[str]:
        sid = student_id.strip()
        return {subj for (s, subj) in self.load_pairs() if s == sid}
