# Data Sources

The Atlas prioritizes authoritative U.S. public datasets with documented provenance.

## Integrated source

### SBA State Small Business Statistics 2025

**Publisher:** U.S. Small Business Administration, Office of Advocacy  
**Official landing page:** https://data.sba.gov/dataset/state-small-business-statistics-2025

The dataset includes key statistics from SBA state small-business profiles, including
small-business counts, employment, job creation, and ownership indicators.

The application resolves the current Excel resource through the SBA CKAN open-data
catalog at runtime rather than storing a stale copy in the repository.

## Planned sources

### U.S. Census Bureau — County Business Patterns

Planned use:

- number of establishments;
- employment;
- annual payroll;
- industry structure;
- county/state geographic comparison.

Official developer documentation:
https://www.census.gov/data/developers/data-sets/cbp-zbp/cbp-api.html

### U.S. Census Bureau — Annual Business Survey

Planned use:

- employer-business characteristics;
- ownership characteristics;
- innovation and financing-related contextual measures where appropriate.

### CDFI Fund

Planned use:

- CDFI institution locations;
- community-development finance coverage;
- geographic comparison of financing infrastructure.

### Bureau of Labor Statistics

Planned use:

- unemployment;
- labor-force conditions;
- local labor-market context.

### Bureau of Economic Analysis

Planned use:

- regional income;
- GDP;
- personal income and related economic context.

## Source-integration standard

Every integrated dataset should document:

1. publisher;
2. official landing page or API;
3. data vintage/year;
4. geography;
5. fields used;
6. transformations;
7. missing-value treatment;
8. license or public-use terms;
9. known limitations; and
10. whether the data are descriptive, contextual, or used in an index.

No private applicant-level financial records should be committed to this repository.
