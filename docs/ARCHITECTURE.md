# Architecture

The Atlas separates retrieval, geographic cleaning, index construction, and presentation.

```text
Official Public Sources
        |
        v
  Source Connectors
        |
        v
 Data / Geography Cleaning
        |
        +------------------+
        |                  |
        v                  v
 State/County Metrics   Index Components
        |                  |
        +--------+---------+
                 |
                 v
        Geographic Atlas
                 |
        +--------+--------+
        |                 |
        v                 v
 Interactive Maps     Rankings/Exports
```

## Current modules

- `public_data.py` — official source discovery and retrieval;
- `geography.py` — state normalization, numeric cleaning, and map-ready aggregation;
- `indicators.py` — transparent percentile scoring and weighted index construction;
- `app.py` — Streamlit dashboard.

## Design principles

1. Public source provenance remains visible.
2. Raw metrics remain available alongside composite scores.
3. Retrieval logic is separated from analysis logic.
4. Tests avoid network dependence.
5. Composite rankings remain configurable and inspectable.
