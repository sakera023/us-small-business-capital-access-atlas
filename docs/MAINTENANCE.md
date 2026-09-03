# Project Maintenance

## Quality gates

The project uses GitHub Actions to run:

- Ruff linting;
- pytest on Python 3.11 and 3.12; and
- a Streamlit health check.

A separate workflow validates the official Census CBP state download and uploads
machine-readable artifacts.

## Dependency maintenance

Dependabot is configured for Python and GitHub Actions dependencies.

## Release process

A release should:

1. update `pyproject.toml`, `CITATION.cff`, and `CHANGELOG.md`;
2. pass lint and tests;
3. build source and wheel distributions;
4. validate distributions;
5. create a versioned GitHub release; and
6. update the research roadmap when a planned milestone is complete.

## Public app

The Streamlit deployment tracks the `main` branch. Production-facing changes should be
covered by tests and the smoke-test workflow.

## Data-source maintenance

Public-source integrations should be reviewed when:

- a government URL changes;
- a new reference year becomes available;
- field definitions change;
- geographic identifiers change; or
- a source publishes an erratum.

## Corrections

Material source, methodology, or transformation corrections should be documented in the
changelog and, when appropriate, in release notes.
