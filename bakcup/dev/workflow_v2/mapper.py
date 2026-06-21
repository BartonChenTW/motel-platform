from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from .models import Record, Suggestion


@dataclass
class CatalogRow:
    item_id: str
    name: str
    ontology_iri: str
    process_id: str | None = None


def _normalize(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def _score(a: str, b: str) -> float:
    return SequenceMatcher(a=_normalize(a), b=_normalize(b)).ratio()


def _load_catalog(path: Path, id_col: str, name_col: str, ontology_col: str, process_col: str | None = None) -> list[CatalogRow]:
    rows: list[CatalogRow] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            item_id = (row.get(id_col) or "").strip()
            if not item_id:
                continue
            rows.append(
                CatalogRow(
                    item_id=item_id,
                    name=(row.get(name_col) or item_id).strip(),
                    ontology_iri=(row.get(ontology_col) or "").strip(),
                    process_id=(row.get(process_col) or "").strip() if process_col else None,
                )
            )
    return rows


def suggest_mapping(record: Record, technologies_csv: Path, processes_csv: Path) -> Suggestion:
    tech_rows = _load_catalog(
        technologies_csv,
        id_col="tech_id",
        name_col="technology_name",
        ontology_col="ontology_iri",
        process_col="process_id",
    )
    process_rows = _load_catalog(
        processes_csv,
        id_col="process_id",
        name_col="process_name",
        ontology_col="ontology_iri",
    )

    if not tech_rows:
        return Suggestion(
            record_id=record.record_id,
            temp_id=record.temp_id,
            suggested_tech_id="UNMAPPED",
            suggested_process_id="UNMAPPED",
            confidence=0.0,
            method="rule_fuzzy",
            rationale="No technology catalog rows available",
            ontology_iri=None,
        )

    ranked = sorted(
        ((row, _score(record.description, row.name)) for row in tech_rows),
        key=lambda item: item[1],
        reverse=True,
    )
    top_row, top_score = ranked[0]

    process_id = top_row.process_id or "UNMAPPED"
    if process_id == "UNMAPPED" and process_rows:
        ranked_process = sorted(
            ((row, _score(record.description, row.name)) for row in process_rows),
            key=lambda item: item[1],
            reverse=True,
        )
        process_id = ranked_process[0][0].item_id

    return Suggestion(
        record_id=record.record_id,
        temp_id=record.temp_id,
        suggested_tech_id=top_row.item_id,
        suggested_process_id=process_id,
        confidence=round(top_score, 4),
        method="rule_fuzzy",
        rationale=f"Top name similarity match: {top_row.name}",
        ontology_iri=top_row.ontology_iri or None,
    )
