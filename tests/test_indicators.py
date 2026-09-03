import pandas as pd
import pytest

from capital_access_atlas.indicators import build_composite_index


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


def test_build_composite_index_rejects_empty_metrics():
    frame = pd.DataFrame({"State": ["VA", "MD"], "Value": [1, 2]})

    with pytest.raises(ValueError):
        build_composite_index(frame, "State", {})


def test_build_composite_index_rejects_zero_total_weight():
    frame = pd.DataFrame({"State": ["VA", "MD"], "Value": [1, 2]})

    with pytest.raises(ValueError):
        build_composite_index(frame, "State", {"Value": 0.0})
