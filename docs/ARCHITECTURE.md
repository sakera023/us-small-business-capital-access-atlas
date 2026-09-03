# Architecture

The Atlas separates public-data retrieval, geographic normalization, descriptive analysis,
composite-index construction, validation, and presentation.

```text
Official U.S. Public Sources
   |                    |
   |                    |
   v                    v
 SBA Workbook        Census CBP ZIP
   |                    |
   +---------+----------+
             |
             v
   Retrieval + Provenance
             |
             v
 Geographic / Numeric Cleaning
             |
      +------+------+
      |             |
      v             v
 Map-Ready Data  Index Components
      |             |
      |             v
      |      Robustness Diagnostics
      |             |
      +------+------+
             |
             v
     Streamlit Research UI
       /      |       \
      v       v        v
    Maps   Rankings   Exports
```

## Package modules

- `public_data.py` — SBA source metadata and workbook retrieval;
- `census_cbp.py` — Census CBP ZIP retrieval, parsing, FIPS normalization, and state totals;
- `geography.py` — state normalization, numeric cleaning, metric discovery, and map-ready
  aggregation;
- `indicators.py` — transparent percentile scoring and weighted composite construction;
- `analysis.py` — data-quality and leave-one-metric-out sensitivity diagnostics;
- `app.py` — public Streamlit research dashboard.

## Reproducibility layer

- `tests/` — unit tests with network-independent fixtures;
- `examples/` — Jupyter research walkthroughs;
- `scripts/run_cbp_validation.py` — reproducible official-data validation runner;
- GitHub Actions CI — Python 3.11/3.12, linting, tests, and Streamlit smoke testing;
- Public Data Validation workflow — downloadable machine-readable validation artifacts.

## Design principles

1. **Provenance first:** every public source has a named publisher and official URL.
2. **Separation of concerns:** retrieval, transformation, scoring, validation, and UI are
   implemented separately.
3. **Network-independent tests:** parsing and transformation tests use fixtures rather than
   depending on government endpoints.
4. **Raw measures remain visible:** composite scores do not replace underlying source data.
5. **Robustness is part of the method:** index sensitivity is evaluated, not assumed.
6. **Aggregate research only:** the platform is not designed for applicant-level
   underwriting.
7. **Versioned research software:** material changes are documented and released.
