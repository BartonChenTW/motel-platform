from __future__ import annotations

from pathlib import Path

import streamlit as st

from dev.workflow_v2.pipeline import WorkflowEngine
from dev.workflow_v2.settings import WorkflowPaths, detect_repo_root


repo_root = detect_repo_root(Path(__file__).resolve())
engine = WorkflowEngine(WorkflowPaths.from_repo_root(repo_root))

st.set_page_config(page_title="MOTEL User Submission", layout="wide")
st.title("MOTEL Workflow v2: User Submission")

with st.form("submit_form"):
    description = st.text_area("Description", height=150)
    source_id = st.text_input("Source ID", value="SRC_USER_001")
    attribute_id = st.selectbox("Attribute", ["ATTR_CAPEX", "ATTR_EFFICIENCY", "ATTR_LIFETIME"])
    value = st.number_input("Value", value=800.0, step=10.0)
    unit = st.text_input("Unit", value="CHF/kW")

    col1, col2 = st.columns(2)
    with col1:
        geographic_scope = st.text_input("Geographic Scope", value="GEO_CH")
        temporal_scope = st.text_input("Temporal Scope", value="TIME_2026")
    with col2:
        capacity_scope = st.text_input("Capacity Scope", value="CAP_RESIDENTIAL")
        system_boundary = st.text_input("System Boundary", value="COND_GRID_CONNECTED")

    submitted = st.form_submit_button("Submit Record")

if submitted:
    scope = {
        "geographic_scope": geographic_scope,
        "temporal_scope": temporal_scope,
        "capacity_scope": capacity_scope,
        "system_boundary": system_boundary,
    }
    try:
        record = engine.create_and_submit(
            description=description,
            scope=scope,
            source_id=source_id,
            attribute_id=attribute_id,
            value=value,
            unit=unit,
        )
        st.success(f"Submitted: {record.record_id} ({record.temp_id})")
        st.json(record.to_dict())
    except Exception as exc:
        st.error(f"Submission failed: {exc}")

st.subheader("Current Unmapped Queue")
rows = [r.to_dict() for r in engine.list_unmapped()]
if rows:
    st.dataframe([{"record_id": r["record_id"], "temp_id": r["temp_id"], "status": r["status"], "description": r["description"]} for r in rows], use_container_width=True)
else:
    st.info("No unmapped records yet.")
