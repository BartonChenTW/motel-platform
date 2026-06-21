from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from difflib import SequenceMatcher

from .models import Record


@dataclass
class DuplicatePair:
    record_id_a: str
    record_id_b: str
    similarity: float
    reason: str


def _norm(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _fingerprint(record: Record) -> str:
    payload = f"{_norm(record.description)}|{record.scope.geographic_scope}|{record.scope.temporal_scope}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def detect_duplicates(records: list[Record], threshold: float = 0.9) -> list[DuplicatePair]:
    results: list[DuplicatePair] = []

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            left = records[i]
            right = records[j]

            if _fingerprint(left) == _fingerprint(right):
                results.append(
                    DuplicatePair(
                        record_id_a=left.record_id,
                        record_id_b=right.record_id,
                        similarity=1.0,
                        reason="Exact normalized fingerprint match",
                    )
                )
                continue

            score = SequenceMatcher(a=_norm(left.description), b=_norm(right.description)).ratio()
            if score >= threshold:
                results.append(
                    DuplicatePair(
                        record_id_a=left.record_id,
                        record_id_b=right.record_id,
                        similarity=round(score, 4),
                        reason=f"Description similarity >= {threshold}",
                    )
                )

    return results
