from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import (
    AssumptionRef,
    MappingMeta,
    Record,
    Scope,
    SourceRef,
    Suggestion,
    ValueItem,
)

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def _serialize(data: dict[str, Any]) -> str:
    if yaml is not None:
        return yaml.safe_dump(data, sort_keys=False)
    return json.dumps(data, indent=2)


def _deserialize(text: str) -> dict[str, Any]:
    if yaml is not None:
        parsed = yaml.safe_load(text)
        return parsed if isinstance(parsed, dict) else {}
    parsed = json.loads(text)
    return parsed if isinstance(parsed, dict) else {}


def ensure_dirs(*dirs: Path) -> None:
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def write_record(record: Record, target_dir: Path) -> Path:
    ensure_dirs(target_dir)
    record.updated_at = datetime.utcnow().isoformat()
    path = target_dir / f"{record.record_id}.yaml"
    path.write_text(_serialize(record.to_dict()), encoding="utf-8")
    return path


def read_record(path: Path) -> Record:
    raw = _deserialize(path.read_text(encoding="utf-8"))
    scope_raw = raw.get("scope", {})
    source_raw = raw.get("sources", [])
    assumption_raw = raw.get("assumptions", [])
    values_raw = raw.get("values", [])
    mapping_raw = raw.get("mapping", {})

    record = Record(
        record_id=raw["record_id"],
        temp_id=raw["temp_id"],
        description=raw["description"],
        status=raw.get("status", "unmapped"),
        scope=Scope(
            geographic_scope=scope_raw.get("geographic_scope", "GEO_UNK"),
            temporal_scope=scope_raw.get("temporal_scope", "TIME_UNK"),
            capacity_scope=scope_raw.get("capacity_scope", "CAP_UNK"),
            system_boundary=scope_raw.get("system_boundary", "COND_UNK"),
        ),
        sources=[
            SourceRef(source_id=item.get("source_id", "SRC_UNK"), relevance=item.get("relevance", "primary"))
            for item in source_raw
        ],
        assumptions=[
            AssumptionRef(
                assumption_id=item.get("assumption_id", "ASSUME_UNK"),
                relevance=item.get("relevance", "primary"),
            )
            for item in assumption_raw
        ],
        values=[
            ValueItem(
                attribute_id=item.get("attribute_id", "ATTR_UNK"),
                value=item.get("value"),
                value_type=item.get("value_type", "numeric"),
                unit=item.get("unit", "-"),
                uncertainty=item.get("uncertainty"),
                note=item.get("note"),
            )
            for item in values_raw
        ],
        mapping=MappingMeta(**mapping_raw),
        created_at=raw.get("created_at", datetime.utcnow().isoformat()),
        updated_at=raw.get("updated_at", datetime.utcnow().isoformat()),
    )
    return record


def write_suggestions(suggestions: list[Suggestion], path: Path) -> None:
    payload = [asdict(item) for item in suggestions]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_serialize({"suggestions": payload}), encoding="utf-8")


def read_suggestions(path: Path) -> list[Suggestion]:
    if not path.exists():
        return []
    raw = _deserialize(path.read_text(encoding="utf-8"))
    out: list[Suggestion] = []
    for item in raw.get("suggestions", []):
        out.append(Suggestion(**item))
    return out
