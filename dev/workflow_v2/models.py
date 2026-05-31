from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


ALLOWED_STATUS = {"unmapped", "mapped", "validated", "rejected"}


@dataclass
class Scope:
    geographic_scope: str
    temporal_scope: str
    capacity_scope: str
    system_boundary: str


@dataclass
class SourceRef:
    source_id: str
    relevance: str = "primary"


@dataclass
class AssumptionRef:
    assumption_id: str
    relevance: str = "primary"


@dataclass
class ValueItem:
    attribute_id: str
    value: Any
    value_type: str
    unit: str
    uncertainty: dict[str, Any] | None = None
    note: str | None = None


@dataclass
class MappingMeta:
    mapped_tech_id: str | None = None
    mapped_process_id: str | None = None
    confidence: float | None = None
    method: str | None = None
    mapping_notes: str | None = None
    ontology_iri: str | None = None
    approved_by: str | None = None
    approved_at: str | None = None


@dataclass
class Record:
    record_id: str
    temp_id: str
    description: str
    status: str
    scope: Scope
    sources: list[SourceRef] = field(default_factory=list)
    assumptions: list[AssumptionRef] = field(default_factory=list)
    values: list[ValueItem] = field(default_factory=list)
    mapping: MappingMeta = field(default_factory=MappingMeta)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.record_id:
            errors.append("record_id is required")
        if not self.temp_id:
            errors.append("temp_id is required")
        if not self.description or len(self.description.strip()) < 20:
            errors.append("description must be at least 20 characters")
        if self.status not in ALLOWED_STATUS:
            errors.append(f"status must be one of: {sorted(ALLOWED_STATUS)}")
        if not self.sources:
            errors.append("at least one source is required")
        if not self.values:
            errors.append("at least one value is required")
        return errors


@dataclass
class Suggestion:
    record_id: str
    temp_id: str
    suggested_tech_id: str
    suggested_process_id: str
    confidence: float
    method: str
    rationale: str
    ontology_iri: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
