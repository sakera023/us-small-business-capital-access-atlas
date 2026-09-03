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

The Atlas retrieves the official Excel workbook from the SBA public distribution path and
exposes state-level numeric measures for mapping, comparison, data-quality review, and the
exploratory Index Lab.

### U.S. Census Bureau — County Business Patterns 2023

**Publisher:** U.S. Census Bureau  
**Official dataset page:** https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html  
**State ZIP:** https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23st.zip  
**County ZIP:** https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23co.zip  
**Developer documentation:** https://www.census.gov/data/developers/data-sets/cbp-zbp/cbp-api.html  
**Reference year:** 2023  
**Geography:** State and county/county equivalent  
**Atlas status:** Integrated

County Business Patterns covers establishments with paid employees and publishes
establishments, employment during the week of March 12, first-quarter payroll, and annual
payroll with industry/geographic detail.

The Atlas:

- loads the downloadable state and county ZIP files without requiring a Census API key;
- normalizes state and county FIPS codes;
- prepares one all-industry total row per state and county;
- supports state-to-county drill-down; and
- calculates a county industry-concentration HHI from high-level sector establishment
  shares where the required rows are available.

### U.S. Census Bureau — TIGERweb 2023 generalized county boundaries

**Publisher:** U.S. Census Bureau  
**Layer:** Generalized ACS 2023 State/County MapServer, Counties 5M  
**Layer URL:** https://tigerweb.geo.census.gov/arcgis/rest/services/Generalized_ACS2023/State_County/MapServer/12  
**Vintage:** January 1, 2023 generalized counties  
**Geography:** County/county equivalent  
**Atlas status:** Integrated

The Atlas queries only the selected state's county geometries at runtime and caches them in
Streamlit. This reduces map payload size and keeps CBP 2023 data aligned with a 2023 Census
county-boundary vintage.

### CDFI Fund — List of Currently Certified CDFIs

**Publisher:** Community Development Financial Institutions Fund, U.S. Department of the
Treasury  
**Official certification page:** https://www.cdfifund.gov/programs-training/certification/cdfi  
**Geography used by Atlas:** State of organization location in the published workbook  
**Atlas status:** Integrated

The application discovers the current official workbook link from the CDFI Certification
page and retains a documented fallback link for resilience.

The Atlas summarizes:

- unique Certified CDFI organizations by state;
- the number of institution types where that field is present; and
- Certified CDFIs per 10,000 Census CBP establishments when both datasets are loaded.

**Important limitation:** organization location is not the same as lending volume, branch
coverage, target-market geography, or service-area coverage. The CDFI layer is therefore a
capital-support infrastructure proxy, not a direct measure of financing availability.

## Planned sources

### U.S. Census Bureau — Annual Business Survey

Planned use:

- employer-firm characteristics;
- owner-characteristic indicators where appropriate;
- business innovation and financing context; and
- entrepreneurship research.

### Additional CDFI Fund public data

Planned work will evaluate public award, target-market, and other geography products that
can support more direct measures of community-development finance coverage without
overstating organization-location counts.

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
