import pandas as pd
import pytest

from capital_access_atlas.geography import (
    detect_state_column,
    normalize_state_abbreviation,
    numeric_metric_columns,
    prepare_state_metric,
)


def test_normalize_state_abbreviation():
    assert normalize_state_abbreviation("Virginia") == "VA"
    assert normalize_state_abbreviation("va") == "VA"
    assert normalize_state_abbreviation("District of Columbia") == "DC"
    assert normalize_state_abbreviation("Not a state") is None


def test_detect_state_column_and_metrics():
    frame = pd.DataFrame(
        {
            "State": ["Virginia", "Maryland", "Texas", "California"],
            "Businesses": ["800,000", "600,000", "3,000,000", "4,000,000"],
            "Share": ["99.5%", "99.4%", "99.8%", "99.8%"],
        }
    )

    state_column = detect_state_column(frame)
    metrics = numeric_metric_columns(frame, state_column)

    assert state_column == "State"
    assert "Businesses" in metrics
    assert "Share" in metrics


def test_prepare_state_metric():
    frame = pd.DataFrame(
        {
            "State": ["Virginia", "Maryland", "Texas"],
            "Value": ["10", "20", "30"],
        }
    )

    mapped = prepare_state_metric(frame, "Value")

    assert set(mapped["state"]) == {"VA", "MD", "TX"}
    assert mapped.loc[mapped["state"] == "TX", "value"].iloc[0] == 30


def test_prepare_state_metric_requires_state_column():
    frame = pd.DataFrame({"Region": ["East", "West", "South"], "Value": [1, 2, 3]})

    with pytest.raises(ValueError):
        prepare_state_metric(frame, "Value")
