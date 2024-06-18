# Makefile for the MiniGoogleCloudCollector project
requirements = ../pkg/pip_requirements.txt
venv = ../venv
requirements_stamp = requirements.timestamp

$(venv):
	python -m venv $(venv);

$(requirements_stamp): $(requirements) $(venv)
	$(venv)/bin/pip install -r $(requirements)
	touch $(requirements_stamp);

activate: $(venv)
	@echo "Activate your venv by running 'source $(venv)/bin/activate'";

run: main.py $(shell find . -name "*.py") activate $(requirements_stamp) 
	export GOOGLE_APPLICATION_CREDENTIALS="utils/key.json";
	python main.py;

.PHONY: clean activate

clean:
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rf ../__pycache__;
	rm -f $(requirements_stamp);