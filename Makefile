venv: venv/bin/activate

venv/bin/activate: requirements-base.txt
	test -d venv || python3.6 -m venv venv
	venv/bin/pip install -r requirements-base.txt
	touch venv/bin/activate

test: venv
	venv/bin/pip install -r requirements-test.txt
	EAS_SETTINGS="eas/settings/tests.py" venv/bin/python -m pytest tests

coverage: venv
	venv/bin/pip install -r requirements-test.txt
	EAS_SETTINGS="eas/settings/tests.py" venv/bin/python -m pytest tests --cov=eas --cov-report=term-missing

dev:
	venv/bin/pip install -r requirements-dev.txt
	EAS_SETTINGS="eas/settings/dev.py" venv/bin/gunicorn eas.wsgi:app --log-file -

run: venv
	venv/bin/python ./run.py

lint: venv
	venv/bin/python -m pylint eas
