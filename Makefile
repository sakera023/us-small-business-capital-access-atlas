.PHONY: install dev lint test run validate build check

install:
	python -m pip install -r requirements.txt

dev:
	python -m pip install -r requirements-dev.txt

lint:
	ruff check src tests scripts app.py

test:
	python -m pytest -q

run:
	streamlit run app.py

validate:
	python scripts/run_cbp_validation.py

build:
	python -m build

check: lint test
