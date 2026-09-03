# Architecture

The Atlas separates authoritative-source retrieval, geographic normalization,
descriptive analysis, composite-index construction, validation, and presentation.

```text
       Authoritative U.S. Public Sources
      /             |              \
     v              v               v
   SBA Excel    Census CBP ZIP   CDFI Workbook
                    |
                    v
            Census TIGERweb
              County Geometry
                    |
        +-----------+-----------+
        |                       |
        v                       v
 Retrieval / Provenance   Geographic Cleaning
        |                       |
        +-----------+-----------+
                    |
                    v
      State + County Research Tables
          /         |          \
         v          v           v
       Maps      Index Lab   Data Quality
                    |
                    v
          Robustness Diagnostics
                    |
         +----------+----------+
         |                     |
         v                     v
 Rankings / Exports      Streamlit Atlas
```

## Package modules

- `public_data.py` — SBA metadata and workbook retrieval;
- `census_cbp.py` — Census state/county ZIP retrieval, FIPS normalization, county HHI,
  and TIGERweb boundary access;
- `cdfi.py` — current Certified CDFI workbook discovery and state-level summaries;
- `geography.py` — state normalization and map-ready numeric aggregation;
- `indicators.py` — transparent alternative normalization and composite scoring;
- `analysis.py` — quality, omission, normalization, weight, and missingness diagnostics;
- `app.py` — public research dashboard.

## Performance strategy

The 12.7 MB Census county archive is downloaded only when county analysis is requested.
The application reduces the raw county file to county totals and industry-concentration
outputs before storing session data.

County boundaries are queried from the official 2023 TIGERweb layer **one state at a
time** and cached for 24 hours, avoiding a national county-geometry payload on each
interaction.

## Reproducibility layer

- network-independent parser/unit tests;
- Python 3.11/3.12 CI;
- Streamlit health smoke test;
- state/county public-data validation workflow;
- index robustness benchmark;
- machine-readable GitHub Actions artifacts;
- notebooks, case studies, source documentation, and review materials.

## Design principles

1. provenance first;
2. state/county geography retained explicitly;
3. retrieval separated from transformations;
4. raw measures remain visible beside composite scores;
5. robustness is measured rather than assumed;
6. CDFI organization location is not misrepresented as service-area coverage;
7. aggregate research is separated from applicant-level decision making; and
8. external review/adoption is never self-certified.
