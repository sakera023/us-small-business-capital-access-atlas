import pytest

from capital_access_atlas.public_data import SBA_STATE_DATASET, _select_excel_resource


def test_sba_catalog_uses_official_source():
    assert SBA_STATE_DATASET["landing_page"].startswith("https://data.sba.gov/")


def test_select_excel_resource_prefers_active_excel():
    package = {
        "resources": [
            {"format": "CSV", "url": "https://example.test/data.csv", "state": "active"},
            {"format": "XLSX", "url": "https://example.test/old.xlsx", "state": "deleted"},
            {"format": "XLSX", "url": "https://example.test/current.xlsx", "state": "active"},
        ]
    }

    selected = _select_excel_resource(package)

    assert selected["url"] == "https://example.test/current.xlsx"


def test_select_excel_resource_rejects_missing_excel():
    with pytest.raises(ValueError):
        _select_excel_resource(
            {"resources": [{"format": "CSV", "url": "https://example.test/data.csv"}]}
        )
