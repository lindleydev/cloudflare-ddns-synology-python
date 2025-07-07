#!/bin/sh
# Adds a fixed Cloudflare provider entry to Synology's ddns_provider.conf
CONF_FILE="/etc/ddns_provider.conf"
PROVIDER_NAME="Cloudflare"
MODULE_PATH="/sbin/cloudflare_ddns.py"
QUERY_URL="https://www.cloudflare.com"
WEBSITE_URL="https://www.cloudflare.com"

if grep -q "^\[$PROVIDER_NAME\]" "$CONF_FILE"; then
  echo "Provider already exists."
  exit 0
fi
# Append new provider section
sudo sh -c "echo '\n[$PROVIDER_NAME]' >> $CONF_FILE"
sudo sh -c "echo '    modulepath=$MODULE_PATH' >> $CONF_FILE"
sudo sh -c "echo '    queryurl=$QUERY_URL' >> $CONF_FILE"
sudo sh -c "echo '    website=$WEBSITE_URL' >> $CONF_FILE"
echo "Provider entry added."
