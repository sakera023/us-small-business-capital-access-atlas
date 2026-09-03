import pandas as pd

from capital_access_atlas.analysis import (
    leave_one_metric_out_sensitivity,
    metric_quality_report,
)


def test_metric_quality_report_calculates_coverage():
    frame = pd.DataFrame({"A": [1, 2, None, 4], "B": [4, 3, 2, 1]})
    report = metric_quality_report(frame, ["A", "B"])

    a = report.loc[report["metric"] == "A"].iloc[0]
    assert a["valid_values"] == 3
    assert a["coverage_rate"] == 0.75


def test_leave_one_metric_out_returns_one_row_per_metric():
    frame = pd.DataFrame(
        {
            "State": ["VA", "MD", "CA", "TX"],
            "Activity": [10, 20, 30, 40],
            "Jobs": [12, 18, 29, 41],
            "Barrier": [40, 30, 20, 10],
        }
    )

    result = leave_one_metric_out_sensitivity(
        frame,
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
    )

    assert len(result) == 3
    assert result["rank_correlation"].between(-1, 1).all()
