"""Official public-data retrieval for the Capital Access Atlas."""

from __future__ import annotations

from io import BytesIO
from urllib.request import Request, urlopen

import pandas as pd

SBA_STATE_DATASET = {
    "label": "SBA State Small Business Statistics 2025",
    "landing_page": "https://data.sba.gov/dataset/state-small-business-statistics-2025",
    "resource_url": (
        "https://data.sba.gov/sites/default/files/distribution/"
        "SBA-ADVO-CKAN-009/state_statistics_rankings_2025.xlsx"
    ),
    "publisher": "U.S. Small Business Administration, Office of Advocacy",
    "identifier": "SBA-ADVO-CKAN-009",
    "issue_date": "2026-01-30",
    "last_modified": "2026-01-30",
    "license_title": "U.S. Government Works",
    "description": (
        "State-level small-business statistics from the SBA 2025 Small Business "
        "Profiles, including business counts, employment, job creation, and ownership."
    ),
}


def _fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "us-small-business-capital-access-atlas/0.1"},
    )
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.read()


def _select_excel_resource(package: dict) -> dict:
    """Select an Excel resource from CKAN-style metadata for compatibility/tests."""
    resources = package.get("resources", [])
    candidates = [
        resource
        for resource in resources
        if str(resource.get("format", "")).strip().lower() in {"xlsx", "xls"}
        and resource.get("url")
    ]
    if not candidates:
        raise ValueError("No Excel resource was found in the SBA dataset package.")

    active = [
        resource
        for resource in candidates
        if str(resource.get("state", "active")).lower() == "active"
    ]
    return (active or candidates)[0]


def get_sba_state_metadata() -> dict:
    """Return verified metadata for the official SBA state-statistics workbook.

    The SBA public site currently exposes the dataset through its public landing page and
    canonical file distribution URL. The Atlas therefore avoids depending on the retired
    /api/3/action/package_show route that can return HTTP 404 on the current SBA site.
    """
    return {
        "label": SBA_STATE_DATASET["label"],
        "publisher": SBA_STATE_DATASET["publisher"],
        "description": SBA_STATE_DATASET["description"],
        "landing_page": SBA_STATE_DATASET["landing_page"],
        "package_title": SBA_STATE_DATASET["label"],
        "last_modified": SBA_STATE_DATASET["last_modified"],
        "license_title": SBA_STATE_DATASET["license_title"],
        "resource_name": "State small business statistics 2025 (XLSX)",
        "resource_url": SBA_STATE_DATASET["resource_url"],
        "resource_format": "XLSX",
        "identifier": SBA_STATE_DATASET["identifier"],
    }


def load_sba_state_workbook() -> tuple[dict, dict[str, pd.DataFrame]]:
    """Download the current official SBA workbook and return all non-empty sheets."""
    metadata = get_sba_state_metadata()
    workbook = _fetch_bytes(metadata["resource_url"])
    sheets = pd.read_excel(BytesIO(workbook), sheet_name=None)

    cleaned = {
        str(name): frame.dropna(axis=0, how="all").dropna(axis=1, how="all")
        for name, frame in sheets.items()
    }
    cleaned = {name: frame for name, frame in cleaned.items() if not frame.empty}

    if not cleaned:
        raise ValueError("The SBA workbook did not contain a readable data sheet.")

    return metadata, cleaned
