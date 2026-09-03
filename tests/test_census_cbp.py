from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd

from capital_access_atlas.census_cbp import (
    _first_data_member,
    load_cbp_state_file,
    summarize_cbp_state_totals,
)


def _archive_bytes(csv_text: str) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("cbp23st.txt", csv_text)
    return buffer.getvalue()


def test_load_cbp_state_file_reads_zip_member():
    payload = _archive_bytes("fipstate,naics,est,emp\n51,------,10,100\n")
    frame = load_cbp_state_file(lambda _: payload)

    assert list(frame.columns) == ["fipstate", "naics", "est", "emp"]
    assert len(frame) == 1


def test_summarize_cbp_state_totals_maps_fips_and_core_metrics():
    frame = pd.DataFrame(
        {
            "fipstate": ["51", "24", "06"],
            "naics": ["------", "------", "------"],
            "est": ["100", "80", "500"],
            "emp": ["1000", "700", "5000"],
            "ap": ["12000", "8000", "90000"],
            "qp1": ["3000", "2000", "22000"],
        }
    )

    summary = summarize_cbp_state_totals(frame)

    assert set(summary["state"]) == {"VA", "MD", "CA"}
    assert summary.loc[summary["state"] == "VA", "establishments"].iloc[0] == 100


def test_first_data_member_rejects_empty_archive():
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("README.md", "metadata only")

    with ZipFile(BytesIO(buffer.getvalue())) as archive:
        try:
            _first_data_member(archive)
        except ValueError as exc:
            assert "CSV/text" in str(exc)
        else:
            raise AssertionError("Expected ValueError")
