from __future__ import annotations

from pathlib import Path

from .pipeline import WorkflowEngine
from .settings import WorkflowPaths, detect_repo_root


def bootstrap_demo_records() -> None:
    repo_root = detect_repo_root(Path(__file__).resolve())
    engine = WorkflowEngine(WorkflowPaths.from_repo_root(repo_root))

    if engine.list_unmapped() or engine.list_mapped():
        return

    base_scope = {
        "geographic_scope": "GEO_CH",
        "temporal_scope": "TIME_2026",
        "capacity_scope": "CAP_RESIDENTIAL",
        "system_boundary": "COND_GRID_CONNECTED",
    }

    engine.create_and_submit(
        description="Rooftop solar photovoltaic system for residential electricity generation in Switzerland with typical capex assumptions.",
        scope=base_scope,
        source_id="SRC_NREL_ATB_2023",
        attribute_id="ATTR_CAPEX",
        value=980.0,
        unit="CHF/kW",
    )

    engine.create_and_submit(
        description="Lithium-ion battery energy storage used for household peak shaving and daily charging cycles.",
        scope=base_scope,
        source_id="SRC_SWISSGRID_2025",
        attribute_id="ATTR_EFFICIENCY",
        value=0.91,
        unit="fraction",
    )


if __name__ == "__main__":
    bootstrap_demo_records()
