import pandas as pd
import pytest

from capital_access_atlas.indicators import (
    NORMALIZATION_METHODS,
    build_composite_index,
    standardized_score,
)


def test_build_composite_index_returns_zero_to_100_scores():
    frame = pd.DataFrame(
        {
            "State": ["Virginia", "Maryland", "Texas", "California"],
            "Activity": [10, 20, 30, 40],
            "Barrier": [40, 30, 20, 10],
        }
    )

    result = build_composite_index(
        frame,
        state_column="State",
        metric_weights={"Activity": 1.0, "Barrier": 1.0},
        inverse_metrics={"Barrier"},
    )

    assert result["capital_access_index"].between(0, 100).all()
    assert result["data_coverage"].between(0, 1).all()
    assert result.iloc[0]["state"] == "CA"


@pytest.mark.parametrize("method", NORMALIZATION_METHODS)
def test_normalization_methods_stay_on_zero_to_100_scale(method):
    scores = standardized_score(pd.Series([1, 2, 3, 4, 100]), method=method)

    assert scores.dropna().between(0, 100).all()


def test_build_composite_index_supports_robust_normalization():
    frame = pd.DataFrame(
        {
            "State": ["VA", "MD", "TX", "CA"],
            "Activity": [10, 20, 30, 1000],
            "Jobs": [8, 19, 33, 45],
        }
    )

    result = build_composite_index(
        frame,
        state_column="State",
        metric_weights={"Activity": 1.0, "Jobs": 1.0},
        normalization="robust_zscore",
    )

    assert result["normalization"].eq("robust_zscore").all()


def test_build_composite_index_rejects_empty_metrics():
    frame = pd.DataFrame({"State": ["VA", "MD"], "Value": [1, 2]})

    with pytest.raises(ValueError):
        build_composite_index(frame, "State", {})


def test_build_composite_index_rejects_zero_total_weight():
    frame = pd.DataFrame({"State": ["VA", "MD"], "Value": [1, 2]})

    with pytest.raises(ValueError):
        build_composite_index(frame, "State", {"Value": 0.0})
