# Contributing

Contributions are welcome when they improve data quality, geographic coverage,
reproducibility, methodology, accessibility, or research integrity.

Before contributing, review:

- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [DATA_GOVERNANCE.md](docs/DATA_GOVERNANCE.md)
- [ADOPTION.md](ADOPTION.md)

## Development setup

```bash
git clone https://github.com/sakera023/us-small-business-capital-access-atlas.git
cd us-small-business-capital-access-atlas
python -m venv .venv
pip install -r requirements-dev.txt
```

Run checks:

```bash
ruff check src tests scripts app.py
python -m pytest -q
```

## Public-data contributions

A new data integration should document:

- official publisher;
- official landing page and distribution/API endpoint;
- vintage/reference year;
- geography and identifiers;
- variables used;
- transformations;
- missing-data treatment;
- public-use/license status;
- known limitations; and
- whether the data are descriptive, contextual, validation, or index inputs.

Network-dependent retrieval should be separated from transformation logic so parsing can
be tested with local fixtures.

Do not commit private applicant data, proprietary financial records, credentials, or
personally identifiable information.

## Methodology contributions

For index or ranking changes, document:

- construct/indicator rationale;
- directionality;
- normalization;
- weighting;
- missingness;
- sensitivity;
- geographic coverage;
- validation plan; and
- interpretation limits.

## Documentation and examples

New major functionality should include at least one of:

- a tested example;
- a Jupyter notebook;
- a case study;
- a methodology note; or
- a source/provenance update.

## Pull requests

A pull request should:

1. describe the research or engineering purpose;
2. include tests for new logic;
3. update documentation when behavior changes;
4. avoid unsupported claims; and
5. pass GitHub Actions CI.

External contributors are especially welcome to work on county CBP integration, CDFI
geography, independent replication, methodology review, and accessibility.
