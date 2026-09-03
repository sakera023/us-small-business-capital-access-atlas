# Capital Access Opportunity Index — Methodology

## Status

**Research prototype. Not an official score.**

The Atlas provides a transparent laboratory for studying how multiple place-based
indicators could be combined. It does not yet publish a formal national Capital Access
Opportunity Index.

## Proposed dimensions

### 1. Entrepreneurial activity

Examples include small-business counts, establishments per capita, business formation,
and small-business employment.

### 2. Business scale and employment

Examples include employment share, payroll, employment growth, and job creation.

### 3. Capital-support infrastructure

Examples include Certified CDFI organization presence and future measures of
community-development finance coverage.

### 4. Economic opportunity

Examples include income, labor-market conditions, industry diversity, and business growth.

### 5. Structural access constraints

Examples include rurality, low-income geography, persistent poverty, financial-institution
coverage, and digital-access context where authoritative sources permit.

## Current scoring methods

The Index Lab supports four documented normalization choices.

### Percentile

Raw values are converted to within-sample percentile scores from 0 to 100.

### Standard z-score

Values are standardized using the mean and population standard deviation and transformed
to a 0–100 normal-CDF scale.

### Winsorized z-score

Values are clipped at the 5th and 95th percentiles before standardization to reduce
sensitivity to extreme observations.

### Robust z-score

Values are centered on the median and scaled using median absolute deviation (MAD), then
mapped to the same 0–100 normal-CDF scale.

For an inverse-direction metric, the final score is reflected so that lower raw values
produce higher component scores.

## Weighting

Users assign non-negative weights. The composite score is the weighted mean of available
component scores. The implementation also reports `data_coverage`, the share of total
component weight supported by non-missing values.

## Robustness diagnostics

The Atlas now provides:

- leave-one-metric-out sensitivity;
- normalization sensitivity;
- one-component weight-emphasis sensitivity;
- deterministic missing-data stress tests; and
- normalization rank-correlation outputs.

Large rank changes indicate methodological fragility and should be reported rather than
hidden.

See [Validation and Robustness](VALIDATION.md) and
[Validation Report](VALIDATION_REPORT.md).

## Current implementation status

The current implementation is a methodology laboratory. A formal state or county index
still requires:

- final indicator dictionary;
- source-year harmonization;
- minimum coverage rules;
- indicator correlation/redundancy analysis;
- temporal stability;
- external criterion validation;
- independent methodological review; and
- versioned published output tables.

## Interpretation boundary

A high or low score should never be interpreted by itself as proof of discrimination,
creditworthiness, financing availability, policy effectiveness, or causal disadvantage.
