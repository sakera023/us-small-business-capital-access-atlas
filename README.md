# U.S. Small Business Capital Access Atlas

[![CI](https://github.com/sakera023/us-small-business-capital-access-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/sakera023/us-small-business-capital-access-atlas/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
[![Citation](https://img.shields.io/badge/Citation-CFF-blue)](CITATION.cff)

An open-source **geospatial research platform for measuring and visualizing small-business
capital-access conditions across the United States** using authoritative public data.

The Atlas is designed to help researchers, economic-development practitioners, educators,
and policy analysts examine how entrepreneurial activity, business scale, financing
infrastructure, and regional economic conditions vary across states and communities.

## Research objective

The project asks a national-scale question:

> **Where do small businesses appear to face the largest gaps between entrepreneurial
> activity, economic opportunity, and access to capital-support infrastructure?**

Rather than making applicant-level lending predictions, this repository focuses on
**place-based measurement and public-data analysis**.

## How this project differs from Equitable Capital Optimization AI

| Project | Primary focus |
| --- | --- |
| Equitable Capital Optimization AI | Predictive modeling, fairness auditing, explainability, and capital-allocation simulation |
| **U.S. Small Business Capital Access Atlas** | Public-data integration, geographic measurement, regional comparison, and capital-access mapping |

The projects are complementary but methodologically separate.

## Initial capabilities

- official SBA state small-business statistics integration;
- live discovery of the current SBA workbook through the SBA open-data catalog;
- automatic U.S. state-name normalization;
- automatic detection of state-level numeric measures;
- interactive U.S. choropleth maps;
- state ranking and comparison tables;
- downloadable cleaned state-level CSV extracts;
- transparent public-data provenance;
- an explicit methodology for a future **Capital Access Opportunity Index**;
- reproducible tests and GitHub Actions CI.

## Authoritative public-data roadmap

The Atlas is being built around public U.S. sources rather than private applicant data.

| Source | Intended use | Status |
| --- | --- | --- |
| U.S. Small Business Administration, Office of Advocacy | Small-business counts, employment, job creation, ownership and state profiles | **Integrated** |
| U.S. Census Bureau, County Business Patterns | Establishments, employment and payroll by geography/industry | Planned |
| U.S. Census Bureau, Annual Business Survey | Employer-firm and owner-characteristic indicators | Planned |
| CDFI Fund | Community-development finance institutions and investment geography | Planned |
| Bureau of Labor Statistics | Labor-market context | Planned |
| Bureau of Economic Analysis | Regional income/output context | Planned |

See [Data Sources](docs/DATA_SOURCES.md).

## Responsible interpretation

This repository analyzes **aggregate geographic data**.

It does **not**:

- determine whether an individual or business should receive credit;
- estimate a real applicant's approval probability;
- infer protected characteristics;
- prove discrimination or causation from map differences;
- treat an index score as a regulatory or legal finding.

A place-based score is a research summary of selected public indicators and is only as
valid as its source data, transformations, weighting choices, and geographic coverage.

## Application

The Streamlit application is in `app.py`.

Run locally:

```bash
git clone https://github.com/sakera023/us-small-business-capital-access-atlas.git
cd us-small-business-capital-access-atlas
python -m venv .venv
```

Activate the environment and install:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repository structure

```text
.
├── app.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── capital_access_atlas/
│       ├── __init__.py
│       ├── geography.py
│       ├── indicators.py
│       └── public_data.py
├── tests/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_SOURCES.md
│   ├── INDEX_METHODOLOGY.md
│   └── RESEARCH_ROADMAP.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── CITATION.cff
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Capital Access Opportunity Index

A future version of the Atlas will publish a reproducible composite index at state and,
where data quality permits, county level.

The index is intended to organize indicators into transparent dimensions such as:

1. **entrepreneurial activity**;
2. **business scale and employment**;
3. **capital-support infrastructure**;
4. **economic opportunity**; and
5. **structural access constraints**.

No single composite score will be presented without the underlying component values,
source year, transformation, missing-data treatment, and sensitivity analysis.

See [Index Methodology](docs/INDEX_METHODOLOGY.md).

## Citation

If this software contributes to research or teaching, cite the repository using
[CITATION.cff](CITATION.cff). The associated data sources should also be cited separately.

## Contributing

External contributions are welcome, especially for authoritative public-data integration,
geographic validation, reproducibility, accessibility, and methodology review.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).

## Maintainer

**Sakera Begum**
