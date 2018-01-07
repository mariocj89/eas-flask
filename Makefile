venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3.6 -m venv venv
	venv/bin/pip install -r requirements.txt
	touch venv/bin/activate

test: venv
	venv/bin/python -m pytest tests

