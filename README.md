# Cloudflare DDNS for Synology (Python Custom Provider)

This project provides a portable, dependency-free Python script for using Cloudflare as a custom DDNS provider on Synology and similar systems. No external Python packages or compilation are required.

## Quick Install (Recommended for Synology)

You can install the DDNS script and add the provider entry in one step by downloading and running the install script directly from GitHub:

```sh
wget https://raw.githubusercontent.com/lindleydev/cloudflare-ddns-synology-python/main/wget-install.sh -O ~/wget-install.sh
chmod +x ~/wget-install.sh
sudo ~/wget-install.sh
```

This will:
- Download the latest DDNS script to `/usr/syno/bin/ddns/cloudflare_ddns.py`
- Make it executable
- Add the provider entry to `/etc/ddns_provider.conf`

If you want to do this manually, see the scripts for details.

## Manual Install (Raw Script)

You can install the DDNS script as a single-file Python script (no Python or pip required on Synology) by downloading the latest release from GitHub:

```sh
wget https://github.com/lindleydev/cloudflare-ddns-synology-python/releases/latest/download/cloudflare_ddns.py -O /usr/syno/bin/ddns/cloudflare_ddns.py
sudo chmod +x /usr/syno/bin/ddns/cloudflare_ddns.py
```

Then add the provider entry:
```sh
wget https://raw.githubusercontent.com/lindleydev/cloudflare-ddns-synology-python/main/add_synology_ddns_provider.sh -O ~/add_synology_ddns_provider.sh
chmod +x ~/add_synology_ddns_provider.sh
sudo ~/add_synology_ddns_provider.sh
rm ~/add_synology_ddns_provider.sh
```

This method is recommended for Synology and other systems without Python package management.

## Features
- Compatible with Synology's custom DDNS provider protocol
- Uses Cloudflare API directly (no dependencies)
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
   /usr/syno/bin/ddns/cloudflare_ddns.py example.com--subdomain.example.com 1.2.3.4 your@email.com api_token
   ```

2. **Manual CLI Mode** (named arguments):
   ```
   /usr/syno/bin/ddns/cloudflare_ddns.py --hostname example.com--subdomain.example.com --myip 1.2.3.4 --username your@email.com --password api_token
   ```

## Testing
Run tests with:
```sh
uv pip install -e .[test]
pytest
```

## Release Pipeline
- The release process now uploads the raw, portable script as `cloudflare_ddns.py` (no compilation or dependencies required).
- See `.github/workflows/release.yml` for details.

## References
- [Synology Custom DDNS Provider](https://kb.synology.com/en-id/DSM/help/DSM/AdminCenter/connection_ddns?version=7)
