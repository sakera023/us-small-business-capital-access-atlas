import pandas as pd

from capital_access_atlas.analysis import (
    leave_one_metric_out_sensitivity,
    metric_quality_report,
    missing_data_stress_test,
    normalization_sensitivity_benchmark,
    weight_sensitivity_benchmark,
)


def _frame():
    return pd.DataFrame(
        {
            "State": ["VA", "MD", "CA", "TX", "NC", "GA"],
            "Activity": [10, 20, 31, 40, 25, 18],
            "Jobs": [12, 18, 29, 41, 23, 17],
            "Barrier": [40, 30, 19, 10, 24, 35],
        }
    )


def test_metric_quality_report_calculates_coverage():
    frame = pd.DataFrame({"A": [1, 2, None, 4], "B": [4, 3, 2, 1]})
    report = metric_quality_report(frame, ["A", "B"])

    a = report.loc[report["metric"] == "A"].iloc[0]
    assert a["valid_values"] == 3
    assert a["coverage_rate"] == 0.75


def test_leave_one_metric_out_returns_one_row_per_metric():
    result = leave_one_metric_out_sensitivity(
        _frame(),
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
    )

    assert len(result) == 3
    assert result["rank_correlation"].between(-1, 1).all()


def test_normalization_sensitivity_compares_four_methods():
    result = normalization_sensitivity_benchmark(
        _frame(),
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
    )

    assert len(result) == 4
    assert result.iloc[0]["normalization"] == "percentile"


def test_weight_sensitivity_emphasizes_each_component():
    result = weight_sensitivity_benchmark(
        _frame(),
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
        emphasis_multiplier=2.0,
    )

    assert set(result["emphasized_metric"]) == {"Activity", "Jobs", "Barrier"}


def test_missing_data_stress_test_is_reproducible():
    first = missing_data_stress_test(
        _frame(),
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
        missing_rates=(0.1,),
        repeats=3,
        seed=7,
    )
    second = missing_data_stress_test(
        _frame(),
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
        missing_rates=(0.1,),
        repeats=3,
        seed=7,
    )

    pd.testing.assert_frame_equal(first, second)
