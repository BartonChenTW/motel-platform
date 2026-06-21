from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .deduplicator import DuplicatePair, detect_duplicates
from .mapper import suggest_mapping
from .models import MappingMeta, Record, Scope, SourceRef, Suggestion, ValueItem
from .settings import WorkflowPaths
from .storage import read_record, read_suggestions, write_record, write_suggestions


class WorkflowEngine:
    def __init__(self, paths: WorkflowPaths):
        self.paths = paths

    def _next_ids(self) -> tuple[str, str]:
        existing = list(self.paths.unmapped_dir.glob("REC_*.yaml")) + list(self.paths.mapped_dir.glob("REC_*.yaml"))
        n = len(existing) + 1
        return f"REC_{n:04d}", f"TMP_{n:04d}"

    def submit_record(self, record: Record) -> Path:
        errors = record.validate()
        if errors:
            raise ValueError("Record validation failed: " + "; ".join(errors))
        record.status = "unmapped"
        return write_record(record, self.paths.unmapped_dir)

    def create_and_submit(self, *, description: str, scope: dict, source_id: str, attribute_id: str, value: float, unit: str) -> Record:
        record_id, temp_id = self._next_ids()
        record = Record(
            record_id=record_id,
            temp_id=temp_id,
            description=description,
            status="unmapped",
            scope=Scope(**scope),
            sources=[SourceRef(source_id=source_id)],
            values=[ValueItem(attribute_id=attribute_id, value=value, value_type="numeric", unit=unit)],
        )
        self.submit_record(record)
        return record

    def list_unmapped(self) -> list[Record]:
        return [read_record(path) for path in sorted(self.paths.unmapped_dir.glob("REC_*.yaml"))]

    def list_mapped(self) -> list[Record]:
        return [read_record(path) for path in sorted(self.paths.mapped_dir.glob("REC_*.yaml"))]

    def build_suggestions(self) -> list[Suggestion]:
        suggestions: list[Suggestion] = []
        for record in self.list_unmapped():
            suggestions.append(
                suggest_mapping(
                    record,
                    technologies_csv=self.paths.technologies_csv,
                    processes_csv=self.paths.processes_csv,
                )
            )
        write_suggestions(suggestions, self.paths.suggestions_dir / "latest.yaml")
        return suggestions

    def get_suggestions(self) -> list[Suggestion]:
        return read_suggestions(self.paths.suggestions_dir / "latest.yaml")

    def approve_suggestion(self, record_id: str, reviewer: str, notes: str = "") -> Path:
        suggestion_map = {s.record_id: s for s in self.get_suggestions()}
        if record_id not in suggestion_map:
            raise ValueError(f"No suggestion found for {record_id}")

        target_path = self.paths.unmapped_dir / f"{record_id}.yaml"
        if not target_path.exists():
            raise FileNotFoundError(f"Unmapped record not found: {record_id}")

        record = read_record(target_path)
        suggestion = suggestion_map[record_id]
        record.status = "mapped"
        record.mapping = MappingMeta(
            mapped_tech_id=suggestion.suggested_tech_id,
            mapped_process_id=suggestion.suggested_process_id,
            confidence=suggestion.confidence,
            method=suggestion.method,
            mapping_notes=notes or suggestion.rationale,
            ontology_iri=suggestion.ontology_iri,
            approved_by=reviewer,
            approved_at=datetime.utcnow().isoformat(),
        )

        mapped_path = write_record(record, self.paths.mapped_dir)
        target_path.unlink(missing_ok=True)
        return mapped_path

    def dedupe_report(self) -> list[DuplicatePair]:
        records = self.list_unmapped() + self.list_mapped()
        return detect_duplicates(records)

    def dedupe_report_as_dict(self) -> list[dict]:
        return [asdict(item) for item in self.dedupe_report()]
