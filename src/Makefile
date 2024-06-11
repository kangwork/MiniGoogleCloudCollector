# Makefile for the MiniGoogleCloudCollector project

# Run main.py with all the .py files recursively as dependencies
run: main.py $(shell find . -name "*.py")
	python3.12 main.py 'y';

.PHONY: clean

# Clean all the __pycache__ directories
clean:
	find . -name "__pycache__" -exec rm -rf {} \;