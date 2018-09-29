setpath:
	PYTHONPATH=.

test: setpath
	pytest -v tests.py
