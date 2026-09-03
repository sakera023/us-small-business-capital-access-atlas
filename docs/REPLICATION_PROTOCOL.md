# Independent Replication Protocol

## Purpose

This protocol gives an external researcher, instructor, developer, or reviewer a short,
verifiable way to reproduce core Atlas outputs without relying on screenshots or claims
from the maintainer.

## Environment

Recommended:

- Python 3.11 or 3.12;
- internet access to the official SBA, Census, and CDFI Fund sources; and
- a clean virtual environment.

## Install

From PyPI:

```bash
pip install us-small-business-capital-access-atlas
```

For the newest repository code:

```bash
git clone https://github.com/sakera023/us-small-business-capital-access-atlas.git
cd us-small-business-capital-access-atlas
pip install -r requirements-dev.txt
```

## Reproduce official-data validation

```bash
python scripts/run_cbp_validation.py
python scripts/run_cdfi_validation.py
python scripts/run_index_robustness.py
```

A valid run should demonstrate, at minimum:

- 51 Census CBP state rows (50 states + District of Columbia);
- more than 3,000 Census county/county-equivalent rows;
- 51 state/DC jurisdictions in the CDFI state summary;
- more than 100 institution-level Certified CDFI organizations; and
- generated robustness tables for normalization, weighting, omission, and missingness.

The Certified CDFI list is dynamic, so its exact organization count may change when the
CDFI Fund updates certification status.

## Reproduce the application

```bash
streamlit run app.py
```

Verify that the application can:

1. load SBA state data;
2. load Census state data;
3. load Census county data;
4. map a selected state's counties;
5. load the current Certified CDFI list;
6. display a CDFI state summary; and
7. run Index Lab robustness diagnostics.

## Report an independent replication

Use the repository's **Research / Adoption Report** issue template and include:

- date;
- environment / Python version;
- commit SHA or released version;
- commands run;
- whether outputs reproduced successfully;
- any discrepancies;
- a public link to your repository, notebook, report, or syllabus when available.

Independent replication is valuable even when it finds a problem. A reproducible
discrepancy should be documented rather than hidden.
