"""U.S. Census County Business Patterns (CBP) public-data integration."""

from __future__ import annotations

from io import BytesIO
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pandas as pd

from .geography import US_STATE_NAMES

CENSUS_CBP_2023 = {
    "label": "U.S. Census County Business Patterns 2023 — State File",
    "publisher": "U.S. Census Bureau",
    "vintage": "2023",
    "landing_page": "https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html",
    "documentation": "https://www.census.gov/data/developers/data-sets/cbp-zbp/cbp-api.html",
    "resource_url": (
        "https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23st.zip"
    ),
    "description": (
        "Annual state-level business-establishment statistics including employment, "
        "first-quarter payroll, annual payroll, and establishment counts by industry."
    ),
}

STATE_FIPS_TO_ABBR = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO",
    "09": "CT", "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI",
    "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
    "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
    "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
    "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD",
    "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
    "54": "WV", "55": "WI", "56": "WY",
}


def _first_data_member(archive: ZipFile) -> str:
    candidates = [
        name
        for name in archive.namelist()
        if not name.endswith("/") and name.lower().endswith((".csv", ".txt"))
    ]
    if not candidates:
        raise ValueError("The Census CBP ZIP archive did not contain a CSV/text file.")
    return candidates[0]


def _fetch_bytes(url: str, timeout: int = 60) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "us-small-business-capital-access-atlas/0.2"},
    )
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.read()


def load_cbp_state_file(fetch_bytes=_fetch_bytes) -> pd.DataFrame:
    """Load the official downloadable CBP state file."""
    raw = fetch_bytes(CENSUS_CBP_2023["resource_url"])
    with ZipFile(BytesIO(raw)) as archive:
        member = _first_data_member(archive)
        frame = pd.read_csv(archive.open(member), dtype=str, low_memory=False)

    frame.columns = [str(column).strip().lower() for column in frame.columns]
    return frame


def _column(frame: pd.DataFrame, *candidates: str) -> str | None:
    for candidate in candidates:
        if candidate in frame.columns:
            return candidate
    return None


def _filter_total_rows(frame: pd.DataFrame) -> pd.DataFrame:
    work = frame.copy()

    naics_column = _column(work, "naics", "naics2017")
    if naics_column:
        values = work[naics_column].astype(str).str.strip()
        preferred = ["------", "00", "0", "TOTAL", "ALL"]
        match = next((code for code in preferred if (values == code).any()), None)
        if match is not None:
            work = work[values == match]

    lfo_column = _column(work, "lfo")
    if lfo_column and (work[lfo_column].astype(str).str.zfill(3) == "001").any():
        work = work[work[lfo_column].astype(str).str.zfill(3) == "001"]

    size_column = _column(work, "empszes", "empsize")
    if size_column and (work[size_column].astype(str).str.zfill(3) == "001").any():
        work = work[work[size_column].astype(str).str.zfill(3) == "001"]

    return work


def summarize_cbp_state_totals(frame: pd.DataFrame) -> pd.DataFrame:
    """Return one state-level CBP total row with core published measures."""
    work = _filter_total_rows(frame)

    state_column = _column(work, "fipstate", "state")
    if state_column is None:
        raise ValueError("CBP state FIPS column was not found.")

    metric_candidates = {
        "establishments": ("est", "estab"),
        "employment": ("emp",),
        "annual_payroll_thousands": ("ap", "payann"),
        "q1_payroll_thousands": ("qp1", "payqtr1"),
    }

    output = pd.DataFrame()
    fips = work[state_column].astype(str).str.replace(".0", "", regex=False).str.zfill(2)
    output["state"] = fips.map(STATE_FIPS_TO_ABBR)
    output["state_name"] = output["state"].map(US_STATE_NAMES)

    for output_name, candidates in metric_candidates.items():
        source = _column(work, *candidates)
        if source:
            output[output_name] = pd.to_numeric(work[source], errors="coerce")

    output = output.dropna(subset=["state"]).drop_duplicates(subset=["state"])
    if output.empty:
        raise ValueError("No state-total CBP rows could be prepared.")

    return output.sort_values("state").reset_index(drop=True)
