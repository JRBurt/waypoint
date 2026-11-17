.PHONY: test

test:
	python run_tests.py

lint:
	black .; ruff check .