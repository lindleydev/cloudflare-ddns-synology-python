# Cloudflare DDNS for Synology (Python Custom Provider)

This project provides a Python script and Synology integration for using Cloudflare as a custom DDNS provider.

## Quick Install (Recommended for Synology)

You can install the DDNS script and add the provider entry in one step by downloading and running the install script directly from GitHub:

```sh
wget https://raw.githubusercontent.com/lindleydev/cloudflare-ddns-synology-python/main/wget-install.sh -O /tmp/wget-install.sh
chmod +x /tmp/wget-install.sh
sudo /tmp/wget-install.sh
```

This will:
- Download the latest DDNS script to `/sbin/cloudflare_ddns.py`
- Make it executable
- Add the provider entry to `/etc/ddns_provider.conf`

If you want to do this manually, see the scripts for details.

## Quick Install (Standalone Binary for Synology)

You can install the DDNS script as a single-file binary (no Python or pip required) by downloading the latest release from GitHub:

```sh
wget https://github.com/lindleydev/cloudflare-ddns-synology-python/releases/latest/download/cloudflare_ddns.py -O /sbin/cloudflare_ddns.py
sudo chmod +x /sbin/cloudflare_ddns.py
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
- The script expects the following parameters:
  - `hostname`: DNS record to update
  - `myip`: IP address to set
  - `username`: Cloudflare account email
  - `password`: Cloudflare API token

## Testing
Run tests with:
```sh
uv pip install -e .[test]
pytest
```

## References
- [cloudflare-ddns PyPI](https://pypi.org/project/cloudflare-ddns/)
- [Synology Custom DDNS Provider](https://kb.synology.com/en-id/DSM/help/DSM/AdminCenter/connection_ddns?version=7)
