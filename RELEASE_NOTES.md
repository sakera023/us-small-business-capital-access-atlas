# U.S. Small Business Capital Access Atlas v0.3.0

Version 0.3.0 is the Atlas's county, CDFI, robustness, and research-archival release.

## Highlights

### County-level Census CBP analysis

- official Census County Business Patterns 2023 county-file integration;
- state and county FIPS/GEOID normalization;
- county establishments, employment, annual payroll, and first-quarter payroll;
- high-level county industry-concentration HHI;
- state-to-county drill-down; and
- Census TIGERweb 2023 generalized county boundaries.

### Certified CDFI capital-support geography

- current official Certified CDFI workbook integration;
- institution-level worksheet selection;
- state-level Certified CDFI organization summaries;
- Certified CDFIs per 10,000 CBP establishments contextual proxy; and
- live-data sanity checks that reject suspiciously small institution lists.

The merged validation workflow represented 1,191 institution-level Certified CDFI
organizations across the 50 states and District of Columbia on 2026-09-03. The official
certification list is dynamic and later counts may differ.

### Robustness and reproducibility

- percentile, standard z-score, winsorized z-score, and robust median/MAD normalization;
- leave-one-metric-out sensitivity;
- one-component weight-emphasis sensitivity;
- missing-data stress testing;
- cross-normalization rank-correlation outputs;
- state/county public-data validation artifacts; and
- Python 3.11/3.12 CI plus Streamlit smoke testing.

### Research dissemination

- PyPI Trusted Publishing triggered from published GitHub releases;
- independent replication protocol;
- verified external-use ledger;
- research outreach kit;
- independent methodology-review package; and
- Zenodo GitHub archival integration prepared for DOI minting.

## Public application

https://capital-access-atlas-sakera.streamlit.app/

## Python package

```bash
pip install us-small-business-capital-access-atlas==0.3.0
```

## Responsible-use boundary

The Atlas analyzes aggregate geographic public data. It is not an applicant-level
underwriting system and should not be used to make individual lending, investment, credit,
or eligibility decisions.

Geographic associations and composite rankings do not by themselves establish causation,
discrimination, service-area coverage, or policy effectiveness.
