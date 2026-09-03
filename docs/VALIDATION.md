# Validation and Robustness Framework

## Purpose

Geographic rankings can be sensitive to coverage, indicator selection, transformations,
weights, and missing data. The Atlas therefore treats robustness testing as part of the
method rather than as an optional presentation step.

## Current diagnostics

### Data-quality report

`metric_quality_report` reports:

- total rows;
- valid and missing values;
- coverage rate;
- unique numeric values;
- minimum;
- median; and
- maximum.

### Leave-one-metric-out sensitivity

`leave_one_metric_out_sensitivity` rebuilds an index after omitting each component and
reports mean/max absolute rank shift and rank correlation with the baseline.

### Alternative normalization benchmark

The Atlas currently supports four 0–100 transformations:

1. percentile ranks;
2. standard z-scores mapped through the normal CDF;
3. 5th/95th-percentile winsorized z-scores; and
4. median/MAD robust z-scores.

`normalization_sensitivity_benchmark` compares state ranks across all four methods.

### Weight sensitivity

`weight_sensitivity_benchmark` emphasizes each component in turn and measures the
resulting rank changes.

### Missing-data stress test

`missing_data_stress_test` removes metric observations at deterministic random rates and
reports:

- mean absolute rank shift;
- maximum rank shift;
- mean rank correlation; and
- mean component-weight coverage.

The default research benchmark evaluates 5%, 10%, and 20% missingness across repeated
runs.

### Rank-correlation matrix

The reproducible robustness script writes the full state-rank table for each normalization
method and a cross-method rank-correlation matrix.

## Public-data validation

The automated validation workflow now processes both Census CBP state and county files and
writes:

- state totals;
- state quality report;
- county totals;
- county quality report; and
- county industry-concentration results.

The same workflow runs the composite-index robustness benchmark and uploads all outputs as
GitHub Actions artifacts.

## Remaining validation work

A formal Capital Access Opportunity Index still requires:

- final indicator selection;
- source-year harmonization;
- correlation/redundancy analysis among candidate constructs;
- year-over-year stability;
- external criterion comparisons;
- geographic stability/holdout analysis; and
- genuine independent methodological review.

## What validation does not establish

Robustness analysis can show stability under specified analytical choices. It does not
establish causality, legal discrimination, policy effectiveness, service-area coverage, or
applicant-level creditworthiness.


## Certified CDFI live-source validation

The CDFI workbook contains multiple possible worksheets. A state summary can have perfect
state-code coverage while containing only one row per state, so state-recognition rate
alone is not sufficient to identify the institution-level roster.

The loader now:

1. identifies a state column;
2. requires an organization-name field;
3. prefers the candidate worksheet with the largest number of recognized organization
   rows; and
4. rejects a candidate with fewer than 100 recognized institution-state rows.

The live validation script independently applies the same sanity threshold.

On 2026-09-03, workflow run
https://github.com/sakera023/us-small-business-capital-access-atlas/actions/runs/33741066574
selected the official **List of Certified CDFIs** worksheet and represented 1,191
Certified CDFI organizations across the 50 states and District of Columbia. The official
list is dynamic, so later counts may differ.
