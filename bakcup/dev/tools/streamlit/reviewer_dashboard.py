from __future__ import annotations

from pathlib import Path

import streamlit as st

from bakcup.dev.workflow_v2.pipeline import WorkflowEngine
from bakcup.dev.workflow_v2.settings import WorkflowPaths, detect_repo_root


repo_root = detect_repo_root(Path(__file__).resolve())
engine = WorkflowEngine(WorkflowPaths.from_repo_root(repo_root))

st.set_page_config(page_title="MOTEL Reviewer Dashboard", layout="wide")
st.title("MOTEL Workflow v2: Reviewer Dashboard")

if st.button("Generate Fresh Suggestions"):
    generated = engine.build_suggestions()
    st.success(f"Generated {len(generated)} suggestions")

suggestions = engine.get_suggestions()
if not suggestions:
    st.info("No suggestions yet. Generate suggestions first.")
else:
    table = [s.to_dict() for s in suggestions]
    st.dataframe(table, use_container_width=True)

    record_ids = [s.record_id for s in suggestions]
    selected = st.selectbox("Record to approve", record_ids)
    reviewer = st.text_input("Reviewer", value="reviewer_01")
    notes = st.text_area("Notes", value="Approved after quick validation")

    if st.button("Approve Selected"):
        try:
            path = engine.approve_suggestion(selected, reviewer=reviewer, notes=notes)
            st.success(f"Approved and moved to mapped: {path.name}")
        except Exception as exc:
            st.error(f"Approval failed: {exc}")

st.subheader("Duplicate Check")
if st.button("Run Deduplication"):
    dedupe_rows = engine.dedupe_report_as_dict()
    if dedupe_rows:
        st.dataframe(dedupe_rows, use_container_width=True)
    else:
        st.success("No duplicates detected.")
