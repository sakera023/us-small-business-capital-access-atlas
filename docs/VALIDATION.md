# Validation and Robustness Framework

## Purpose

The Atlas includes validation diagnostics because geographic rankings can be sensitive to
data coverage, indicator selection, transformations, and weights.

A professional place-based index should demonstrate not only how a score is calculated,
but also how stable the result is under reasonable alternative specifications.

## Current diagnostics

### Data-quality report

`metric_quality_report` summarizes:

- total rows;
- valid numeric values;
- missing values;
- coverage rate;
- number of unique numeric values;
- minimum;
- median; and
- maximum.

This report is intended to identify fields that are too sparse or poorly behaved for use
in a map or index.

### Leave-one-metric-out sensitivity

`leave_one_metric_out_sensitivity` rebuilds an index after omitting each component in
turn and reports:

- states compared;
- mean absolute rank shift;
- maximum absolute rank shift; and
- rank correlation with the baseline specification.

Large rank shifts indicate that a composite is highly dependent on one component and
should be interpreted cautiously.

## Validation principles

Before a formal Capital Access Opportunity Index is released, the project should add:

1. alternative normalization methods;
2. alternative weight scenarios;
3. missing-data stress tests;
4. geographic holdout/stability checks;
5. year-over-year stability;
6. correlation and redundancy analysis;
7. comparison with external economic-development indicators; and
8. independent methodological review.

## What validation does not establish

Robustness analysis can show that a result is stable under specified analytical choices.
It does not establish causality, legal discrimination, policy effectiveness, or
applicant-level creditworthiness.
