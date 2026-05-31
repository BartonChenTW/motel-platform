from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dev.workflow_v2.pipeline import WorkflowEngine
from dev.workflow_v2.settings import WorkflowPaths


class WorkflowV2Test(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        data_root = root / "workflow_data"
        self.paths = WorkflowPaths(
            root=root,
            data_root=data_root,
            unmapped_dir=data_root / "unmapped_records",
            mapped_dir=data_root / "mapped_records",
            sources_dir=data_root / "sources",
            suggestions_dir=data_root / "suggestions",
            technologies_csv=data_root / "technologies.csv",
            processes_csv=data_root / "processes.csv",
        )
        self.paths.unmapped_dir.mkdir(parents=True, exist_ok=True)
        self.paths.mapped_dir.mkdir(parents=True, exist_ok=True)
        self.paths.sources_dir.mkdir(parents=True, exist_ok=True)
        self.paths.suggestions_dir.mkdir(parents=True, exist_ok=True)

        self.paths.technologies_csv.write_text(
            "tech_id,technology_name,ontology_iri,process_id\n"
            "T_SOLAR,Solar photovoltaic,motel:T_SOLAR,P_GEN\n",
            encoding="utf-8",
        )
        self.paths.processes_csv.write_text(
            "process_id,process_name,ontology_iri\n"
            "P_GEN,Electricity generation,motel:P_GEN\n",
            encoding="utf-8",
        )
        self.engine = WorkflowEngine(self.paths)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_submit_suggest_approve(self) -> None:
        record = self.engine.create_and_submit(
            description="Solar photovoltaic roof system for electricity production in residential buildings.",
            scope={
                "geographic_scope": "GEO_CH",
                "temporal_scope": "TIME_2026",
                "capacity_scope": "CAP_RESIDENTIAL",
                "system_boundary": "COND_GRID_CONNECTED",
            },
            source_id="SRC_001",
            attribute_id="ATTR_CAPEX",
            value=1000.0,
            unit="CHF/kW",
        )
        self.assertEqual(record.status, "unmapped")
        self.assertEqual(len(self.engine.list_unmapped()), 1)

        suggestions = self.engine.build_suggestions()
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0].suggested_tech_id, "T_SOLAR")

        mapped_path = self.engine.approve_suggestion(record.record_id, reviewer="tester")
        self.assertTrue(mapped_path.exists())
        self.assertEqual(len(self.engine.list_unmapped()), 0)
        self.assertEqual(len(self.engine.list_mapped()), 1)


if __name__ == "__main__":
    unittest.main()
