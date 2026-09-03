"""Transparent composite-indicator helpers for atlas research."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .geography import coerce_numeric_series, normalize_state_abbreviation


def percentile_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert a numeric series to a 0-100 percentile score."""
    numeric = coerce_numeric_series(series)
    scored = numeric.rank(method="average", pct=True) * 100
    if not higher_is_better:
        scored = 100 - scored
    return scored


def build_composite_index(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
) -> pd.DataFrame:
    """Build a transparent weighted 0-100 state index from selected metrics.

    Parameters
    ----------
    frame:
        DataFrame containing one or more rows per state.
    state_column:
        Column containing state names or abbreviations.
    metric_weights:
        Mapping of metric column name to non-negative weight.
    inverse_metrics:
        Metrics where lower raw values should yield a higher index score.
    """
    if not metric_weights:
        raise ValueError("At least one metric is required.")

    inverse_metrics = inverse_metrics or set()
    unknown = sorted(set(metric_weights) - set(frame.columns))
    if unknown:
        raise ValueError(f"Unknown metric columns: {unknown}")

    weights = np.array(list(metric_weights.values()), dtype=float)
    if np.any(weights < 0) or float(weights.sum()) <= 0:
        raise ValueError("Metric weights must be non-negative and sum to more than zero.")

    work = pd.DataFrame(
        {"state": frame[state_column].map(normalize_state_abbreviation)}
    )

    component_columns: list[str] = []
    normalized_weights: dict[str, float] = {}
    total_weight = float(weights.sum())

    for metric, weight in metric_weights.items():
        component = f"{metric}__score"
        work[component] = percentile_score(
            frame[metric],
            higher_is_better=metric not in inverse_metrics,
        )
        component_columns.append(component)
        normalized_weights[component] = float(weight) / total_weight

    work = work.dropna(subset=["state"])
    aggregated = work.groupby("state", as_index=False)[component_columns].mean()

    weighted_total = pd.Series(0.0, index=aggregated.index)
    available_weight = pd.Series(0.0, index=aggregated.index)

    for component, weight in normalized_weights.items():
        valid = aggregated[component].notna()
        weighted_total = weighted_total.add(
            aggregated[component].fillna(0) * weight,
            fill_value=0,
        )
        available_weight = available_weight.add(valid.astype(float) * weight, fill_value=0)

    aggregated["capital_access_index"] = weighted_total.div(
        available_weight.replace(0, np.nan)
    )
    aggregated["data_coverage"] = available_weight
    return aggregated.sort_values(
        "capital_access_index",
        ascending=False,
    ).reset_index(drop=True)
