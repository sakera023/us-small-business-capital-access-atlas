# Capital Access Opportunity Index — Methodology

## Status

**Research prototype. Not an official score.**

The long-term Atlas will support a transparent composite index designed to summarize
multiple place-based indicators of entrepreneurial activity and capital-access context.

## Proposed dimensions

### 1. Entrepreneurial activity

Examples:

- number of small businesses;
- establishments per capita;
- business formation indicators;
- small-business employment.

### 2. Business scale and employment

Examples:

- small-business employment share;
- annual payroll;
- employment growth;
- job creation.

### 3. Capital-support infrastructure

Examples:

- CDFI presence;
- community-development lending infrastructure;
- business-support institutions;
- potentially relevant public lending-program geography.

### 4. Economic opportunity

Examples:

- regional income;
- employment conditions;
- industry diversity;
- business growth.

### 5. Structural access constraints

Examples:

- rurality;
- persistent poverty or low-income geography;
- limited financial-institution coverage;
- broadband/digital-access context where an authoritative source is available.

## Scoring approach

The current Index Lab converts each selected numeric component to a percentile-based
0–100 score. Users can:

- choose component measures;
- assign non-negative weights; and
- reverse measures where lower raw values represent a more favorable outcome.

The composite score is the weighted average of available component scores.

## Why percentile scoring

Percentile scoring is transparent and easy to interpret, but it has limitations:

- scores are relative to the comparison set;
- distances between percentiles do not equal distances in raw values;
- rankings can change when geography coverage changes; and
- outliers may be compressed.

Future versions should compare percentile scoring with z-score standardization,
winsorization, and other robust transformations.

## Current robustness diagnostic

The public Index Lab includes **leave-one-metric-out sensitivity analysis**. For every
selected component, the Atlas rebuilds the composite without that metric and reports:

- mean absolute state-rank shift;
- maximum absolute state-rank shift; and
- rank correlation with the baseline specification.

A large rank shift is evidence that a proposed composite depends heavily on one component.
That should trigger additional methodological review rather than being hidden from users.

See [Validation and Robustness](VALIDATION.md).

## Data coverage

The implementation reports the share of component weight supported by non-missing values
for each geography. A formal index should define a minimum coverage threshold before a
score is published.

## Required validation before publishing a formal index

A formal Atlas index should include:

- documented indicator selection;
- source-year alignment;
- missing-data rules;
- sensitivity to weighting;
- sensitivity to transformations;
- geographic stability checks;
- correlation/redundancy analysis;
- external expert review;
- versioned methodology; and
- reproducible output tables.

## Current implementation status

Version 0.2.0 provides an **exploratory methodology laboratory**, not a published national
ranking. A formal Atlas index remains a future research milestone and will require
indicator finalization, source-year harmonization, sensitivity analysis, external review,
and versioned output tables.

## Interpretation boundary

A high or low score should never be interpreted by itself as proof of discrimination,
creditworthiness, policy effectiveness, or causal disadvantage.
