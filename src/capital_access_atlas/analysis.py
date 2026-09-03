"""Data-quality and index-sensitivity diagnostics."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import NORMALIZATION_METHODS, build_composite_index


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


def _ranked(index_frame: pd.DataFrame, rank_name: str) -> pd.DataFrame:
    ranked = index_frame[["state", "capital_access_index"]].dropna().copy()
    ranked[rank_name] = ranked["capital_access_index"].rank(
        ascending=False,
        method="average",
    )
    return ranked


def _rank_comparison(
    baseline: pd.DataFrame,
    alternative: pd.DataFrame,
    alternative_label: str,
    label_column: str,
) -> dict[str, float | int | str]:
    merged = baseline.merge(alternative, on="state", how="inner")
    shift = (merged["baseline_rank"] - merged["alternative_rank"]).abs()
    correlation = merged["baseline_rank"].corr(
        merged["alternative_rank"],
        method="pearson",
    )
    return {
        label_column: alternative_label,
        "states_compared": len(merged),
        "mean_absolute_rank_shift": float(shift.mean()) if len(shift) else np.nan,
        "max_absolute_rank_shift": float(shift.max()) if len(shift) else np.nan,
        "rank_correlation": float(correlation) if pd.notna(correlation) else np.nan,
    }


def leave_one_metric_out_sensitivity(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
    normalization: str = "percentile",
) -> pd.DataFrame:
    """Measure state-rank changes when each component is omitted in turn."""
    if len(metric_weights) < 2:
        raise ValueError("Sensitivity analysis requires at least two metrics.")

    baseline = _ranked(
        build_composite_index(
            frame,
            state_column=state_column,
            metric_weights=metric_weights,
            inverse_metrics=inverse_metrics,
            normalization=normalization,
        ),
        "baseline_rank",
    )[["state", "baseline_rank"]]

    rows = []
    for omitted in metric_weights:
        reduced_weights = {
            metric: weight
            for metric, weight in metric_weights.items()
            if metric != omitted
        }
        reduced_inverse = (inverse_metrics or set()) - {omitted}
        reduced = _ranked(
            build_composite_index(
                frame,
                state_column=state_column,
                metric_weights=reduced_weights,
                inverse_metrics=reduced_inverse,
                normalization=normalization,
            ),
            "alternative_rank",
        )[["state", "alternative_rank"]]

        rows.append(
            _rank_comparison(
                baseline,
                reduced,
                omitted,
                "omitted_metric",
            )
        )

    return pd.DataFrame(rows).sort_values(
        "mean_absolute_rank_shift",
        ascending=False,
    ).reset_index(drop=True)


def normalization_sensitivity_benchmark(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
    methods: tuple[str, ...] = NORMALIZATION_METHODS,
) -> pd.DataFrame:
    """Compare state rankings across alternative normalization methods."""
    if not methods:
        raise ValueError("At least one normalization method is required.")

    baseline_method = methods[0]
    baseline = _ranked(
        build_composite_index(
            frame,
            state_column=state_column,
            metric_weights=metric_weights,
            inverse_metrics=inverse_metrics,
            normalization=baseline_method,
        ),
        "baseline_rank",
    )[["state", "baseline_rank"]]

    rows = []
    for method in methods:
        alternative = _ranked(
            build_composite_index(
                frame,
                state_column=state_column,
                metric_weights=metric_weights,
                inverse_metrics=inverse_metrics,
                normalization=method,
            ),
            "alternative_rank",
        )[["state", "alternative_rank"]]
        row = _rank_comparison(
            baseline,
            alternative,
            method,
            "normalization",
        )
        row["baseline_normalization"] = baseline_method
        rows.append(row)

    return pd.DataFrame(rows)


def weight_sensitivity_benchmark(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
    normalization: str = "percentile",
    emphasis_multiplier: float = 2.0,
) -> pd.DataFrame:
    """Compare baseline weights with one-component-emphasis scenarios."""
    if len(metric_weights) < 2:
        raise ValueError("Weight sensitivity requires at least two metrics.")
    if emphasis_multiplier <= 0:
        raise ValueError("emphasis_multiplier must be greater than zero.")

    baseline = _ranked(
        build_composite_index(
            frame,
            state_column=state_column,
            metric_weights=metric_weights,
            inverse_metrics=inverse_metrics,
            normalization=normalization,
        ),
        "baseline_rank",
    )[["state", "baseline_rank"]]

    rows = []
    for emphasized in metric_weights:
        scenario = dict(metric_weights)
        scenario[emphasized] = scenario[emphasized] * emphasis_multiplier
        alternative = _ranked(
            build_composite_index(
                frame,
                state_column=state_column,
                metric_weights=scenario,
                inverse_metrics=inverse_metrics,
                normalization=normalization,
            ),
            "alternative_rank",
        )[["state", "alternative_rank"]]
        row = _rank_comparison(
            baseline,
            alternative,
            emphasized,
            "emphasized_metric",
        )
        row["emphasis_multiplier"] = emphasis_multiplier
        rows.append(row)

    return pd.DataFrame(rows).sort_values(
        "mean_absolute_rank_shift",
        ascending=False,
    ).reset_index(drop=True)


def missing_data_stress_test(
    frame: pd.DataFrame,
    state_column: str,
    metric_weights: dict[str, float],
    inverse_metrics: set[str] | None = None,
    normalization: str = "percentile",
    missing_rates: tuple[float, ...] = (0.05, 0.10, 0.20),
    repeats: int = 10,
    seed: int = 42,
) -> pd.DataFrame:
    """Stress-test index rankings after deterministic random metric deletion."""
    if repeats < 1:
        raise ValueError("repeats must be at least 1")
    if any(rate < 0 or rate >= 1 for rate in missing_rates):
        raise ValueError("missing rates must be between 0 (inclusive) and 1 (exclusive)")

    baseline_index = build_composite_index(
        frame,
        state_column=state_column,
        metric_weights=metric_weights,
        inverse_metrics=inverse_metrics,
        normalization=normalization,
    )
    baseline = _ranked(baseline_index, "baseline_rank")[["state", "baseline_rank"]]
    rng = np.random.default_rng(seed)

    rows = []
    metrics = list(metric_weights)

    for rate in missing_rates:
        shifts = []
        correlations = []
        coverage = []
        for _ in range(repeats):
            stressed = frame.copy()
            for metric in metrics:
                mask = rng.random(len(stressed)) < rate
                stressed.loc[mask, metric] = np.nan

            stressed_index = build_composite_index(
                stressed,
                state_column=state_column,
                metric_weights=metric_weights,
                inverse_metrics=inverse_metrics,
                normalization=normalization,
            )
            alternative = _ranked(
                stressed_index,
                "alternative_rank",
            )[["state", "alternative_rank"]]
            merged = baseline.merge(alternative, on="state", how="inner")
            shift = (merged["baseline_rank"] - merged["alternative_rank"]).abs()
            correlation = merged["baseline_rank"].corr(
                merged["alternative_rank"],
                method="pearson",
            )
            if not shift.empty:
                shifts.extend(shift.tolist())
            if pd.notna(correlation):
                correlations.append(float(correlation))
            coverage.append(float(stressed_index["data_coverage"].mean()))

        rows.append(
            {
                "missing_rate": rate,
                "repeats": repeats,
                "mean_absolute_rank_shift": float(np.mean(shifts)) if shifts else np.nan,
                "max_absolute_rank_shift": float(np.max(shifts)) if shifts else np.nan,
                "mean_rank_correlation": (
                    float(np.mean(correlations)) if correlations else np.nan
                ),
                "mean_data_coverage": float(np.mean(coverage)) if coverage else np.nan,
            }
        )

    return pd.DataFrame(rows)
