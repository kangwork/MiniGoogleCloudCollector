# Makefile for the MiniGoogleCloudCollector project

run: main.py $(shell find . -name "*.py")
	python3.12 main.py 'y';

.PHONY: clean

clean:
	find . -name "__pycache__" -exec rm -rf {} \;