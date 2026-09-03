"""Generate reproducible composite-index robustness benchmark outputs."""

from pathlib import Path

import pandas as pd

from capital_access_atlas import (
    NORMALIZATION_METHODS,
    build_composite_index,
    leave_one_metric_out_sensitivity,
    load_cbp_state_file,
    missing_data_stress_test,
    normalization_sensitivity_benchmark,
    summarize_cbp_state_totals,
    weight_sensitivity_benchmark,
)

OUTPUT_DIR = Path("validation")
PROTOCOL_VERSION = "1.0"
METRICS = [
    "establishments",
    "employment",
    "annual_payroll_thousands",
    "q1_payroll_thousands",
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    state = summarize_cbp_state_totals(load_cbp_state_file())
    metrics = [metric for metric in METRICS if metric in state.columns]
    if len(metrics) < 2:
        raise RuntimeError("At least two CBP metrics are required for robustness testing.")

    weights = {metric: 1.0 for metric in metrics}

    omission = leave_one_metric_out_sensitivity(
        state,
        state_column="state",
        metric_weights=weights,
    )
    normalization = normalization_sensitivity_benchmark(
        state,
        state_column="state",
        metric_weights=weights,
        methods=NORMALIZATION_METHODS,
    )
    weight = weight_sensitivity_benchmark(
        state,
        state_column="state",
        metric_weights=weights,
        emphasis_multiplier=2.0,
    )
    missing = missing_data_stress_test(
        state,
        state_column="state",
        metric_weights=weights,
        missing_rates=(0.05, 0.10, 0.20),
        repeats=25,
        seed=42,
    )

    rank_columns = {}
    for method in NORMALIZATION_METHODS:
        index = build_composite_index(
            state,
            state_column="state",
            metric_weights=weights,
            normalization=method,
        )
        ranks = index.set_index("state")["capital_access_index"].rank(
            ascending=False,
            method="average",
        )
        rank_columns[method] = ranks

    rank_frame = pd.DataFrame(rank_columns)
    rank_correlation = rank_frame.corr(method="pearson")

    omission.to_csv(OUTPUT_DIR / "index_leave_one_out.csv", index=False)
    normalization.to_csv(
        OUTPUT_DIR / "index_normalization_sensitivity.csv",
        index=False,
    )
    weight.to_csv(OUTPUT_DIR / "index_weight_sensitivity.csv", index=False)
    missing.to_csv(OUTPUT_DIR / "index_missing_data_stress.csv", index=False)
    rank_frame.to_csv(OUTPUT_DIR / "index_normalization_ranks.csv")
    rank_correlation.to_csv(
        OUTPUT_DIR / "index_normalization_rank_correlation.csv"
    )

    print(f"Robustness protocol: {PROTOCOL_VERSION}")
    print("\nNormalization sensitivity")
    print(normalization.to_string(index=False))
    print("\nWeight sensitivity")
    print(weight.to_string(index=False))
    print("\nMissing-data stress test")
    print(missing.to_string(index=False))
    print("\nNormalization rank-correlation matrix")
    print(rank_correlation.to_string())


if __name__ == "__main__":
    main()
