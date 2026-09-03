# PyPI Publishing

The repository is prepared for secure PyPI publishing through **Trusted Publishing
(OIDC)**. No long-lived PyPI API token is stored in GitHub.

## Pending publisher configuration

In PyPI Trusted Publisher Management, create a pending publisher with:

- **PyPI project name:** `us-small-business-capital-access-atlas`
- **GitHub owner:** `sakera023`
- **Repository:** `us-small-business-capital-access-atlas`
- **Workflow:** `publish-pypi.yml`
- **Environment:** `pypi`

After the publisher is configured, run the **Publish Python package to PyPI** workflow
manually from GitHub Actions.

## Package import

The distribution name is:

```text
us-small-business-capital-access-atlas
```

The Python import namespace is:

```python
import capital_access_atlas
```

## Release discipline

Before publishing a new PyPI version:

1. update `pyproject.toml`;
2. update `CITATION.cff`;
3. update `CHANGELOG.md`;
4. pass CI;
5. create a versioned GitHub release; and
6. publish the exact tested version.

Do not republish a version number with different code.
