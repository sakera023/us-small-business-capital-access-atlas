# Reproducible Public-Data Validation Report

## Scope

The repository includes an automated validation workflow for the official U.S. Census
County Business Patterns 2023 state file.

The workflow:

1. downloads the official Census state ZIP;
2. identifies the data member inside the archive;
3. normalizes columns;
4. extracts all-industry state totals;
5. maps state FIPS codes to abbreviations;
6. prepares establishments, employment, annual payroll, and first-quarter payroll where
   present; and
7. writes a machine-readable data-quality report.

## Reproduce

```bash
pip install -r requirements-dev.txt
python scripts/run_cbp_validation.py
```

Outputs:

```text
validation/cbp_2023_state_totals.csv
validation/cbp_2023_quality_report.csv
```

GitHub Actions also uploads these files as workflow artifacts.

## Validation fields

The quality report records:

- row count;
- valid values;
- missing values;
- coverage rate;
- unique numeric values;
- minimum;
- median; and
- maximum.

## Interpretation

This workflow validates retrieval and transformation behavior. It does not independently
audit Census methodology and does not establish that a public indicator is appropriate for
a causal claim or an applicant-level decision.

## Future validation

Planned extensions include county-level coverage checks, year-over-year comparisons,
source-vintage consistency, composite-index sensitivity, and independent replication.
