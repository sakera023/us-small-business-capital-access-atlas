# Data Governance and Research Integrity

## Public-data policy

The Atlas is designed around authoritative aggregate public data. Private applicant-level
financial records should not be committed to the repository.

## Required provenance

Every integrated source should document:

1. publisher;
2. official source URL;
3. data vintage/reference period;
4. geography;
5. fields used;
6. transformations;
7. missing-data treatment;
8. public-use/license status; and
9. known limitations.

## Reproducibility

Transformations used in published maps or composite scores should be implemented in code,
tested, and documented.

## Versioning

Material methodology or data-source changes should be recorded in the changelog and
released with a version identifier.

## Responsible claims

Descriptive geographic differences should not be described as causal effects. Composite
scores should not be presented as legal findings, underwriting recommendations, or
validated measures of discrimination.

## Corrections

If a source link, field mapping, transformation, or interpretation is found to be wrong,
the correction should be documented through a commit, issue, or release note.
