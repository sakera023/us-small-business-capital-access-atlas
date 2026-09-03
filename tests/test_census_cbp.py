from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd

from capital_access_atlas.census_cbp import (
    _first_data_member,
    county_name_lookup,
    load_cbp_county_file,
    load_cbp_state_file,
    load_county_geojson,
    summarize_cbp_county_totals,
    summarize_cbp_state_totals,
    summarize_county_industry_concentration,
)


def _archive_bytes(csv_text: str, member: str = "cbp23st.txt") -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr(member, csv_text)
    return buffer.getvalue()


def test_load_cbp_state_file_reads_zip_member():
    payload = _archive_bytes("fipstate,naics,est,emp\n51,------,10,100\n")
    frame = load_cbp_state_file(lambda _: payload)

    assert list(frame.columns) == ["fipstate", "naics", "est", "emp"]
    assert len(frame) == 1


def test_load_cbp_county_file_reads_zip_member():
    payload = _archive_bytes(
        "fipstate,fipscty,naics,est,emp\n51,013,------,10,100\n",
        member="cbp23co.txt",
    )
    frame = load_cbp_county_file(lambda _: payload)

    assert "fipscty" in frame.columns
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


def test_summarize_cbp_county_totals_builds_five_digit_geoid():
    frame = pd.DataFrame(
        {
            "fipstate": ["51", "24"],
            "fipscty": ["013", "031"],
            "naics": ["------", "------"],
            "est": ["100", "80"],
            "emp": ["1000", "700"],
            "ap": ["12000", "8000"],
            "qp1": ["3000", "2000"],
        }
    )

    summary = summarize_cbp_county_totals(frame)

    assert set(summary["geoid"]) == {"51013", "24031"}
    assert set(summary["state"]) == {"VA", "MD"}


def test_county_industry_concentration_uses_sector_shares():
    frame = pd.DataFrame(
        {
            "fipstate": ["51", "51", "51", "51"],
            "fipscty": ["013", "013", "059", "059"],
            "naics": ["11----", "23----", "11----", "23----"],
            "est": ["50", "50", "90", "10"],
        }
    )

    result = summarize_county_industry_concentration(frame)

    arlington = result.loc[result["geoid"] == "51013"].iloc[0]
    fairfax = result.loc[result["geoid"] == "51059"].iloc[0]
    assert arlington["industry_hhi"] == 5000
    assert fairfax["industry_hhi"] == 8200


def test_load_county_geojson_builds_query_and_returns_features():
    seen = {}

    def fake_fetch(url):
        seen["url"] = url
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"GEOID": "51013", "NAME": "Arlington County"},
                    "geometry": {"type": "Polygon", "coordinates": []},
                }
            ],
        }

    payload = load_county_geojson("51", fetch_json=fake_fetch)

    assert payload["features"]
    assert "STATE%3D%2751%27" in seen["url"] or "STATE%3D%2751%27" in seen["url"].upper()


def test_county_name_lookup():
    lookup = county_name_lookup(
        {
            "features": [
                {"properties": {"GEOID": "51013", "NAME": "Arlington County"}},
                {"properties": {"GEOID": "51059", "BASENAME": "Fairfax"}},
            ]
        }
    )

    assert lookup["51013"] == "Arlington County"
    assert lookup["51059"] == "Fairfax"


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
