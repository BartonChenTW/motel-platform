# author: Barton Chen
# Date: 2026-06-21
# This script contains helper functions for the Refuel ingestion pipeline, including data cleaning, 
# parsing, and transformation utilities.


import math
import re
from collections import defaultdict
import pandas as pd

## --- supportive functions

def is_nan(value):
    """Checks if a value is None or NaN."""
    return value is None or (
        isinstance(value, float) and math.isnan(value)
    )

def clean(value):
    """Returns None if the value is NaN, otherwise returns the original value."""
    return None if is_nan(value) else value

def split_csv(value):
    if is_nan(value):
        return []
    return [
        x.strip()
        for x in str(value).split(",")
        if x.strip() and x.strip().lower() not in {"na", "nan"}
    ]

def split_csv_float(value):
    out = []
    for token in split_csv(value):
        try:
            out.append(float(token))
        except ValueError:
            out.append(None)
    return out

def normalize_unit(unit_text):
    if is_nan(unit_text):
        return None
    unit = str(unit_text).strip()
    if not unit or unit == "-":
        return None
    return unit

def prepare_df(df_raw):
    """Normalize ConvTech table where row 1 contains machine-friendly headers."""
    df = df_raw.copy()
    header_idx = 1
    df.columns = [str(c).strip() for c in df.loc[header_idx]]
    df = df.loc[header_idx + 1:].reset_index(drop=True)

    # Remove section/header-like rows
    if "tech_id" in df.columns:
        df = df[df["tech_id"].notna()]
        df = df[df["tech_id"].astype(str).str.strip().str.lower() != "nan"]
        df = df[df["tech_id"].astype(str).str.strip().str.lower() != "tech_id"]
    if "unit_operation" in df.columns:
        df = df[df["unit_operation"].notna()]

    return df.reset_index(drop=True)



## --- functions to get sources/references

def get_src_attrs(source_text):
    if not source_text or not source_text.strip():
        return []

    # Collect: source_id -> set of linked attributes
    source_to_attrs: dict[str, set] = defaultdict(set)

    # Split on ";" to get individual attribute-group : source(s) segments
    segments = re.split(r";", source_text)

    for segment in segments:
        segment = segment.strip().rstrip(";").strip()
        if not segment:
            continue

        # Split on ":" — left side = quoted attribute names, right side = source IDs
        parts = segment.split(":", 1)
        if len(parts) != 2:
            continue

        attrs_part, sources_part = parts[0].strip(), parts[1].strip()

        # Extract attribute names (quoted strings)
        attributes = re.findall(r'"([^"]+)"', attrs_part)
        attributes = [a.strip() for a in attributes if a.strip()]

        # Extract source IDs (comma-separated, unquoted identifiers)
        # Remove any trailing punctuation or whitespace
        raw_sources = [s.strip().strip('"').strip() for s in sources_part.split(",")]
        source_ids = [s for s in raw_sources if s and s.lower() != "missing"]

        for source_id in source_ids:
            source_to_attrs[source_id].update(attributes)
    
    return source_to_attrs

def parse_source_text(source_text: str, df_ref: pd.DataFrame) -> list[dict]:
    """
    Parse a raw source_text string of the form:
        "attr1", "attr2": source_id_A; "attr3": source_id_B, source_id_C;
    
    Returns a list of source dicts following the unmapped_record schema:
        [
            {
                "source_description": "source_id_A",
                "source_type": "other",
                "link": "",
                "linked_attribute": ["attr1", "attr2"]
            },
            ...
        ]
    
    Notes:
    - A single attribute can be linked to multiple source IDs (comma-separated after the colon).
    - Duplicate source IDs across segments are merged: their linked_attributes are unioned.
    - Source IDs equal to "missing" are skipped.
    """
    
    source_to_attrs = get_src_attrs(source_text)

    # Build the sources array
    sources = []
    for source_id, linked_attrs in source_to_attrs.items():
        # src_name = map_src_id.get(source_id, '')
        src_name = source_id  # Use source_id directly if no mapping is provided

        ## get source data from `ds_src`
        df = df_ref[df_ref['source_id']==src_name]
        if len(df) == 0:
            print(f'Cannot find source_id "{source_id}" in source dataset')
        elif len(df) > 1:
            print(f'Multiple entries found for source_id "{source_id}" in source dataset; using the first match.')
        else:
            di_src = df.iloc[0].to_dict()

            # new schema does not include source_type and link
            sources.append({
                "source_name": di_src['source_id'],
                "source_description": di_src['description'],
                "linked_attribute": sorted(linked_attrs),
            })

    return sources

def add_sources_to_record(record: dict, source_text: str, df_ref: pd.DataFrame) -> dict:
    """
    Parse source_text and inject a 'sources' key into the record.

    Args:
        record:      The unmapped_record dict (modified in-place and returned).
        source_text: Raw string from row.get("list_of_source_id").
        df_ref:       A pandas DataFrame containing source information.

    Returns:
        The same record dict with 'sources' populated.
    """
    if source_text == source_text:      # skip if source_text is NaN
        record["sources"] = parse_source_text(source_text, df_ref)
    return record



## --- functions to get attributes

def get_attr_note(row: pd.Series) -> str:
    """
    Extracts the note for a given attribute from a DataFrame row.

    Args:
        row: A pandas Series representing a row from the ConvTech DataFrame.
        attr_name: The name of the attribute to extract the note for.    
        
    Returns:
        The note string for the attribute, or None if not found.
    """
    s = str(row.to_dict())
    s = s.replace("{", "").replace("}", "").replace("'", "")

    return s


def add_attributes_to_record(ue: dict, row: pd.Series, df_attr: pd.DataFrame) -> dict:
    """
    Extracts attribute-related fields from a DataFrame row and adds them to the unmapped_record.

    Args:
        ue:  The unmapped_record dict (modified in-place and returned).
        row: A pandas Series representing a row from the ConvTech DataFrame.
        df_attr: A pandas DataFrame containing attribute information.
    Returns:
        The same unmapped_record dict with 'attributes' populated.
    """
    attributes = []

    for attr in df_attr.index:
        if attr not in row.keys():
            continue  # Skip if the attribute is not present in the row

        if is_nan(row[attr]):
            continue  # Skip if the attribute value is NaN

        attr = {
            'attribute_name': attr,
            'value': clean(row[attr]),
            'uncertainty_notes': None,
            'time_index': clean(row.get('tech_year', None)),
            'notes': get_attr_note(df_attr.loc[attr])
        }
        attributes.append(attr)

    ue["attributes"] = attributes
    return ue



## --- functions to get balancing

def build_balancing_entries(carriers, shares, units):
    size = max(len(carriers), len(shares), len(units))
    entries = []

    for i in range(size):
        carrier = carriers[i] if i < len(carriers) else None
        share = shares[i] if i < len(shares) else None
        unit = units[i] if i < len(units) else None

        if carrier is None and share is None and unit is None:
            continue

        entries.append({
            "carrier": carrier,
            "share": share,
            "unit": unit,
        })

    return entries

def to_balance_list(items):
    """Normalize balancing items to list of dicts with carrier_name/share/unit."""
    normalized = []
    for item in items or []:
        if not isinstance(item, dict):
            continue

        carrier_name = clean(item.get("carrier_name"))
        if carrier_name is None:
            carrier_name = clean(item.get("carrier"))

        share = clean(item.get("share"))
        unit = clean(item.get("unit"))

        if carrier_name is None and share is None and unit is None:
            continue

        normalized.append({
            "carrier_name": carrier_name,
            "share": share,
            "unit": unit,
        })

    return normalized


def infer_main_output_unit(main_output_carrier, output_carriers, output_units):
    """Infer the unit for the selected main output carrier."""
    if main_output_carrier is not None:
        for carrier, unit in zip(output_carriers, output_units):
            if clean(carrier) == main_output_carrier:
                unit_norm = normalize_unit(unit)
                if unit_norm:
                    return unit_norm
                

def add_balancing_to_record(ue: dict, row: pd.Series) -> dict:
    """
    Extracts balancing-related fields from a DataFrame row and adds them to the unmapped_record.

    Args:
        ue:  The unmapped_record dict (modified in-place and returned).
        row: A pandas Series representing a row from the ConvTech DataFrame.
    Returns:
        The same unmapped_record dict with 'balancing' populated.
    """

    input_carriers = split_csv(row.get("carriers_in"))
    input_shares = split_csv_float(row.get("ratios_in"))
    input_units = split_csv(row.get("units_in_ratios"))

    output_carriers = split_csv(row.get("carriers_out"))
    output_shares = split_csv_float(row.get("ratios_out"))
    output_units = split_csv(row.get("units_out_ratios"))

    ue["balancing"] = {}

    ue["balancing"]["inputs"] = to_balance_list(
        build_balancing_entries(
            input_carriers,
            input_shares,
            input_units,
        )
    )
    ue["balancing"]["outputs"] = to_balance_list(
        build_balancing_entries(
            output_carriers,
            output_shares,
            output_units,
        )
    )

    main_output_carrier = clean(row.get("main_output")) #!
    main_output_unit = infer_main_output_unit(
        main_output_carrier,
        output_carriers,
        output_units,
    )

    return ue