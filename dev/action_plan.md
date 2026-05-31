 📋 **MOTEL Workflow v2: Execution Plan**
**Project**: Developing a Methodology for Open Technology Data in Energy Models (MOTEL)
**Version**: 1.0
**Date**: 2026-01-15
**Status**: Draft
**Owner**: Barton Chen, Dennis Beermann

---

---

## **🎯 Overview**
This plan outlines the implementation of **Workflow v2** for the MOTEL project, enabling **flexible data collection** followed by **structured mapping** to technologies/processes and ontologies. The goal is to lower the barrier for contributors while ensuring **traceability, interoperability, and standardization**.

**Key Principles**:
- **User-First**: Users submit records with descriptions, scopes, and sources (no upfront `tech_id`/`process_id` required).
- **Automated + Manual Mapping**: Records are automatically mapped to existing technologies/processes (where possible) and manually validated by domain experts.
- **Traceability**: Every record retains provenance (sources, assumptions, mapping decisions).
- **Ontology Integration**: Mapped records are linked to **Open Energy Ontology (OEO)** or custom MOTEL terms.

---

---

## **📌 Workflow v2 Diagram**
```mermaid
graph TD
    A[User Submits Record] --> Description, Scope, Sources| B(Store as Unmapped Record)
    B --> C[Automated Mapping Suggestion]
    C --> D[Manual Review by Expert]
    D -->|Approved| E[Assign tech_id/process_id]
    D -->|Rejected| F[Request Clarification]
    E --> G[Link to Ontology (OEO/MOTEL)]
    G --> H[Publish to Database]
    H --> I[Notify User of Mapping]




🗂️ Repository Structure


motel-db/
├── data/
│   ├── unmapped_records/          # Records awaiting mapping
│   │   ├── REC_001.yaml
│   │   └── ...
│   ├── mapped_records/            # Records after mapping
│   │   ├── REC_001.yaml
│   │   └── ...
│   ├── technologies/              # Technology definitions
│   │   ├── tech_list.csv
│   │   └── ...
│   ├── processes/                  # Process definitions
│   │   ├── process_list.csv
│   │   └── ...
│   └── sources/                   # Source metadata
│
├── ontology/                      # Ontology files
│   ├── motel.ttl                  # Custom ontology (TTL format)
│   └── imports/                   # Imported ontologies (e.g., OEO)
│
├── scripts/
│   └── mapping/
│       ├── auto_mapper.py         # Automated mapping (NLP + ontology)
│       ├── ontology_mapper.py     # Ontology-based matching
│       ├── combined_mapper.py      # Combine NLP + ontology results
│       ├── deduplicator.py        # Detect duplicate records
│       ├── validator.py            # Validate YAML records
│       ├── save_record.py          # Save records to YAML
│       ├── update_mapping.py       # Update records with mappings
│       └── link_to_ontology.py     # Link records to ontology terms
│
├── tools/
│   ├── streamlit/
│   │   ├── user_submission.py     # User interface for submitting records
│   │   └── reviewer_dashboard.py  # Interface for validating mappings
│   └── fastapi/
│       └── app.py                 # Backend API (optional)
│
├── docs/
│   ├── workflow.md               # Workflow documentation
│   ├── user_guide.md              # How to submit records
│   └── reviewer_guide.md          # How to validate mappings
│
├── schema/
│   └── motel_schema.yaml         # Updated schema for Workflow v2
│
└── README.md




📅 Timeline and Milestones






  
    
      Phase
      Tasks
      Timeline
      Owner
    
  
  
    
      Phase 1: Setup and Preparation
      Update schema, create directories, draft guidelines.
      Week 1–2
      Barton/Dennis
    
    
      Phase 2: User Submission Interface
      Build Streamlit form, YAML validator, temp ID generator.
      Week 3–5
      Dennis
    
    
      Phase 3: Automated Mapping
      Develop NLP/ontology matching, deduplication, suggestions.
      Week 6–9
      Barton
    
    
      Phase 4: Manual Review Interface
      Build reviewer dashboard, approval workflow.
      Week 10–12
      Dennis
    
    
      Phase 5: Ontology Integration
      Update ontology, link records, validate.
      Week 13–15
      Barton
    
    
      Phase 6: Testing and Validation
      Test end-to-end workflow, validate database.
      Week 16–18
      Barton/Dennis
    
    
      Phase 7: Deployment and Public Release
      Deploy apps, make repo public, announce release.
      Week 19–20
      Barton/Dennis
    
  




📝 Phase 1: Setup and Preparation
Goal: Prepare the repository, schema, and tools for Workflow v2.
Tasks






  
    
      Task
      Details
      Files
      Owner
    
  
  
    
      Update YAML schema for Workflow v2
      Add temp_id, status, mapped_tech_id, etc.
      schema/motel_schema.yaml
      Barton
    
    
      Create data directories
      Set up data/unmapped_records/ and data/mapped_records/.
      data/
      Dennis
    
    
      Update tech_list.csv
      Add ontology_iri and oeo_equivalent columns.
      data/technologies/tech_list.csv
      Barton
    
    
      Update process_list.csv
      Add ontology_iri and oeo_equivalent columns.
      data/processes/process_list.csv
      Barton
    
    
      Draft user submission guidelines
      Create docs/user_guide.md.
      docs/user_guide.md
      Dennis
    
    
      Draft reviewer guidelines
      Create docs/reviewer_guide.md.
      docs/reviewer_guide.md
      Barton
    
  




1.1 Updated YAML Schema
File: schema/motel_schema.yaml


# MOTEL Data Schema v2.0
# Updated for Workflow v2: Flexible record collection + later mapping

---
## Main Records (Unmapped or Mapped)
record:
    _type: records
    record_id: Unique identifier for this record (e.g., REC_001)
    temp_id: Temporary ID (used until mapping is complete)
    description: Detailed description of the technology/process
    status: unmapped | mapped | validated
    mapped_tech_id: Foreign key to Technology (assigned in mapping step)
    mapped_process_id: Foreign key to Process (assigned in mapping step)
    mapping_notes: Notes from the mapping review
    mapping_approved_by: Contributor who approved the mapping
    mapping_date: Date when mapping was approved (ISO 8601)
    scope:
        geographic_scope: Foreign key to GeographicScope (e.g., GEO_CH)
        temporal_scope: Foreign key to TemporalScope (e.g., TIME_2025)
        capacity_scope: Foreign key to CapacityScope (e.g., CAP_RESIDENTIAL)
        system_boundary: Foreign key to SystemBoundary (e.g., COND_ISO_BASELOAD)
    sources:
        _item:
            source_id: Foreign key to Source entity
            relevance: primary | secondary | tertiary
    assumptions:
        _item:
            assumption_id: Foreign key to Assumption entity
            relevance: primary | secondary
    values:
        _item:
            attribute_id: Foreign key to Attribute entity (e.g., ATTR_CAPEX)
            value: The actual value (numeric, text, boolean, array, or dict)
            value_type: numeric | text | boolean | array | timeseries | distribution
            unit: Unit of measurement (e.g., USD/kW)
            uncertainty:
                type: range | standard_deviation | confidence_interval | distribution
                min: Minimum value (if type=range or confidence_interval)
                max: Maximum value (if type=range or confidence_interval)
                std: Standard deviation (if type=standard_deviation)
                confidence_level: Confidence level (if type=confidence_interval)
                distribution: Distribution type (e.g., normal)
                params: Distribution parameters (e.g., {mean: 800, std: 50})
            note: Any additional notes

---
## Secondary Datasets
tech:
    _type: secondary
    tech_id: Unique identifier for the technology
    technology_name: Common name of the technology
    ehubx_tech_id: Corresponding ehubX technology ID
    ontology_iri: Corresponding Ontology IRI identifier
    oeo_equivalent: Equivalent OEO term
    process_id: Corresponding process identifier (if applicable)
    is_swiss_specific: boolean

process:
    _type: supplementary
    process_id: Unique identifier for the process
    process_name: Name of the process
    process_description: Brief description of the process
    process_type: conversion | storage | distribution | consumption | other
    ontology_iri: Corresponding Ontology IRI identifier
    oeo_equivalent: Equivalent OEO term
    is_swiss_specific: boolean




1.2 Updated tech_list.csv
File: data/technologies/tech_list.csv


tech_id,technology_name,ehubx_tech_id,ontology_iri,oeo_equivalent,is_swiss_specific,description
T_C_Conv_Solar_PV,Solar PV,SolarPV_Swiss,motel\:T_C_Conv_Solar_PV,oeo\:SolarPV,FALSE,"Photovoltaic technology for electricity generation."
T_C_Conv_Wind_On,Onshore Wind,WindOn_Swiss,motel\:T_C_Conv_Wind_On,oeo\:WindTurbineOnshore,FALSE,"Onshore wind turbines for electricity generation."
T_S_Stor_Battery,Battery Storage,Battery_Swiss,motel\:T_S_Stor_Battery,oeo\:BatteryStorage,FALSE,"Lithium-ion battery storage for electricity."
T_C_Conv_Hydro_Pump,Swiss Hydro Pump,HydroPump_Swiss,motel\:T_C_Conv_Hydro_Pump,,TRUE,"Swiss-specific hydro pump technology for energy storage."




1.3 Updated process_list.csv
File: data/processes/process_list.csv


process_id,process_name,process_type,ontology_iri,oeo_equivalent,is_swiss_specific,description
P_Electricity_Generation,Electricity Generation,conversion,motel\:P_Electricity_Generation,oeo\:ElectricityGeneration,FALSE,"Process of generating electricity."
P_Hydro_Pumping,Hydro Pumping,conversion,motel\:P_Hydro_Pumping,oeo\:PumpedHydroStorage,TRUE,"Process of pumping water for hydropower storage in Switzerland."
P_Charging,Battery Charging,storage,motel\:P_Charging,oeo\:ChargingProcess,FALSE,"Process of charging a battery with electricity."




1.4 User Submission Guidelines
File: docs/user_guide.md


# 📝 User Guide: Submitting Records to MOTEL

Thank you for contributing to the **MOTEL project**! This guide explains how to submit technology or process data to our open database.

## **📌 What to Submit**
Submit a **record** describing a technology or process used in energy systems. Each record should include:
1. **Description**: A clear, detailed description of the technology/process.
   - Example: *"A photovoltaic system that converts sunlight into electricity, commonly used in Swiss residential buildings with a typical efficiency of 18%."*
2. **Scope**: The context in which the data applies.
   - **Geographic Scope**: Where is this technology/process used? (e.g., Switzerland, EU, Global)
   - **Temporal Scope**: When does this data apply? (e.g., 2025, 2025–2030)
   - **Capacity Scope**: What scale/capacity range? (e.g., residential, utility-scale, 1–10 MW)
   - **System Boundary**: Operating conditions (e.g., isolated system, grid-connected).
3. **Sources**: Where did this data come from?
   - Provide **source documents, databases, or reports** (e.g., NREL ATB 2023, JASM).
   - Include **links or DOIs** if available.
4. **Assumptions**: What assumptions were made?
   - Example: *"Efficiency assumed to be 18% based on typical Swiss installations."*
5. **Values**: Technology/process parameters (e.g., CAPEX, efficiency, lifetime).
   - Include **units** and **uncertainty** (e.g., min/max, standard deviation).

## **📥 How to Submit**
### Option 1: Web Form (Recommended)
1. Go to the [MOTEL Submission Form](https://motel-db.streamlit.app/submit).
2. Fill in the fields:
   - **Description**: Write a clear description.
   - **Scope**: Select geographic, temporal, and capacity scopes.
   - **Sources**: Add source details (name, type, link, etc.).
   - **Assumptions**: List any assumptions.
   - **Values**: Add parameter values (e.g., CAPEX = 800 USD/kW).
3. Click **Submit**. Your record will be assigned a `temp_id` and stored as **unmapped**.

### Option 2: YAML File (Advanced)
1. Create a YAML file following the [MOTEL Schema v2.0](../schema/motel_schema.yaml).
   Example:
   ```yaml
   record:
       record_id: REC_001
       temp_id: TEMP_001
       description: "A photovoltaic system that converts sunlight into electricity..."
       scope:
           geographic_scope: GEO_CH
           temporal_scope: TIME_2025_2030
           capacity_scope: CAP_RESIDENTIAL
       sources:
           - source_id: SRC_USER_001
             source_description: "User submission via web form"
             source_type: user_submission
       assumptions:
           - assumption_id: ASSUMP_001
             assumption_description: "Efficiency assumed to be 18%."
       values:
           - attribute_id: ATTR_CAPEX
             value: 800
             value_type: numeric
             unit: USD/kW
             uncertainty:
                 type: range
                 min: 700
                 max: 900
       status: unmapped




Save the file as REC_XXX.yaml (where XXX is a unique number).
Submit a Pull Request to the motel-db/unmapped_records directory.
🔍 What Happens Next?

Automated Mapping: Our system will suggest a tech_id and process_id based on your description.
Manual Review: A domain expert (e.g., Barton or Dennis) will validate the mapping.
Notification: You’ll receive an email or GitHub notification with the final tech_id/process_id.
Publication: Your record will be published in the MOTEL database with full traceability.
💡 Tips for High-Quality Submissions

Be specific: Include technology type, fuel, capacity range, and location in the description.
Cite sources: Provide links, DOIs, or PDF backups for all data.
Include uncertainty: Specify ranges, standard deviations, or confidence intervals where possible.
Check for duplicates: Search the MOTEL Database to avoid submitting existing technologies.
🆘 Need Help?

Questions? Open a GitHub Discussion.
Bugs? Open a GitHub Issue.
Contact: Email barton.chen@empa.ch.


---

### **1.5 Reviewer Guidelines**
**File**: `docs/reviewer_guide.md`
```markdown
# 👨‍🔬 Reviewer Guide: Validating MOTEL Record Mappings

As a **reviewer**, your role is to **validate the automated mappings** of submitted records to `tech_id` and `process_id`. This ensures the **quality and consistency** of the MOTEL database.

## **📌 Workflow Overview**
1. **Automated Mapping**: The system suggests a `tech_id` and `process_id` for each unmapped record.
2. **Your Task**: Review the suggestion and **approve, reject, or request changes**.
3. **Finalization**: Approved mappings are added to the database and linked to ontologies.

## **🔧 Tools**
- **Reviewer Dashboard**: [MOTEL Reviewer Tool](https://motel-db-reviewer.streamlit.app) (Streamlit app).
- **Ontology Browser**: [Protégé](https://protege.stanford.edu/) (for exploring OEO/MOTEL ontologies).
- **Data Explorer**: [MOTEL Database](https://motel-db.streamlit.app/explore) (to check existing records).

## **📝 Review Process**
### Step 1: Access Unmapped Records
1. Open the [Reviewer Dashboard](https://motel-db-reviewer.streamlit.app).
2. Select an **unmapped record** from the list.

### Step 2: Review the Record
For each record, check:
| **Field** | **What to Verify** | **Example** |
|-----------|--------------------|-------------|
| **Description** | Is the description **clear and specific**? Does it match the suggested `tech_id`? | ✅ "5 kW rooftop PV in Switzerland" → `T_C_Conv_Solar_PV` |
| **Scope** | Does the scope (geographic, temporal, etc.) match the `tech_id`? | ✅ `GEO_CH` + `T_C_Conv_Solar_PV` (Swiss Solar PV) |
| **Sources** | Are the sources **credible and relevant**? | ✅ NREL ATB 2023 is a valid source for Solar PV. |
| **Values** | Are the values (e.g., CAPEX, efficiency) **realistic** for the suggested `tech_id`? | ✅ CAPEX = 800 USD/kW for Solar PV. |
| **Automated Suggestion** | Does the suggested `tech_id`/`process_id` **match the description**? | ✅ "Solar PV" → `T_C_Conv_Solar_PV` |
| **OEO Alignment** | Does the `tech_id` have a **valid OEO equivalent**? | ✅ `T_C_Conv_Solar_PV` → `oeo:SolarPV` |

### Step 3: Decide on the Mapping
| **Decision** | **Action** | **When to Use** |
|--------------|------------|-----------------|
| **Approve** | Click **Approve** and assign the `tech_id`/`process_id`. | The suggestion is **correct and complete**. |
| **Reject** | Click **Reject** and provide a reason. | The suggestion is **incorrect**. |
| **Request Changes** | Click **Request Changes** and ask the user for **clarification**. | The description is **unclear or incomplete**. |
| **Manual Override** | Override the suggestion and **manually assign** a `tech_id`/`process_id`. | The suggestion is **close but not perfect**. |

### Step 4: Add Ontology Links (Optional)
If the `tech_id` or `process_id` is **not already linked to an ontology term** (e.g., OEO):
1. Open `ontology/motel.ttl` in [Protégé](https://protege.stanford.edu/).
2. Add a link to the **OEO equivalent** (if applicable):
   ```turtle
   motel:T_C_Conv_Solar_PV motel:linkedToOEO oeo:SolarPV .




Commit the changes to the ontology/ directory.
✅ Approval Criteria
A mapping should be approved if:

 The description clearly matches the suggested tech_id/process_id.
 The scope (geographic, temporal, etc.) is consistent with the tech_id.
 The sources are credible and relevant.
 The values (e.g., CAPEX, efficiency) are realistic for the tech_id.
 The tech_id/process_id exists in data/technologies/tech_list.csv or data/processes/process_list.csv.
 The mapping does not create duplicates (check the Data Explorer).
❌ Rejection Criteria
Reject a mapping if:

 The description does not match the suggested tech_id/process_id.
 The scope is inconsistent (e.g., GEO_CH but tech_id is for a global technology).
 The sources are unreliable (e.g., no citation, unclear origin).
 The values are unrealistic (e.g., CAPEX = 10 USD/kW for Solar PV).
 The tech_id/process_id does not exist in the controlled vocabulary.
 The mapping creates a duplicate of an existing record.
📊 Example Reviews
Example 1: Approve
Record:


description: "A 5 kW rooftop photovoltaic system in Switzerland with 18% efficiency."
scope:
    geographic_scope: GEO_CH
    temporal_scope: TIME_2025
values:
    - attribute_id: ATTR_CAPEX
      value: 800
      unit: USD/kW



Suggested Mapping:

tech_id: T_C_Conv_Solar_PV
process_id: P_Electricity_Generation
Decision: ✅ Approve
Reason: Description and values match Solar PV in Switzerland.

Example 2: Reject
Record:


description: "A system that stores energy using water."
scope:
    geographic_scope: GEO_CH



Suggested Mapping:

tech_id: T_C_Conv_Solar_PV
process_id: P_Electricity_Generation
Decision: ❌ Reject
Reason: Description matches Hydro Pump, not Solar PV.
Correct Mapping: T_C_Conv_Hydro_Pump, P_Hydro_Pumping.

Example 3: Request Changes
Record:


description: "A new type of battery."
scope:
    geographic_scope: GEO_CH



Suggested Mapping:

tech_id: T_S_Stor_Battery
Decision: 🔄 Request Changes
Reason: Description is too vague.
Clarification Request:

"Could you clarify the type of battery (e.g., lithium-ion, flow battery) and its typical use case (e.g., grid-scale, residential)?"


📌 Best Practices

Check OEO First: Before approving, verify that the tech_id has a valid OEO equivalent (if applicable).
Use the Data Explorer: Search for similar records to avoid duplicates.
Document Decisions: Add detailed notes in the mapping_notes field.
Escalate Uncertain Cases: If unsure, tag @barton-chen or @dennis-beermann for review.
Batch Reviews: Review 5–10 records at a time to maintain consistency.

🆘 Need Help?

Questions? Open a GitHub Discussion.
Bugs? Open a GitHub Issue.
Contact: Email barton.chen@empa.ch.


---
---
---

## **📌 Phase 2: User Submission Interface**
**Goal**: Enable users to submit records via a **web form** (Streamlit) or **YAML files** (GitHub).

### **Tasks**
| **Task** | **Details** | **Files** | **Owner** |
|----------|-------------|-----------|-----------|
| Build Streamlit submission form | Create a form for users to submit records. | `tools/streamlit/user_submission.py` | Dennis |
| Add YAML validation | Validate submitted YAML files against schema. | `scripts/mapping/validator.py` | Dennis |
| Store unmapped records | Save submitted records to `data/unmapped_records/`. | `scripts/mapping/save_record.py` | Dennis |
| Assign temporary IDs | Generate `temp_id` for each new record. | `scripts/mapping/generate_temp_id.py` | Dennis |
| Notify users | Send confirmation email/GitHub notification. | `scripts/mapping/notify_user.py` | Dennis |

---

### **2.1 Streamlit Submission Form**
**File**: `tools/streamlit/user_submission.py`
```python
import streamlit as st
import yaml
import pandas as pd
from datetime import datetime
import os
import uuid

@st.cache_data
def load_vocabularies():
    tech_df = pd.read_csv("data/technologies/tech_list.csv")
    process_df = pd.read_csv("data/processes/process_list.csv")
    geographic_df = pd.read_csv("data/controlled_vocab/geographic_scope.csv")
    temporal_df = pd.read_csv("data/controlled_vocab/temporal_scope.csv")
    capacity_df = pd.read_csv("data/controlled_vocab/capacity_scope.csv")
    system_df = pd.read_csv("data/controlled_vocab/system_boundary.csv")
    attribute_df = pd.read_csv("data/controlled_vocab/attribute.csv")
    source_type_df = pd.read_csv("data/controlled_vocab/source_type.csv")
    return {
        "technologies": tech_df,
        "processes": process_df,
        "geographic": geographic_df,
        "temporal": temporal_df,
        "capacity": capacity_df,
        "system": system_df,
        "attributes": attribute_df,
        "source_types": source_type_df,
    }

def main():
    st.set_page_config(page_title="MOTEL: Submit a Record", layout="wide")
    st.title("📝 Submit a New Record to MOTEL")
    st.markdown("Contribute to the **MOTEL project** by submitting a technology or process record.")

    vocabularies = load_vocabularies()

    # Step 1: Description
    st.header("1. Description")
    description = st.text_area(
        "Describe the technology or process in detail:",
        placeholder="Example: A 5 kW rooftop photovoltaic system in Switzerland with 18% efficiency.",
        height=150,
    )

    # Step 2: Scope
    st.header("2. Scope")
    col1, col2 = st.columns(2)
    with col1:
        geographic_scope = st.selectbox("Geographic Scope", options=vocabularies["geographic"]["geographic_scope"].tolist())
        temporal_scope = st.selectbox("Temporal Scope", options=vocabularies["temporal"]["temporal_scope"].tolist())
    with col2:
        capacity_scope = st.selectbox("Capacity Scope", options=vocabularies["capacity"]["capacity_scope"].tolist())
        system_boundary = st.selectbox("System Boundary", options=vocabularies["system"]["system_boundary"].tolist())

    # Step 3: Sources
    st.header("3. Sources")
    source_items = []
    num_sources = st.number_input("Number of sources", min_value=1, value=1)
    for i in range(num_sources):
        with st.expander(f"Source {i+1}"):
            source_description = st.text_input(f"Source Description", key=f"source_desc_{i}")
            source_type = st.selectbox(f"Source Type", options=vocabularies["source_types"]["source_type"].tolist(), key=f"source_type_{i}")
            link = st.text_input(f"Link or DOI", key=f"source_link_{i}")
            access_date = st.date_input(f"Access Date", key=f"source_date_{i}", value=datetime.now())
            source_items.append({
                "source_id": f"SRC_USER_{uuid.uuid4().hex[:8].upper()}",
                "source_description": source_description,
                "source_type": source_type,
                "link": link,
                "access_date": access_date.strftime("%Y-%m-%d"),
            })

    # Step 4: Assumptions
    st.header("4. Assumptions")
    assumption_items = []
    num_assumptions = st.number_input("Number of assumptions", min_value=0, value=0)
    for i in range(num_assumptions):
        with st.expander(f"Assumption {i+1}"):
            assumption_description = st.text_input(f"Assumption Description", key=f"assumption_desc_{i}")
            assumption_items.append({
                "assumption_id": f"ASSUMP_{uuid.uuid4().hex[:8].upper()}",
                "assumption_description": assumption_description,
            })

    # Step 5: Values
    st.header("5. Values")
    value_items = []
    num_values = st.number_input("Number of values", min_value=0, value=0)
    for i in range(num_values):
        with st.expander(f"Value {i+1}"):
            col1, col2 = st.columns(2)
            with col1:
                attribute_id = st.selectbox(f"Attribute", options=vocabularies["attributes"]["attribute_id"].tolist(), key=f"value_attr_{i}")
                value = st.text_input(f"Value", key=f"value_val_{i}")
                unit = st.selectbox(f"Unit", options=vocabularies["attributes"].loc[vocabularies["attributes"]["attribute_id"] == attribute_id, "attribute_unit"].tolist(), key=f"value_unit_{i}")
            with col2:
                value_type = st.selectbox(f"Value Type", options=["numeric", "text", "boolean", "array"], key=f"value_type_{i}")
                uncertainty_type = st.selectbox(f"Uncertainty Type", options=["range", "standard_deviation", "confidence_interval", "none"], key=f"uncertainty_type_{i}")
                if uncertainty_type == "range":
                    min_val = st.number_input("Min", key=f"min_{i}")
                    max_val = st.number_input("Max", key=f"max_{i}")
                    uncertainty = {"type": uncertainty_type, "min": min_val, "max": max_val}
                elif uncertainty_type == "standard_deviation":
                    std_val = st.number_input("Standard Deviation", key=f"std_{i}")
                    uncertainty = {"type": uncertainty_type, "std": std_val}
                elif uncertainty_type == "confidence_interval":
                    min_val = st.number_input("Min", key=f"min_ci_{i}")
                    max_val = st.number_input("Max", key=f"max_ci_{i}")
                    confidence = st.number_input("Confidence Level (0-1)", min_value=0.0, max_value=1.0, key=f"conf_{i}")
                    uncertainty = {"type": uncertainty_type, "min": min_val, "max": max_val, "confidence_level": confidence}
                else:
                    uncertainty = None
                note = st.text_input(f"Note", key=f"note_{i}")
            value_items.append({
                "attribute_id": attribute_id,
                "value": value,
                "value_type": value_type,
                "unit": unit,
                "uncertainty": uncertainty,
                "note": note,
            })

    # Submit button
    if st.button("Submit Record"):
        if not description:
            st.error("Description is required!")
        else:
            record_id = f"REC_{uuid.uuid4().hex[:8].upper()}"
            temp_id = f"TEMP_{uuid.uuid4().hex[:8].upper()}"
            record = {
                "record": {
                    "record_id": record_id,
                    "temp_id": temp_id,
                    "description": description,
                    "status": "unmapped",
                    "scope": {
                        "geographic_scope": geographic_scope,
                        "temporal_scope": temporal_scope,
                        "capacity_scope": capacity_scope,
                        "system_boundary": system_boundary,
                    },
                    "sources": source_items,
                    "assumptions": assumption_items,
                    "values": value_items,
                }
            }
            os.makedirs("data/unmapped_records", exist_ok=True)
            filename = f"data/unmapped_records/{record_id}.yaml"
            with open(filename, "w") as f:
                yaml.dump(record, f, sort_keys=False)
            st.success(f"✅ Record submitted successfully! Your record ID is **{record_id}** and temp ID is **{temp_id**}.")
            st.markdown(f"[View your record here](https://github.com/empa-uesl/motel-db/blob/main/{filename})")

if __name__ == "__main__":
    main()




📌 Phase 3: Automated Mapping
Goal: Automate the suggestion of tech_id and process_id for unmapped records.
Tasks






  
    
      Task
      Details
      Files
      Owner
    
  
  
    
      Develop NLP matching
      Use NLP to compare descriptions to existing tech_id definitions.
      scripts/mapping/auto_mapper.py
      Barton
    
    
      Develop ontology matching
      Link descriptions to OEO/MOTEL ontology terms.
      scripts/mapping/ontology_mapper.py
      Barton
    
    
      Combine matching results
      Merge NLP and ontology results.
      scripts/mapping/combined_mapper.py
      Barton
    
    
      Deduplication
      Detect and flag duplicate records.
      scripts/mapping/deduplicator.py
      Barton
    
    
      Store mapping suggestions
      Save suggestions to CSV for review.
      data/mapping_suggestions.csv
      Barton
    
  




3.1 NLP Matching
File: scripts/mapping/auto_mapper.py


import spacy
import pandas as pd
from pathlib import Path
import yaml

nlp = spacy.load("en_core_web_md")

def load_tech_process_data():
    tech_df = pd.read_csv("data/technologies/tech_list.csv")
    process_df = pd.read_csv("data/processes/process_list.csv")
    return tech_df, process_df

def preprocess_text(text):
    if not text:
        return ""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def nlp_match(description, tech_df, process_df, top_n=3):
    desc_processed = preprocess_text(description)
    tech_df["processed_name"] = tech_df["technology_name"].apply(preprocess_text)
    process_df["processed_name"] = process_df["process_name"].apply(preprocess_text)

    tech_df["similarity"] = tech_df["processed_name"].apply(
        lambda x: nlp(desc_processed).similarity(nlp(x)) if x else 0
    )
    process_df["similarity"] = process_df["processed_name"].apply(
        lambda x: nlp(desc_processed).similarity(nlp(x)) if x else 0
    )

    top_techs = tech_df.nlargest(top_n, "similarity")[["tech_id", "technology_name", "similarity"]].to_dict("records")
    top_processes = process_df.nlargest(top_n, "similarity")[["process_id", "process_name", "similarity"]].to_dict("records")

    return {"technologies": top_techs, "processes": top_processes}

def match_record(yaml_file):
    with open(yaml_file, "r") as f:
        record = yaml.safe_load(f)
    description = record["record"]["description"]
    tech_df, process_df = load_tech_process_data()
    matches = nlp_match(description, tech_df, process_df)
    return {"record_id": record["record"]["record_id"], "matches": matches}

if __name__ == "__main__":
    result = match_record("data/unmapped_records/REC_001.yaml")
    print(result)




3.2 Ontology Matching
File: scripts/mapping/ontology_mapper.py


from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS
import yaml
import re

def load_ontology():
    g = Graph()
    g.parse("ontology/motel.ttl", format="turtle")
    return g

def extract_keywords(description):
    words = re.findall(r'\b\w+\b', description.lower())
    return set(words)

def ontology_match(description, g):
    keywords = extract_keywords(description)
    matches = []
    for s, p, o in g:
        if p == RDFS.label:
            label = str(o).lower()
            if any(keyword in label for keyword in keywords):
                matches.append({
                    "uri": str(s),
                    "label": label,
                    "type": "class" if (s, RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class")) in g else "individual",
                })
    return matches

def match_record_to_ontology(yaml_file):
    with open(yaml_file, "r") as f:
        record = yaml.safe_load(f)
    description = record["record"]["description"]
    g = load_ontology()
    matches = ontology_match(description, g)
    return {"record_id": record["record"]["record_id"], "ontology_matches": matches}

if __name__ == "__main__":
    result = match_record_to_ontology("data/unmapped_records/REC_001.yaml")
    print(result)




📌 Phase 4: Manual Review Interface
Goal: Build a Streamlit dashboard for reviewers to validate mapping suggestions.
Tasks






  
    
      Task
      Details
      Files
      Owner
    
  
  
    
      Build reviewer dashboard
      Create a Streamlit app for validating mappings.
      tools/streamlit/reviewer_dashboard.py
      Dennis
    
    
      Load mapping suggestions
      Display suggestions from data/mapping_suggestions.csv.
      data/mapping_suggestions.csv
      Dennis
    
    
      Add approval workflow
      Allow reviewers to approve/reject suggestions.
      scripts/mapping/update_mapping.py
      Dennis
    
    
      Update mapped records
      Move approved records to data/mapped_records/.
      scripts/mapping/move_record.py
      Dennis
    
    
      Notify users
      Send notifications when records are mapped.
      scripts/mapping/notify_user.py
      Dennis
    
  




4.1 Reviewer Dashboard
File: tools/streamlit/reviewer_dashboard.py


import streamlit as st
import pandas as pd
import yaml
import os
from datetime import datetime
from pathlib import Path

@st.cache_data
def load_data():
    suggestions_df = pd.read_csv("data/mapping_suggestions.csv")
    unmapped_records = []
    for yaml_file in Path("data/unmapped_records").glob("*.yaml"):
        with open(yaml_file, "r") as f:
            record = yaml.safe_load(f)
        unmapped_records.append(record)
    return suggestions_df, unmapped_records

def get_record_by_id(record_id, unmapped_records):
    for record in unmapped_records:
        if record["record"]["record_id"] == record_id:
            return record
    return None

def update_mapping(record_id, tech_id, process_id, reviewer, notes):
    record_file = f"data/unmapped_records/{record_id}.yaml"
    with open(record_file, "r") as f:
        record = yaml.safe_load(f)
    record["record"]["status"] = "mapped"
    record["record"]["mapped_tech_id"] = tech_id
    record["record"]["mapped_process_id"] = process_id
    record["record"]["mapping_approved_by"] = reviewer
    record["record"]["mapping_date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    record["record"]["mapping_notes"] = notes
    os.makedirs("data/mapped_records", exist_ok=True)
    mapped_file = f"data/mapped_records/{record_id}.yaml"
    with open(mapped_file, "w") as f:
        yaml.dump(record, f, sort_keys=False)
    os.remove(record_file)
    suggestions_df = pd.read_csv("data/mapping_suggestions.csv")
    suggestions_df = suggestions_df[suggestions_df["record_id"] != record_id]
    suggestions_df.to_csv("data/mapping_suggestions.csv", index=False)
    return mapped_file

def main():
    st.set_page_config(page_title="MOTEL: Review Mappings", layout="wide")
    st.title("🔍 Review Mapping Suggestions")
    suggestions_df, unmapped_records = load_data()
    record_ids = suggestions_df["record_id"].unique()
    selected_record_id = st.selectbox("Select a record to review:", record_ids)

    if selected_record_id:
        record = get_record_by_id(selected_record_id, unmapped_records)
        if record:
            st.subheader(f"Record: {selected_record_id}")
            st.markdown(f"**Description**: {record['record']['description']}")
            st.markdown(f"**Scope**: {record['record']['scope']}")
            st.markdown(f"**Submission Date**: {record['record'].get('submission_date', 'N/A')}")

            with st.expander("Sources"):
                for source in record["record"]["sources"]:
                    st.markdown(f"- {source['source_description']} ({source['source_type']})")

            with st.expander("Assumptions"):
                for assumption in record["record"]["assumptions"]:
                    st.markdown(f"- {assumption['assumption_description']}")

            with st.expander("Values"):
                for value in record["record"]["values"]:
                    st.markdown(f"- **{value['attribute_id']}**: {value['value']} {value.get('unit', '')}")

            st.subheader("🤖 Mapping Suggestions")
            record_suggestions = suggestions_df[suggestions_df["record_id"] == selected_record_id]
            tech_suggestions = record_suggestions[record_suggestions["suggestion_type"] == "technology"]
            process_suggestions = record_suggestions[record_suggestions["suggestion_type"] == "process"]

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Technology Suggestions")
                if not tech_suggestions.empty:
                    for _, row in tech_suggestions.iterrows():
                        st.markdown(f"- **{row['suggestion_name']}** (`{row['suggestion_id']}`) (Score: {row['nlp_score']:.2f}) [OEO: {row['oeo_equivalent']}]")
                else:
                    st.markdown("No technology suggestions.")
            with col2:
                st.markdown("#### Process Suggestions")
                if not process_suggestions.empty:
                    for _, row in process_suggestions.iterrows():
                        st.markdown(f"- **{row['suggestion_name']}** (`{row['suggestion_id']}`) (Score: {row['nlp_score']:.2f}) [OEO: {row['oeo_equivalent']}]")
                else:
                    st.markdown("No process suggestions.")

            st.subheader("✏️ Manual Override")
            all_techs = pd.read_csv("data/technologies/tech_list.csv")["tech_id"].tolist()
            all_processes = pd.read_csv("data/processes/process_list.csv")["process_id"].tolist()
            col1, col2 = st.columns(2)
            with col1:
                tech_id = st.selectbox("Override Technology ID", options=[""] + all_techs, index=0)
            with col2:
                process_id = st.selectbox("Override Process ID", options=[""] + all_processes, index=0)
            mapping_notes = st.text_area("Mapping Notes", placeholder="Example: Matched to Solar PV despite low NLP score due to expert knowledge.")

            st.subheader("✅ Decision")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Approve Suggestions"):
                    top_tech = tech_suggestions.iloc[0]["suggestion_id"] if not tech_suggestions.empty else tech_id
                    top_process = process_suggestions.iloc[0]["suggestion_id"] if not process_suggestions.empty else process_id
                    if not top_tech and not top_process:
                        st.error("No suggestions to approve! Use manual override.")
                    else:
                        reviewer = "reviewer@example.com"  # Replace with actual reviewer email
                        mapped_file = update_mapping(selected_record_id, top_tech or tech_id, top_process or process_id, reviewer, mapping_notes)
                        st.success(f"✅ Record {selected_record_id} mapped to tech_id={top_tech or tech_id}, process_id={top_process or process_id}.")
            with col2:
                if st.button("👎 Reject Suggestions"):
                    reason = st.text_area("Reason for Rejection", placeholder="Example: Description matches Hydro Pump, not Solar PV.", key=f"reject_reason_{selected_record_id}")
                    if reason:
                        st.success(f"Rejection noted. Reason: {reason}")
            with col3:
                if st.button("🔄 Request Changes"):
                    request = st.text_area("Clarification Request", placeholder="Example: Please specify the battery type.", key=f"request_changes_{selected_record_id}")
                    if request:
                        st.success(f"Clarification requested: {request}")

if __name__ == "__main__":
    main()




📌 Phase 5: Ontology Integration
Goal: Link mapped records to OEO/MOTEL ontology terms.
Tasks






  
    
      Task
      Details
      Files
      Owner
    
  
  
    
      Update ontology with new terms
      Add new tech_id/process_id to ontology/motel.ttl.
      ontology/motel.ttl
      Barton
    
    
      Link records to ontology
      Add ontology_iri to mapped records.
      scripts/mapping/link_to_ontology.py
      Barton
    
    
      Validate ontology
      Check for inconsistencies in motel.ttl.
      scripts/mapping/validate_ontology.py
      Barton
    
    
      Publish ontology
      Host ontology on GitHub/GraphDB.
      ontology/README.md
      Barton
    
  




5.1 Example Ontology (ontology/motel.ttl)


@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix oeo: <https://openenergyplatform.org/ontology/oeo/> .
@prefix motel: <https://empa.ch/motel/> .
@prefix geo: <http://www.geonames.org/ontology#> .

motel: a owl\:Ontology ;
    rdfs\:label "MOTEL Ontology" ;
    rdfs\:comment "Ontology for the MOTEL project, extending Open Energy Ontology." ;
    owl\:imports oeo: .

motel\:Technology a owl\:Class ;
    rdfs\:subClassOf oeo\:Technology ;
    rdfs\:label "MOTEL Technology" .

motel\:Process a owl\:Class ;
    rdfs\:subClassOf oeo\:Process ;
    rdfs\:label "MOTEL Process" .

motel\:T_C_Conv_Solar_PV a motel\:Technology ;
    rdfs\:label "Solar PV" ;
    rdfs\:comment "Photovoltaic technology for electricity generation." ;
    motel\:linkedToOEO oeo\:SolarPV ;
    motel\:hasEnergyCarrierOut oeo\:Electricity ;
    geo\:locatedIn geo\:CH .

motel\:P_Electricity_Generation a motel\:Process ;
    rdfs\:label "Electricity Generation" ;
    rdfs\:comment "Process of generating electricity." ;
    motel\:linkedToOEO oeo\:ElectricityGeneration .




📌 Phase 6: Testing and Validation
Goal: Test the workflow end-to-end and validate the database.
Tasks






  
    
      Task
      Details
      Owner
    
  
  
    
      Test user submission
      Submit 5–10 test records via the Streamlit form.
      Dennis
    
    
      Test automated mapping
      Run mapping scripts on test records.
      Barton
    
    
      Test manual review
      Validate mappings in the reviewer dashboard.
      Dennis
    
    
      Test ontology integration
      Link test records to ontology terms.
      Barton
    
    
      Validate full workflow
      Ensure records move from unmapped → mapped → ontology-linked.
      Barton/Dennis
    
    
      Performance testing
      Test with 100+ records.
      Barton
    
  




📌 Phase 7: Deployment and Public Release
Goal: Deploy the workflow and make the database public.
Tasks






  
    
      Task
      Details
      Files
      Owner
    
  
  
    
      Deploy Streamlit apps
      Host user submission and reviewer dashboard on Streamlit Cloud.
      Streamlit Cloud
      Dennis
    
    
      Deploy FastAPI backend
      Host the backend API (optional).
      Heroku/Render
      Barton
    
    
      Make repo public
      Change repository visibility to public.
      GitHub Settings
      Barton
    
    
      Announce public release
      Notify stakeholders (ETH, SWEET CoSi, etc.).
      Email/Slack
      Barton
    
    
      Monitor and iterate
      Collect feedback and improve the workflow.
      GitHub Issues
      Barton/Dennis
    
  




📅 Timeline and Milestones






  
    
      Phase
      Tasks
      Timeline
      Owner
    
  
  
    
      Phase 1: Setup and Preparation
      Update schema, create directories, draft guidelines.
      Week 1–2
      Barton/Dennis
    
    
      Phase 2: User Submission Interface
      Build Streamlit form, YAML validator, temp ID generator.
      Week 3–5
      Dennis
    
    
      Phase 3: Automated Mapping
      Develop NLP/ontology matching, deduplication, suggestions.
      Week 6–9
      Barton
    
    
      Phase 4: Manual Review Interface
      Build reviewer dashboard, approval workflow.
      Week 10–12
      Dennis
    
    
      Phase 5: Ontology Integration
      Update ontology, link records, validate.
      Week 13–15
      Barton
    
    
      Phase 6: Testing and Validation
      Test end-to-end workflow, validate database.
      Week 16–18
      Barton/Dennis
    
    
      Phase 7: Deployment and Public Release
      Deploy apps, make repo public, announce release.
      Week 19–20
      Barton/Dennis
    
  




📊 Success Metrics






  
    
      Metric
      Target
      Measurement Method
    
  
  
    
      Number of user submissions
      50+ records/month
      GitHub commits to data/unmapped_records/
    
    
      Mapping accuracy
      >90% correct suggestions
      Manual review of sample mappings
    
    
      Reviewer throughput
      20 records/hour
      Time spent in reviewer dashboard
    
    
      Ontology coverage
      >80% of records linked to OEO
      Check ontology_iri in mapped records
    
    
      User satisfaction
      >4/5 rating
      Survey users after submission
    
    
      Duplicate rate
      <5%
      data/duplicate_records.csv
    
    
      Time to map
      <24 hours
      Timestamp from submission to mapping
    
  




✅ Checklist for Execution


 Phase 1: Setup and Preparation

 Update motel_schema.yaml for Workflow v2.
 Create data/unmapped_records/ and data/mapped_records/ directories.
 Update tech_list.csv and process_list.csv with ontology_iri and oeo_equivalent.
 Draft docs/user_guide.md and docs/reviewer_guide.md.


 Phase 2: User Submission Interface

 Build tools/streamlit/user_submission.py.
 Create scripts/mapping/validator.py.
 Create scripts/mapping/save_record.py.
 Create scripts/mapping/generate_temp_id.py.
 Create scripts/mapping/notify_user.py.
 Test submission form with 5–10 records.


 Phase 3: Automated Mapping

 Build scripts/mapping/auto_mapper.py.
 Build scripts/mapping/ontology_mapper.py.
 Build scripts/mapping/combined_mapper.py.
 Build scripts/mapping/deduplicator.py.
 Test mapping on 5–10 records.


 Phase 4: Manual Review Interface

 Build tools/streamlit/reviewer_dashboard.py.
 Create scripts/mapping/update_mapping.py.
 Create scripts/mapping/move_record.py.
 Test reviewer dashboard with 5–10 records.


 Phase 5: Ontology Integration

 Update ontology/motel.ttl with new terms.
 Create scripts/mapping/link_to_ontology.py.
 Create scripts/mapping/validate_ontology.py.
 Add ontology/README.md.
 Link 5–10 test records to ontology.


 Phase 6: Testing and Validation

 Test user submission with 5–10 records.
 Test automated mapping on test records.
 Test manual review in the dashboard.
 Test ontology integration.
 Validate full workflow end-to-end.
 Performance test with 100+ records.


 Phase 7: Deployment and Public Release

 Deploy Streamlit apps to Streamlit Cloud.
 Deploy FastAPI backend (optional).
 Make repository public.
 Announce public release to stakeholders.
 Monitor and iterate based on feedback.


🔗 References

MOTEL Project Proposal
ETH Domain ORD Program
Open Energy Ontology (OEO)
Streamlit Documentation
RDFLib Documentation
GitHub Actions Documentation
