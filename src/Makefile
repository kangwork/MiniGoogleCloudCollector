# Makefile for the MiniGoogleCloudCollector project

requirements = ../pkg/pip_requirements.txt

venv: $(requirements)
	python -m venv venv
	source venv/bin/activate
	pip install -r $(requirements);

# this should be run after the venv target
run: main.py $(shell find . -name "*.py")
	python main.py 'y';

.PHONY: clean

clean:
	find . -name "__pycache__" -exec rm -rf {} \;