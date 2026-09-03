# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [0.3.0] - 2026-09-03

### Added

- official Census CBP 2023 county-file integration;
- county FIPS/GEOID normalization and all-industry county totals;
- state-to-county drill-down using official Census TIGERweb 2023 boundaries;
- county establishments, employment, payroll, and industry-concentration HHI;
- state-scoped county geometry caching in Streamlit;
- current Certified CDFI workbook discovery and state-level organization geography;
- Certified CDFIs per 10,000 CBP establishments contextual proxy;
- percentile, standard z-score, winsorized z-score, and robust median/MAD normalization;
- normalization, weight, omission, and missing-data sensitivity benchmarks;
- cross-normalization rank-correlation outputs;
- expanded state/county public-data validation artifacts;
- independent methodology review package;
- external-use evidence guide;
- independent replication protocol and external-use ledger;
- research outreach kit;
- Zenodo DOI archival plan.

### Changed

- public dashboard expanded with County Drill-down, CDFI Capital Support, and richer
  robustness/quality views;
- validation workflow now processes Census state and county data and index robustness;
- Certified CDFI loader now selects the institution-level worksheet instead of allowing a
  state-summary sheet to be treated as the full roster;
- CDFI live validation rejects suspiciously small institution lists;
- PyPI Trusted Publishing workflow now also runs automatically from published GitHub
  releases.

## [0.2.0] - 2026-09-03

### Added

- official U.S. Census County Business Patterns 2023 state-file integration;
- Census state FIPS normalization and all-industry state-total preparation;
- establishments, employment, annual-payroll, and first-quarter-payroll Atlas views;
- data-quality diagnostics;
- leave-one-metric-out composite-index sensitivity analysis;
- dedicated public-data validation runner and GitHub Actions workflow;
- four reproducible Jupyter research examples;
- three documented geographic research case studies;
- validation and robustness documentation;
- data-governance policy;
- academic citation guide and CodeMeta metadata;
- research impact and external-adoption framework;
- community conduct standards;
- professional public dashboard with SBA and Census tabs;
- versioned v0.2.0 release preparation;
- published version 0.2.0 to PyPI through GitHub OIDC Trusted Publishing.

### Changed

- expanded CI to lint scripts;
- upgraded project and citation metadata to version 0.2.0;
- revised documentation to distinguish descriptive geography from causal or
  applicant-level claims;
- corrected SBA source documentation to reflect the verified public workbook route.

## [0.1.0] - 2026-09-03

### Added

- professional Python package structure;
- official SBA State Small Business Statistics integration;
- automatic state-field and numeric-measure detection;
- interactive national U.S. choropleth mapping;
- state ranking and comparison workflow;
- downloadable cleaned state extracts;
- exploratory Capital Access Opportunity Index Lab;
- transparent percentile-based composite scoring;
- data-source, architecture, methodology, and roadmap documentation;
- unit tests and Streamlit deployment configuration;
- citation, contribution, security, and MIT license files;
- public Streamlit deployment at `capital-access-atlas-sakera.streamlit.app`.
