.PHONY: clean

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean       => to clean clean all automatically generated files"

clean:
	find src/ -name \*.pyc -delete
	find src/ -name \*__pycache__ -delete
