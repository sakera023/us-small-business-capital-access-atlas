"""Geographic cleaning and state-level aggregation helpers."""

from __future__ import annotations

import re

import pandas as pd

US_STATE_NAMES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

STATE_NAME_TO_ABBR = {name.lower(): abbr for abbr, name in US_STATE_NAMES.items()}
STATE_NAME_TO_ABBR.update(
    {
        "washington dc": "DC",
        "washington, dc": "DC",
        "district of columbia": "DC",
    }
)


def normalize_state_abbreviation(value: object) -> str | None:
    """Normalize a U.S. state name or two-letter abbreviation."""
    if pd.isna(value):
        return None

    text = str(value).strip()
    if not text:
        return None

    upper = text.upper()
    if upper in US_STATE_NAMES:
        return upper

    normalized = re.sub(r"\s+", " ", text.lower()).strip(" .")
    return STATE_NAME_TO_ABBR.get(normalized)


def coerce_numeric_series(series: pd.Series) -> pd.Series:
    """Convert common spreadsheet numeric formats to floats."""
    text = series.astype(str).str.strip()
    text = text.str.replace(",", "", regex=False)
    text = text.str.replace("$", "", regex=False)
    text = text.str.replace("%", "", regex=False)
    text = text.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    text = text.replace(
        {
            "nan": None,
            "None": None,
            "": None,
            "—": None,
            "-": None,
            "N/A": None,
            "NA": None,
        }
    )
    return pd.to_numeric(text, errors="coerce")


def detect_state_column(frame: pd.DataFrame) -> str | None:
    """Identify the column most likely to contain state names or abbreviations."""
    if frame.empty:
        return None

    best_column: str | None = None
    best_score = 0.0

    for column in frame.columns:
        series = frame[column].dropna().head(250)
        if len(series) < 3:
            continue

        recognized_share = float(
            series.map(normalize_state_abbreviation).notna().mean()
        )
        hint = str(column).strip().lower()
        if "state" in hint:
            recognized_share += 0.20

        if recognized_share > best_score:
            best_score = recognized_share
            best_column = str(column)

    return best_column if best_score >= 0.45 else None


def numeric_metric_columns(
    frame: pd.DataFrame,
    state_column: str | None = None,
) -> list[str]:
    """Return columns with enough numeric values for state-level analysis."""
    resolved_state_column = state_column or detect_state_column(frame)
    options: list[str] = []

    for column in frame.columns:
        column_name = str(column)
        if column_name == resolved_state_column:
            continue

        numeric = coerce_numeric_series(frame[column])
        if int(numeric.notna().sum()) >= 3:
            options.append(column_name)

    return options


def prepare_state_metric(
    frame: pd.DataFrame,
    metric_column: str,
    state_column: str | None = None,
) -> pd.DataFrame:
    """Prepare a clean one-row-per-state metric table."""
    resolved_state_column = state_column or detect_state_column(frame)
    if resolved_state_column is None:
        raise ValueError("No U.S. state column could be detected in this worksheet.")
    if metric_column not in frame.columns:
        raise ValueError(f"Unknown metric column: {metric_column}")

    mapped = pd.DataFrame(
        {
            "state": frame[resolved_state_column].map(normalize_state_abbreviation),
            "value": coerce_numeric_series(frame[metric_column]),
        }
    ).dropna(subset=["state", "value"])

    if mapped.empty:
        raise ValueError("No state-level numeric values were available for this metric.")

    mapped = mapped.groupby("state", as_index=False)["value"].mean()
    mapped["state_name"] = mapped["state"].map(US_STATE_NAMES)
    mapped["metric"] = metric_column
    return mapped.sort_values("value", ascending=False).reset_index(drop=True)
