install:
	python -m pip install -e .[dev]

test:
	pytest -q

pipeline:
	python -m datapulse.pipeline

dashboard:
	streamlit run dashboard/app.py

sample:
	python scripts/seed_sample.py
