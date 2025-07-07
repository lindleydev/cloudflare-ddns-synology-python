#!/bin/sh
# Installs the standalone Synology Cloudflare DDNS binary and adds provider entry
# Usage: sudo ./binary-install.sh

BINARY_URL="https://github.com/<your-username>/<your-repo>/releases/latest/download/cloudflare_ddns.py"
ADD_PROVIDER_URL="https://raw.githubusercontent.com/<your-username>/<your-repo>/main/add_synology_ddns_provider.sh"
TARGET_PATH="/sbin/cloudflare_ddns.py"
ADD_PROVIDER_SCRIPT="/tmp/add_synology_ddns_provider.sh"

set -e

# Download the binary
sudo wget -O "$TARGET_PATH" "$BINARY_URL"
sudo chmod +x "$TARGET_PATH"
echo "Installed cloudflare_ddns.py to $TARGET_PATH."

# Download and run the provider add script
wget -O "$ADD_PROVIDER_SCRIPT" "$ADD_PROVIDER_URL"
chmod +x "$ADD_PROVIDER_SCRIPT"
sudo "$ADD_PROVIDER_SCRIPT"
echo "Provider entry added to /etc/ddns_provider.conf."
rm -f "$ADD_PROVIDER_SCRIPT"
