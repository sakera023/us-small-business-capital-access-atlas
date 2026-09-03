"""Generate reproducible validation outputs for Census CBP state and county data."""

from pathlib import Path

from capital_access_atlas import (
    load_cbp_county_file,
    load_cbp_state_file,
    metric_quality_report,
    summarize_cbp_county_totals,
    summarize_cbp_state_totals,
    summarize_county_industry_concentration,
)

VALIDATION_PROTOCOL_VERSION = "2.0"
OUTPUT_DIR = Path("validation")
CBP_METRICS = [
    "establishments",
    "employment",
    "annual_payroll_thousands",
    "q1_payroll_thousands",
]


def available_metrics(frame):
    return [column for column in CBP_METRICS if column in frame.columns]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw_state = load_cbp_state_file()
    state_totals = summarize_cbp_state_totals(raw_state)
    state_quality = metric_quality_report(
        state_totals,
        available_metrics(state_totals),
    )

    raw_county = load_cbp_county_file()
    county_totals = summarize_cbp_county_totals(raw_county)
    county_quality = metric_quality_report(
        county_totals,
        available_metrics(county_totals),
    )
    county_concentration = summarize_county_industry_concentration(raw_county)

    state_totals.to_csv(OUTPUT_DIR / "cbp_2023_state_totals.csv", index=False)
    state_quality.to_csv(OUTPUT_DIR / "cbp_2023_state_quality.csv", index=False)
    county_totals.to_csv(OUTPUT_DIR / "cbp_2023_county_totals.csv", index=False)
    county_quality.to_csv(OUTPUT_DIR / "cbp_2023_county_quality.csv", index=False)
    county_concentration.to_csv(
        OUTPUT_DIR / "cbp_2023_county_industry_concentration.csv",
        index=False,
    )

    print(f"Validation protocol: {VALIDATION_PROTOCOL_VERSION}")
    print(f"State rows: {len(state_totals):,}")
    print(f"County rows: {len(county_totals):,}")
    print(f"County concentration rows: {len(county_concentration):,}")
    print("\nState quality")
    print(state_quality.to_string(index=False))
    print("\nCounty quality")
    print(county_quality.to_string(index=False))


if __name__ == "__main__":
    main()
