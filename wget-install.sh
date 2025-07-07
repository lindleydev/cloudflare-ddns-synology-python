#!/bin/sh
# Installs the Synology Cloudflare DDNS script via wget and adds provider entry
# Usage: sudo ./wget-install.sh

SCRIPT_URL="https://github.com/lindleydev/cloudflare-ddns-synology-python/releases/latest/download/cloudflare_ddns.py"
ADD_PROVIDER_URL="https://raw.githubusercontent.com/lindleydev/cloudflare-ddns-synology-python/main/add_synology_ddns_provider.sh"
TARGET_PATH="/usr/syno/bin/ddns/cloudflare_ddns.py"
ADD_PROVIDER_SCRIPT="$HOME/add_synology_ddns_provider.sh"

set -e

# Download the main script
sudo wget -O "$TARGET_PATH" "$SCRIPT_URL"
sudo chmod +x "$TARGET_PATH"
echo "Installed cloudflare_ddns.py to $TARGET_PATH."

# Download the provider add script
wget -O "$ADD_PROVIDER_SCRIPT" "$ADD_PROVIDER_URL"
chmod +x "$ADD_PROVIDER_SCRIPT"

# Add provider entry
sudo "$ADD_PROVIDER_SCRIPT"
echo "Provider entry added to /etc/ddns_provider.conf."

# Clean up
rm -f "$ADD_PROVIDER_SCRIPT"
