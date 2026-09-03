# Reproducible Public-Data and Index Validation Report

## Scope

The repository includes an automated workflow that validates the official U.S. Census
County Business Patterns 2023 state and county downloads and produces machine-readable
robustness diagnostics for the exploratory composite-index methodology.

## Public-data workflow

The workflow:

1. downloads the official Census CBP state ZIP;
2. extracts all-industry state totals;
3. downloads the official Census CBP county ZIP;
4. extracts all-industry county totals;
5. normalizes state/county FIPS identifiers;
6. prepares establishments, employment, annual payroll, and first-quarter payroll;
7. calculates county high-level-sector establishment HHI; and
8. writes coverage and distribution diagnostics.

## Composite-index robustness workflow

Using official CBP state totals as a transparent methodological benchmark, the workflow
also compares:

- percentile normalization;
- standard z-score normalization;
- winsorized z-score normalization;
- robust median/MAD z-score normalization;
- leave-one-component-out scenarios;
- one-component weight-emphasis scenarios; and
- 5%, 10%, and 20% missing-data stress scenarios.

The CBP metrics in this benchmark are business-scale variables. The benchmark tests
**method sensitivity**; it is not presented as a validated substantive capital-access
index.

## Reproduce

```bash
pip install -r requirements-dev.txt
python scripts/run_cbp_validation.py
python scripts/run_index_robustness.py
```

## Machine-readable outputs

```text
validation/cbp_2023_state_totals.csv
validation/cbp_2023_state_quality.csv
validation/cbp_2023_county_totals.csv
validation/cbp_2023_county_quality.csv
validation/cbp_2023_county_industry_concentration.csv
validation/index_leave_one_out.csv
validation/index_normalization_sensitivity.csv
validation/index_weight_sensitivity.csv
validation/index_missing_data_stress.csv
validation/index_normalization_ranks.csv
validation/index_normalization_rank_correlation.csv
```

GitHub Actions uploads the complete `validation/` directory as a versioned workflow
artifact.

## Interpretation

This process validates retrieval, transformation, completeness, and sensitivity behavior.
It does not independently audit Census methodology and does not establish causal or legal
conclusions.

Independent expert review remains an external milestone and will only be marked complete
when a real reviewer provides verifiable feedback.


## CDFI correction and verification — 2026-09-03

A live validation review identified that selecting a workbook sheet only by the share of
recognized state values could choose a state-summary sheet rather than the institution
roster.

The integration was strengthened to require an organization-name column and prefer the
institution-level sheet with the greatest number of recognized organization-state rows.
A live sanity threshold also prevents suspiciously small lists from passing validation.

Validation run:
https://github.com/sakera023/us-small-business-capital-access-atlas/actions/runs/33741066574

Observed in that run:

- CDFI worksheet: `List of Certified CDFIs`;
- states / District of Columbia represented: 51; and
- institution-level Certified CDFIs represented: 1,191.

This figure is a dated validation result, not a permanent count. The CDFI Fund updates the
official certification list over time.
