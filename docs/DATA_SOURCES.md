# Data Sources

The Atlas prioritizes authoritative U.S. public datasets with documented provenance,
geographic identifiers, vintage, transformation notes, and interpretation limits.

## Integrated sources

### U.S. Small Business Administration — State Small Business Statistics 2025

**Publisher:** U.S. Small Business Administration, Office of Advocacy  
**Official landing page:** https://data.sba.gov/dataset/state-small-business-statistics-2025  
**Dataset identifier:** SBA-ADVO-CKAN-009  
**Geography:** State  
**Atlas status:** Integrated

The dataset contains statistics from the SBA 2025 Small Business Profiles, including
measures related to small-business counts, employment, job creation, and ownership.

The Atlas retrieves the official Excel workbook from the SBA's public distribution path.
It does not depend on the retired CKAN `/api/3/action/package_show` route.

### U.S. Census Bureau — County Business Patterns 2023

**Publisher:** U.S. Census Bureau  
**Official dataset page:** https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html  
**Official downloadable state file:** https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23st.zip  
**Developer documentation:** https://www.census.gov/data/developers/data-sets/cbp-zbp/cbp-api.html  
**Reference year:** 2023  
**Geography currently integrated:** State  
**Atlas status:** Integrated

County Business Patterns is an annual series covering establishments with paid employees.
The 2023 data include establishment counts, employment during the week of March 12,
first-quarter payroll, and annual payroll, with industry/geographic detail.

The Atlas uses the downloadable public state ZIP instead of requiring a Census API key.

## Planned sources

### Census County Business Patterns — County File

Planned use:

- county establishments;
- employment;
- payroll;
- industry structure;
- state/county drill-down; and
- county-level geographic validation.

### U.S. Census Bureau — Annual Business Survey

Planned use:

- employer-firm characteristics;
- owner-characteristic indicators where appropriate;
- business innovation and financing context; and
- entrepreneurship research.

### CDFI Fund

Planned use:

- certified CDFI institution locations;
- community-development finance coverage;
- geographic capital-support infrastructure; and
- rural/metropolitan comparison.

### Bureau of Labor Statistics

Planned use:

- unemployment;
- labor-force conditions;
- employment growth; and
- local labor-market context.

### Bureau of Economic Analysis

Planned use:

- regional income;
- GDP;
- personal income; and
- regional economic opportunity context.

## Source-integration standard

Every integrated dataset should document:

1. publisher;
2. official landing page and/or distribution URL;
3. data vintage/reference year;
4. geography and identifiers;
5. fields used;
6. transformations;
7. missing-value treatment;
8. public-use/license status;
9. known limitations; and
10. whether the data are descriptive, contextual, validation, or index inputs.

See [Data Governance](DATA_GOVERNANCE.md).

No private applicant-level financial records should be committed to this repository.
