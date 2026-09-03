"""Transparent composite-indicator helpers for Atlas research."""

from __future__ import annotations

from statistics import NormalDist

import numpy as np
import pandas as pd

from .geography import coerce_numeric_series, normalize_state_abbreviation

NORMALIZATION_METHODS = (
    "percentile",
    "zscore",
    "winsorized_zscore",
    "robust_zscore",
)


def percentile_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert a numeric series to a 0-100 percentile score."""
    numeric = coerce_numeric_series(series)
    scored = numeric.rank(method="average", pct=True) * 100
    if not higher_is_better:
        scored = 100 - scored
    return scored


def _cdf_score(zscores: pd.Series) -> pd.Series:
    normal = NormalDist()
    return zscores.map(
        lambda value: normal.cdf(float(value)) * 100 if pd.notna(value) else np.nan
    )


def standardized_score(
    series: pd.Series,
    method: str = "zscore",
    higher_is_better: bool = True,
) -> pd.Series:
    """Transform a numeric series to a 0-100 score using a documented method."""
    if method not in NORMALIZATION_METHODS:
        raise ValueError(
            f"Unknown normalization method: {method}. "
            f"Choose from {', '.join(NORMALIZATION_METHODS)}."
        )
    if method == "percentile":
        return percentile_score(series, higher_is_better=higher_is_better)

    numeric = coerce_numeric_series(series)

    if method == "winsorized_zscore":
        lower = numeric.quantile(0.05)
        upper = numeric.quantile(0.95)
        numeric = numeric.clip(lower=lower, upper=upper)

    if method == "robust_zscore":
        center = numeric.median()
        mad = (numeric - center).abs().median()
        scale = float(mad) * 1.4826
        if not np.isfinite(scale) or scale == 0:
            method = "zscore"
        else:
            scored = _cdf_score((numeric - center) / scale)
            return scored if higher_is_better else 100 - scored

    center = numeric.mean()
    scale = numeric.std(ddof=0)
    if not np.isfinite(scale) or scale == 0:
        scored = pd.Series(np.nan, index=numeric.index, dtype=float)
        scored.loc[numeric.notna()] = 50.0
    else:
        scored = _cdf_score((numeric - center) / scale)

    return scored if higher_is_better else 100 - scored


def build_composite_index(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
    normalization: str = "percentile",
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
    normalization:
        One of percentile, zscore, winsorized_zscore, or robust_zscore.
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
        work[component] = standardized_score(
            frame[metric],
            method=normalization,
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
    aggregated["normalization"] = normalization
    return aggregated.sort_values(
        "capital_access_index",
        ascending=False,
    ).reset_index(drop=True)
