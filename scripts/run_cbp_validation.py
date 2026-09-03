"""Generate a reproducible data-quality report for official Census CBP state totals."""

from pathlib import Path

from capital_access_atlas import (
    load_cbp_state_file,
    metric_quality_report,
    summarize_cbp_state_totals,
)

VALIDATION_PROTOCOL_VERSION = "1.0"
OUTPUT_DIR = Path("validation")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw = load_cbp_state_file()
    state_totals = summarize_cbp_state_totals(raw)

    metrics = [
        column
        for column in [
            "establishments",
            "employment",
            "annual_payroll_thousands",
            "q1_payroll_thousands",
        ]
        if column in state_totals.columns
    ]

    quality = metric_quality_report(state_totals, metrics)

    state_totals.to_csv(OUTPUT_DIR / "cbp_2023_state_totals.csv", index=False)
    quality.to_csv(OUTPUT_DIR / "cbp_2023_quality_report.csv", index=False)

    print("Census CBP 2023 state totals")
    print(state_totals.head().to_string(index=False))
    print("\nData-quality report")
    print(quality.to_string(index=False))


if __name__ == "__main__":
    main()
