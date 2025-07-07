#!/bin/sh
# Installs the cloudflare-ddns-synology package system-wide and sets up Synology integration
set -e

# Install the package to system Python
sudo uv pip install .

# Copy CLI entrypoint to /sbin/cloudflare_ddns.py
sudo cp cloudflare_ddns_synology/cli.py /sbin/cloudflare_ddns.py
sudo chmod +x /sbin/cloudflare_ddns.py

echo "cloudflare-ddns-synology installed and /sbin/cloudflare_ddns.py set up."
