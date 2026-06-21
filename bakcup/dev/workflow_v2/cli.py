from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import WorkflowEngine
from .settings import WorkflowPaths, detect_repo_root


def build_engine(repo_root: Path | None = None) -> WorkflowEngine:
    root = repo_root or detect_repo_root()
    return WorkflowEngine(WorkflowPaths.from_repo_root(root))


def cmd_submit(args: argparse.Namespace) -> None:
    engine = build_engine()
    scope = {
        "geographic_scope": args.geographic_scope,
        "temporal_scope": args.temporal_scope,
        "capacity_scope": args.capacity_scope,
        "system_boundary": args.system_boundary,
    }
    record = engine.create_and_submit(
        description=args.description,
        scope=scope,
        source_id=args.source_id,
        attribute_id=args.attribute_id,
        value=args.value,
        unit=args.unit,
    )
    print(json.dumps(record.to_dict(), indent=2))


def cmd_suggest(_: argparse.Namespace) -> None:
    engine = build_engine()
    suggestions = engine.build_suggestions()
    print(json.dumps([s.to_dict() for s in suggestions], indent=2))


def cmd_approve(args: argparse.Namespace) -> None:
    engine = build_engine()
    path = engine.approve_suggestion(args.record_id, reviewer=args.reviewer, notes=args.notes)
    print(f"Mapped record written: {path}")


def cmd_dedupe(_: argparse.Namespace) -> None:
    engine = build_engine()
    report = engine.dedupe_report_as_dict()
    print(json.dumps(report, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MOTEL Workflow v2 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    submit = sub.add_parser("submit", help="Submit one record")
    submit.add_argument("--description", required=True)
    submit.add_argument("--source-id", default="SRC_USER_001")
    submit.add_argument("--attribute-id", default="ATTR_CAPEX")
    submit.add_argument("--value", type=float, required=True)
    submit.add_argument("--unit", default="CHF/kW")
    submit.add_argument("--geographic-scope", default="GEO_CH")
    submit.add_argument("--temporal-scope", default="TIME_2026")
    submit.add_argument("--capacity-scope", default="CAP_RESIDENTIAL")
    submit.add_argument("--system-boundary", default="COND_GRID_CONNECTED")
    submit.set_defaults(func=cmd_submit)

    suggest = sub.add_parser("suggest", help="Generate mapping suggestions")
    suggest.set_defaults(func=cmd_suggest)

    approve = sub.add_parser("approve", help="Approve one suggestion")
    approve.add_argument("--record-id", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--notes", default="")
    approve.set_defaults(func=cmd_approve)

    dedupe = sub.add_parser("dedupe", help="Run duplicate detection")
    dedupe.set_defaults(func=cmd_dedupe)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
