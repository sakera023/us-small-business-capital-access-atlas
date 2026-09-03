"""Data-quality and index-sensitivity diagnostics."""

from __future__ import annotations

import pandas as pd

from .indicators import build_composite_index


def metric_quality_report(
    frame: pd.DataFrame,
    metrics: list[str],
) -> pd.DataFrame:
    """Summarize completeness and uniqueness for candidate index metrics."""
    rows = []
    total = len(frame)

    for metric in metrics:
        if metric not in frame.columns:
            raise ValueError(f"Unknown metric column: {metric}")

        numeric = pd.to_numeric(frame[metric], errors="coerce")
        valid = int(numeric.notna().sum())
        rows.append(
            {
                "metric": metric,
                "rows": total,
                "valid_values": valid,
                "missing_values": total - valid,
                "coverage_rate": valid / total if total else 0.0,
                "unique_numeric_values": int(numeric.nunique(dropna=True)),
                "minimum": numeric.min(),
                "median": numeric.median(),
                "maximum": numeric.max(),
            }
        )

    return pd.DataFrame(rows)


def leave_one_metric_out_sensitivity(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
) -> pd.DataFrame:
    """Measure state-rank changes when each component is omitted in turn."""
    if len(metric_weights) < 2:
        raise ValueError("Sensitivity analysis requires at least two metrics.")

    baseline = build_composite_index(
        frame,
        state_column=state_column,
        metric_weights=metric_weights,
        inverse_metrics=inverse_metrics,
    )[["state", "capital_access_index"]].copy()
    baseline["baseline_rank"] = baseline["capital_access_index"].rank(
        ascending=False, method="min"
    )

    rows = []
    for omitted in metric_weights:
        reduced_weights = {
            metric: weight
            for metric, weight in metric_weights.items()
            if metric != omitted
        }
        reduced_inverse = (inverse_metrics or set()) - {omitted}
        reduced = build_composite_index(
            frame,
            state_column=state_column,
            metric_weights=reduced_weights,
            inverse_metrics=reduced_inverse,
        )[["state", "capital_access_index"]].copy()
        reduced["reduced_rank"] = reduced["capital_access_index"].rank(
            ascending=False, method="min"
        )

        merged = baseline.merge(reduced, on="state", suffixes=("_baseline", "_reduced"))
        rank_shift = (merged["baseline_rank"] - merged["reduced_rank"]).abs()
        rows.append(
            {
                "omitted_metric": omitted,
                "states_compared": len(merged),
                "mean_absolute_rank_shift": float(rank_shift.mean()),
                "max_absolute_rank_shift": float(rank_shift.max()),
                "rank_correlation": float(
                    merged["baseline_rank"].corr(merged["reduced_rank"], method="pearson")
                ),
            }
        )

    return pd.DataFrame(rows).sort_values(
        "mean_absolute_rank_shift", ascending=False
    ).reset_index(drop=True)
