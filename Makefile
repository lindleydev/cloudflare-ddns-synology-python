# Makefile for cloudflare-ddns-synology

.PHONY: all build publish test clean install

all: build

build:
	uv pip install --upgrade build
	uv run -m build

publish:
	uv pip install --upgrade twine
	uv run -m twine upload dist/*

publish-test:
	uv pip install --upgrade twine
	uv run -m twine upload --repository testpypi dist/*

test:
	uv pip install -e .[test]
	pytest

install:
	uv pip install .

clean:
	rm -rf dist build *.egg-info
