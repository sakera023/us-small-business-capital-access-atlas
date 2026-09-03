# U.S. Small Business Capital Access Atlas

[![CI](https://github.com/sakera023/us-small-business-capital-access-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/sakera023/us-small-business-capital-access-atlas/actions/workflows/ci.yml)
[![Public Data Validation](https://github.com/sakera023/us-small-business-capital-access-atlas/actions/workflows/data-validation.yml/badge.svg)](https://github.com/sakera023/us-small-business-capital-access-atlas/actions/workflows/data-validation.yml)
[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://capital-access-atlas-sakera.streamlit.app/)
[![GitHub Release](https://img.shields.io/github/v/release/sakera023/us-small-business-capital-access-atlas)](https://github.com/sakera023/us-small-business-capital-access-atlas/releases/latest)
[![Citation](https://img.shields.io/badge/Citation-CFF-blue)](CITATION.md)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Profile-4285F4?logo=googlescholar&logoColor=white)](https://scholar.google.com/citations?user=D4t4wxAAAAAJ)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

An open-source **geospatial research platform for integrating, validating, mapping, and
comparing U.S. small-business and capital-access context using authoritative public data**.

The Atlas is designed for researchers, economic-development practitioners, educators,
data scientists, and policy analysts who need a reproducible way to examine how business
activity, employment, payroll, entrepreneurial scale, and capital-support context vary
across U.S. geographies.

## Live public Atlas

**Application:** https://capital-access-atlas-sakera.streamlit.app/

The public dashboard provides:

- official SBA state-level small-business measures;
- official U.S. Census County Business Patterns state totals;
- interactive U.S. choropleths;
- state comparison workflows;
- downloadable map-ready data;
- an exploratory Capital Access Opportunity Index Lab;
- data-quality diagnostics; and
- leave-one-metric-out index sensitivity analysis.

No login or API key is required for the currently integrated public-data layers.

## Research objective

The project examines a national-scale question:

> **Where do small-business activity, economic opportunity, and capital-support context
> appear to diverge across U.S. geographies, and how robust are those patterns to data and
> methodological choices?**

The Atlas focuses on **place-based public-data measurement**, not applicant-level
underwriting.

## Authoritative public data

| Source | Current use | Status |
| --- | --- | --- |
| U.S. Small Business Administration, Office of Advocacy | State small-business counts, employment, job creation, ownership and related profile measures | **Integrated** |
| U.S. Census Bureau, County Business Patterns 2023 | State establishments, employment, annual payroll and first-quarter payroll | **Integrated** |
| U.S. Census County Business Patterns — county file | County establishments, employment, payroll and industry structure | Planned |
| CDFI Fund | Community-development finance infrastructure and geographic coverage | Planned |
| U.S. Census Annual Business Survey | Employer-firm and owner-characteristic context | Planned |
| Bureau of Labor Statistics | Labor-market context | Planned |
| Bureau of Economic Analysis | Regional income and output context | Planned |

See [Data Sources](docs/DATA_SOURCES.md) and
[Data Governance](docs/DATA_GOVERNANCE.md).

## Core research capabilities

### Public-data engineering

- direct retrieval from official U.S. government distribution endpoints;
- ZIP/Excel ingestion;
- state FIPS and state-name normalization;
- numeric-field cleaning;
- state-level aggregation;
- source metadata preservation; and
- downloadable clean extracts.

### Geographic analysis

- U.S. state choropleths;
- interactive metric selection;
- state rankings;
- multi-state comparison;
- SBA and Census source separation; and
- explicit source/vintage labels.

### Transparent composite-index research

The **Capital Access Opportunity Index Lab** supports:

- percentile-based 0–100 component scoring;
- user-defined non-negative weights;
- inverse-direction metrics;
- data-coverage reporting; and
- leave-one-metric-out rank sensitivity.

A composite score is never presented without its component inputs and methodology.

### Validation and reproducibility

The repository includes:

- Python 3.11 and 3.12 CI;
- unit tests for geography, public-data parsing, index logic, and validation;
- Streamlit smoke testing;
- a dedicated public-data validation workflow;
- machine-readable validation artifacts;
- reproducible Jupyter examples; and
- documented case studies.

See [Validation and Robustness](docs/VALIDATION.md) and
[Reproducible Public-Data Validation](docs/VALIDATION_REPORT.md).

## Architecture

```text
Authoritative U.S. Public Sources
          |
          v
   Retrieval / Provenance
          |
          v
Geographic + Numeric Cleaning
       /          \
      v            v
Map-Ready Data   Index Components
      |            |
      +------v-----+
             |
             v
     Validation Diagnostics
             |
       +-----+-----+
       |           |
       v           v
Interactive Maps  Rankings / Exports
       |
       v
 Public Streamlit Atlas
```

See [Architecture](docs/ARCHITECTURE.md).

## Reproducible examples

Four notebooks demonstrate the research workflow:

1. [SBA State Atlas](examples/01_sba_state_atlas.ipynb)
2. [Census CBP State Context](examples/02_census_cbp_state_context.ipynb)
3. [Index Sensitivity](examples/03_index_sensitivity.ipynb)
4. [Data Quality and Provenance](examples/04_data_quality_and_provenance.ipynb)

See the [examples guide](examples/README.md).

## Documented case studies

The repository includes methodological case studies that demonstrate how to use the Atlas
without making unsupported causal or applicant-level claims:

1. [Mid-Atlantic State Comparison](docs/case-studies/01_mid_atlantic_comparison.md)
2. [Rural and Appalachian Research Workflow](docs/case-studies/02_rural_appalachian_workflow.md)
3. [High-Growth State Business Context](docs/case-studies/03_high_growth_state_context.md)

See the [case study index](docs/case-studies/README.md).

## Quick start

Clone and install:

```bash
git clone https://github.com/sakera023/us-small-business-capital-access-atlas.git
cd us-small-business-capital-access-atlas
python -m venv .venv
pip install -r requirements.txt
```

Run the public-data dashboard locally:

```bash
streamlit run app.py
```

Development setup:

```bash
pip install -r requirements-dev.txt
ruff check src tests scripts app.py
python -m pytest -q
```

Run the reproducible Census validation workflow locally:

```bash
python scripts/run_cbp_validation.py
```

## Research and responsible-use boundary

The Atlas analyzes **aggregate geographic data**.

It does **not**:

- determine whether an individual or business should receive credit;
- estimate a real applicant's approval probability;
- infer protected characteristics;
- prove discrimination or causation from map differences;
- establish policy effectiveness from descriptive correlations; or
- treat a composite score as a legal, regulatory, or underwriting finding.

Geographic and index results are only as reliable as their source definitions, vintage,
coverage, transformations, and sensitivity to analytical choices.

## Academic citation and research metadata

The repository includes:

- [CITATION.cff](CITATION.cff) for GitHub's **Cite this repository** feature;
- [CITATION.md](CITATION.md) with a recommended citation and BibTeX;
- [codemeta.json](codemeta.json) for machine-readable research-software metadata; and
- explicit instructions to cite the underlying SBA and Census datasets separately.

No DOI is claimed unless a verified DOI is minted through an external research-software
archive.

## External use and research impact

Genuine outside use is encouraged through:

- public forks and derivative repositories;
- research/adoption issue reports;
- external pull requests;
- independent replication;
- citations;
- public teaching use; and
- documented organizational testing.

See [ADOPTION.md](ADOPTION.md) and
[Research Impact and Adoption Framework](docs/RESEARCH_IMPACT.md).

The project does not manufacture stars, users, citations, testimonials, or adoption claims.

## Research roadmap

The roadmap progresses from the current state-level atlas toward:

1. county-level Census business structure;
2. CDFI/community-finance geography;
3. rural and metropolitan comparisons;
4. a validated state/county Capital Access Opportunity Index; and
5. independent replication and public research dissemination.

See [Research Roadmap](docs/RESEARCH_ROADMAP.md).

## Repository structure

```text
.
├── app.py
├── src/capital_access_atlas/
│   ├── analysis.py
│   ├── census_cbp.py
│   ├── geography.py
│   ├── indicators.py
│   └── public_data.py
├── scripts/
│   └── run_cbp_validation.py
├── examples/
├── tests/
├── docs/
│   ├── case-studies/
│   ├── ARCHITECTURE.md
│   ├── DATA_GOVERNANCE.md
│   ├── DATA_SOURCES.md
│   ├── INDEX_METHODOLOGY.md
│   ├── RESEARCH_IMPACT.md
│   ├── RESEARCH_ROADMAP.md
│   ├── VALIDATION.md
│   └── VALIDATION_REPORT.md
├── .github/workflows/
├── ADOPTION.md
├── CITATION.cff
├── CITATION.md
├── codemeta.json
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Related research software

This Atlas complements
[Equitable Capital Optimization AI](https://github.com/sakera023/equitable-capital-optimization-ai),
which focuses on predictive modeling, explainability, fairness auditing, and simulated
capital allocation. The Atlas remains methodologically separate and focuses on public,
place-based geographic evidence.

## Contributing

Contributions are welcome in public-data integration, geographic validation, methodology,
documentation, accessibility, and independent replication.

See [CONTRIBUTING.md](CONTRIBUTING.md) and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

MIT License. See [LICENSE](LICENSE).

## Maintainer

**Sakera Begum**
