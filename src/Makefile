# Makefile for the MiniGoogleCloudCollector project

# Run main.py with all the .py files recursively as dependencies
run: main.py $(shell find . -name "*.py")
	python3.12 main.py 'y';

# Clean all the .pyc files
clean:
	find . -name "*.pyc" -exec rm -f {} \;