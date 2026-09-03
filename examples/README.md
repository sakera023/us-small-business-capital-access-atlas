# Reproducible Examples

These notebooks demonstrate the Atlas research workflow using public aggregate data and
transparent methodology.

| Notebook | Purpose |
| --- | --- |
| [01 SBA State Atlas](01_sba_state_atlas.ipynb) | Load the official SBA workbook, identify state-level measures, and prepare map-ready data. |
| [02 Census CBP State Context](02_census_cbp_state_context.ipynb) | Load the Census 2023 County Business Patterns state file and inspect establishments, employment, and payroll. |
| [03 Index Sensitivity](03_index_sensitivity.ipynb) | Build a transparent composite index and test leave-one-metric-out rank sensitivity. |
| [04 Data Quality and Provenance](04_data_quality_and_provenance.ipynb) | Review metric completeness, source metadata, and responsible-use boundaries. |

## Run locally

```bash
pip install -e ".[dev]"
pip install jupyter
jupyter lab
```

The notebooks require internet access when they download official SBA or Census files.

## Interpretation

The examples analyze aggregate geographic statistics. They are not underwriting tools and
should not be interpreted as proof of causation, discrimination, or individual
creditworthiness.
