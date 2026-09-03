# PyPI Publishing

## Status

The package is now published on PyPI:

https://pypi.org/project/us-small-business-capital-access-atlas/

Current published version:

`0.2.0`

Install with:

```bash
pip install us-small-business-capital-access-atlas
```

Python import namespace:

```python
import capital_access_atlas
```

## Trusted Publishing

Publishing uses **PyPI Trusted Publishing (OIDC)** through the GitHub Actions workflow:

`.github/workflows/publish-pypi.yml`

The workflow uses the GitHub environment:

`pypi`

No long-lived PyPI API token is stored in the repository.

## Release-triggered publishing

The workflow now runs automatically when a GitHub release is published and can also be
started manually with `workflow_dispatch`. This keeps the PyPI version aligned with a
versioned GitHub release while retaining a manual recovery path.

## Future release process

Before publishing a new PyPI version:

1. update the version in `pyproject.toml`;
2. update `CITATION.cff`;
3. update `CHANGELOG.md`;
4. run CI and public-data validation;
5. create a versioned GitHub release;
6. publish the GitHub release (which automatically starts the PyPI workflow);
7. verify the GitHub Actions publishing run; and
8. verify the PyPI package page and installation command.

A published PyPI version is immutable. Do not reuse a version number for different code.
