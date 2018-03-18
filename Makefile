venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3.6 -m venv venv
	venv/bin/pip install -r requirements.txt
	touch venv/bin/activate

test: venv
	EAS_SETTINGS="eas/settings/tests.py" venv/bin/python -m pytest tests

coverage:
	venv/bin/python -m pytest tests --cov=eas --cov-report=term-missing

run: venv
	venv/bin/python ./run.py
