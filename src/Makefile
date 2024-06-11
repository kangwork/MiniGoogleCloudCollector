# Makefile for the MiniGoogleCloudCollector project

venv: pkg/requirements.txt
	python3.12 -m venv venv
	. venv/bin/activate; pip install -r pkg/requirements.txt

run: venv main.py $(shell find . -name "*.py")
	python3.12 main.py 'y';

.PHONY: clean

clean:
	find . -name "__pycache__" -exec rm -rf {} \;