from io import BytesIO

import pandas as pd

from capital_access_atlas.cdfi import (
    discover_cdfi_workbook_url,
    load_cdfi_certification_workbook,
    merge_cdfi_with_cbp,
    summarize_cdfi_by_state,
)


def test_discover_cdfi_workbook_url_uses_official_link():
    html = b"""
    <a href="/media/123456/download?inline=">
      List of Currently Certified CDFIs
    </a>
    """

    url = discover_cdfi_workbook_url(lambda _: html)

    assert url == "https://www.cdfifund.gov/media/123456/download?inline="


def test_summarize_cdfi_by_state_counts_unique_organizations():
    frame = pd.DataFrame(
        {
            "Organization Name": ["A Fund", "B Fund", "A Fund", "C Fund"],
            "State": ["VA", "Virginia", "MD", "TX"],
            "Organization Type": ["Loan Fund", "Credit Union", "Loan Fund", "Bank"],
        }
    )

    result = summarize_cdfi_by_state(frame)

    va = result.loc[result["state"] == "VA"].iloc[0]
    assert va["certified_cdfis"] == 2
    assert va["institution_type_count"] == 2


def test_merge_cdfi_with_cbp_calculates_relative_intensity():
    cdfi = pd.DataFrame(
        {
            "state": ["VA", "MD"],
            "certified_cdfis": [20, 10],
            "institution_type_count": [3, 2],
        }
    )
    cbp = pd.DataFrame(
        {
            "state": ["VA", "MD"],
            "state_name": ["Virginia", "Maryland"],
            "establishments": [100000, 50000],
        }
    )

    merged = merge_cdfi_with_cbp(cdfi, cbp)

    assert merged.loc[merged["state"] == "VA", "cdfis_per_10k_establishments"].iloc[0] == 2
    assert merged.loc[merged["state"] == "MD", "cdfis_per_10k_establishments"].iloc[0] == 2



def test_loader_prefers_institution_detail_sheet_over_state_summary():
    summary = pd.DataFrame(
        {
            "State": ["VA", "MD", "TX"],
            "Count": [20, 10, 30],
        }
    )
    detail = pd.DataFrame(
        {
            "Organization Name": [f"CDFI {index}" for index in range(120)],
            "State": ["VA", "MD", "TX", "CA"] * 30,
            "Organization Type": ["Loan Fund"] * 120,
        }
    )

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="State Summary", index=False)
        detail.to_excel(writer, sheet_name="Certified CDFIs", index=False)

    workbook = buffer.getvalue()
    landing = b'<a href="/media/123456/download?inline=">List of Currently Certified CDFIs</a>'

    def fake_fetch(url):
        if "programs-training" in url:
            return landing
        return workbook

    metadata, frame = load_cdfi_certification_workbook(fake_fetch)

    assert metadata["worksheet"] == "Certified CDFIs"
    assert len(frame) == 120
