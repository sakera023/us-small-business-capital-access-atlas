# Contributing

Contributions are welcome when they improve data quality, geographic coverage,
reproducibility, transparency, accessibility, or research methodology.

## Development setup

```bash
git clone https://github.com/sakera023/us-small-business-capital-access-atlas.git
cd us-small-business-capital-access-atlas
python -m venv .venv
pip install -r requirements-dev.txt
```

Run checks:

```bash
ruff check src tests app.py
python -m pytest -q
```

## Public-data contributions

A new data integration should document:

- official publisher;
- official landing page/API;
- vintage/year;
- geography and geographic identifiers;
- variables used;
- transformation steps;
- missing-data treatment;
- license/public-use status; and
- known limitations.

Do not commit private applicant data, proprietary financial records, credentials, or
personally identifiable information.

## Methodology contributions

For index changes, include reasoning for:

- indicator inclusion;
- directionality;
- normalization;
- weighting;
- missingness;
- sensitivity; and
- interpretation limits.

## Pull requests

A pull request should include tests for new logic and update documentation when behavior
or methodology changes.
