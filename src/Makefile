# Makefile for the MiniGoogleCloudCollector project
requirements = ../pkg/pip_requirements.txt
venv = ../venv
requirements_stamp = requirements.timestamp

$(venv):
	python -m venv $(venv);

$(requirements_stamp): $(venv) $(requirements)
	touch $(requirements_stamp);
	$(venv)/bin/pip install -r $(requirements);

activate: $(venv)
	@echo "Make sure you activated your venv by running 'source $(venv)/bin/activate'";

run: activate $(requirements_stamp)
	python main.py;

.PHONY: clean activate run

clean:
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rf ../__pycache__;
	rm -f $(requirements_stamp);