# Workflow v2 Developer Notes

## Design choices

- Keep all new files under dev/ as requested.
- Avoid heavy ML dependencies; use difflib similarity.
- Keep data contracts explicit via dataclasses and validate() checks.

## Main modules

- workflow_v2/models.py: record, mapping, and suggestion data models.
- workflow_v2/storage.py: YAML/JSON compatible persistence.
- workflow_v2/mapper.py: rule-based fuzzy mapping against CSV catalogs.
- workflow_v2/deduplicator.py: duplicate pair detection.
- workflow_v2/pipeline.py: orchestrates submit, suggest, approve, and dedupe.
- workflow_v2/cli.py: terminal interface.

## Extending mapping quality

- Add token weights for domain terms.
- Add synonym dictionaries from ontology labels.
- Add scope-aware ranking boosts.
- Add confidence threshold policy for auto-reject.
