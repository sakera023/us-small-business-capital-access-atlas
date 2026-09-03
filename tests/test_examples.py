import json

NOTEBOOKS = [
    "examples/01_sba_state_atlas.ipynb",
    "examples/02_census_cbp_state_context.ipynb",
    "examples/03_index_sensitivity.ipynb",
    "examples/04_data_quality_and_provenance.ipynb",
]


def test_example_notebooks_are_valid_notebook_documents():
    assert len(NOTEBOOKS) == 4

    for notebook_path in NOTEBOOKS:
        with open(notebook_path, encoding="utf-8") as notebook_file:
            payload = json.load(notebook_file)

        assert payload["nbformat"] == 4
        assert payload["cells"]
        assert any(cell.get("cell_type") == "markdown" for cell in payload["cells"])
        assert any(cell.get("cell_type") == "code" for cell in payload["cells"])
