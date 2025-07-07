# Makefile for cloudflare-ddns-synology

.PHONY: all test clean install

all: test

test:
	uv pip install -e .[test]
	pytest

install:
	cp cloudflare_ddns_synology/cli.py /usr/syno/bin/ddns/cloudflare_ddns.py
	chmod +x /usr/syno/bin/ddns/cloudflare_ddns.py

clean:
	rm -rf dist build *.egg-info
