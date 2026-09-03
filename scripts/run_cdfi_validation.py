"""Validate the current official Certified CDFI list and state summary."""

import json
from pathlib import Path

from capital_access_atlas import (
    load_cdfi_certification_workbook,
    metric_quality_report,
    summarize_cdfi_by_state,
)

OUTPUT_DIR = Path("validation")
PROTOCOL_VERSION = "1.0"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    metadata, raw = load_cdfi_certification_workbook()
    state = summarize_cdfi_by_state(raw)

    quality_metrics = ["certified_cdfis"]
    if state["institution_type_count"].notna().any():
        quality_metrics.append("institution_type_count")

    quality = metric_quality_report(state, quality_metrics)

    state.to_csv(OUTPUT_DIR / "cdfi_certified_state_summary.csv", index=False)
    quality.to_csv(OUTPUT_DIR / "cdfi_certified_state_quality.csv", index=False)
    (OUTPUT_DIR / "cdfi_certified_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(f"CDFI validation protocol: {PROTOCOL_VERSION}")
    print(f"Workbook: {metadata['resource_url']}")
    print(f"Worksheet: {metadata['worksheet']}")
    print(f"States / DC represented: {state['state'].nunique()}")
    print(f"Certified organizations represented: {int(state['certified_cdfis'].sum())}")
    print("\nQuality report")
    print(quality.to_string(index=False))


if __name__ == "__main__":
    main()
