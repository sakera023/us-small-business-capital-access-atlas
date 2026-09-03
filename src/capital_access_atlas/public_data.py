"""Official public-data retrieval for the Capital Access Atlas."""

from __future__ import annotations

import json
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

SBA_CKAN_PACKAGE_SHOW = "https://data.sba.gov/api/3/action/package_show"

SBA_STATE_DATASET = {
    "label": "SBA State Small Business Statistics 2025",
    "slug": "state-small-business-statistics-2025",
    "landing_page": "https://data.sba.gov/dataset/state-small-business-statistics-2025",
    "publisher": "U.S. Small Business Administration, Office of Advocacy",
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


def _fetch_json(url: str, timeout: int = 30) -> dict:
    return json.loads(_fetch_bytes(url, timeout=timeout).decode("utf-8"))


def _select_excel_resource(package: dict) -> dict:
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
    """Resolve current metadata for the official SBA state-statistics workbook."""
    query = urlencode({"id": SBA_STATE_DATASET["slug"]})
    payload = _fetch_json(f"{SBA_CKAN_PACKAGE_SHOW}?{query}")

    if not payload.get("success"):
        raise RuntimeError("The SBA data catalog did not return a successful response.")

    package = payload["result"]
    resource = _select_excel_resource(package)

    return {
        "label": SBA_STATE_DATASET["label"],
        "publisher": SBA_STATE_DATASET["publisher"],
        "description": SBA_STATE_DATASET["description"],
        "landing_page": SBA_STATE_DATASET["landing_page"],
        "package_title": package.get("title", SBA_STATE_DATASET["label"]),
        "last_modified": package.get("metadata_modified"),
        "license_title": package.get("license_title") or "U.S. Government Works",
        "resource_name": resource.get("name") or "Excel resource",
        "resource_url": resource["url"],
        "resource_format": resource.get("format", "XLSX"),
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
