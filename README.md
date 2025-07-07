# Cloudflare DDNS for Synology (Python Custom Provider)

This project provides a Python script and Synology integration for using Cloudflare as a custom DDNS provider.

## Quick Install (Standalone Binary for Synology)

You can install the DDNS script as a single-file binary (no Python or pip required) by downloading the latest release from GitHub:

```sh
wget https://github.com/lindleydev/cloudflare-ddns-synology-python/releases/latest/download/cloudflare_ddns.py -O /usr/syno/bin/ddns/cloudflare_ddns.py
sudo chmod +x /usr/syno/bin/ddns/cloudflare_ddns.py
```

Then add the provider entry:
```sh
wget https://raw.githubusercontent.com/lindleydev/cloudflare-ddns-synology-python/main/add_synology_ddns_provider.sh -O /tmp/add_synology_ddns_provider.sh
chmod +x /tmp/add_synology_ddns_provider.sh
sudo /tmp/add_synology_ddns_provider.sh
rm /tmp/add_synology_ddns_provider.sh
```

This method is recommended for Synology and other systems without Python package management.

## Features
- Compatible with Synology's custom DDNS provider protocol
- Uses Cloudflare API via `cloudflare-ddns` package
- CLI for manual or Synology-triggered updates
- Easy install and Synology config scripts

## Synology Custom Provider Setup
- In DSM, add a new custom DDNS provider and select "Cloudflare".
- No parameters are needed in the query URL; Synology will call the local script.
- The script accepts the following parameters:
  - `hostname`: DNS record(s) to update. Multiple domains can be separated with `--` (e.g., `domain1.com--domain2.com`)
  - `myip`: IP address to set
  - `username`: Cloudflare account email
  - `password`: Cloudflare API token

### Usage Modes
This script supports two ways of being called:

1. **Synology DDNS Provider Mode** (positional arguments):
   ```
   /sbin/cloudflare_ddns.py example.com--subdomain.example.com 1.2.3.4 your@email.com api_token
   ```

2. **Manual CLI Mode** (named arguments):
   ```
   /sbin/cloudflare_ddns.py --hostname example.com--subdomain.example.com --myip 1.2.3.4 --username your@email.com --password api_token
   ```

## Testing
Run tests with:
```sh
uv pip install -e .[test]
pytest
```

## References
- [cloudflare-ddns PyPI](https://pypi.org/project/cloudflare-ddns/)
- [Synology Custom DDNS Provider](https://kb.synology.com/en-id/DSM/help/DSM/AdminCenter/connection_ddns?version=7)
