#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import urllib.request
import urllib.parse
import json

class CloudFlare:
    def __init__(self, email, api_key, domain):
        self.email = email
        self.api_key = api_key
        self.domain = domain
        self.base_url = "https://api.cloudflare.com/client/v4"
        # Prefer API token (recommended by Cloudflare)
        if self.api_key.startswith("sk_") or self.api_key.startswith("CFAPI_") or len(self.api_key) > 30:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        else:
            self.headers = {
                "X-Auth-Email": self.email,
                "X-Auth-Key": self.api_key,
                "Content-Type": "application/json"
            }

    def _request(self, method, url, data=None):
        req = urllib.request.Request(url, method=method)
        for k, v in self.headers.items():
            req.add_header(k, v)
        if data is not None:
            req.data = json.dumps(data).encode("utf-8")
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            raise Exception(f"HTTP error: {e}")

    def get_zone_id(self):
        # Find the zone for the domain (must be the root zone, not subdomain)
        parts = self.domain.split('.')
        for i in range(len(parts)-1):
            zone_name = '.'.join(parts[i:])
            url = f"{self.base_url}/zones?name={urllib.parse.quote(zone_name)}"
            data = self._request("GET", url)
            if data.get('success') and data['result']:
                return data['result'][0]['id']
        raise Exception(f"Zone not found for domain: {self.domain}")

    def get_record_id(self, zone_id, record_name):
        url = f"{self.base_url}/zones/{zone_id}/dns_records?type=A&name={urllib.parse.quote(record_name)}"
        data = self._request("GET", url)
        if data.get('success') and data['result']:
            return data['result'][0]['id']
        return None

    def sync_dns_from_my_ip(self, ip=None):
        # Use the provided IP or auto-detect (should always be provided by Synology)
        ip = ip or self.get_my_ip()
        zone_id = self.get_zone_id()
        record_id = self.get_record_id(zone_id, self.domain)
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        payload = {
            "type": "A",
            "name": self.domain,
            "content": ip,
            "ttl": 1,
            "proxied": False
        }
        if record_id:
            # Update existing record
            url = f"{url}/{record_id}"
            data = self._request("PUT", url, payload)
        else:
            # Create new record
            data = self._request("POST", url, payload)
        if not data.get('success'):
            raise Exception(f"Cloudflare API error: {data}")

    def get_my_ip(self):
        # Fallback: get public IP from an external service
        with urllib.request.urlopen("https://api.ipify.org") as resp:
            return resp.read().decode().strip()

def main():
    # Check if we're being called with positional arguments (Synology style)
    # Synology passes arguments in the order: hostname, IP, username, password
    if len(sys.argv) == 5 and not sys.argv[1].startswith('-'):
        hostname = sys.argv[1]
        myip = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
    else:
        # Otherwise use argparse for named arguments (for manual CLI usage)
        parser = argparse.ArgumentParser(description="Cloudflare DDNS updater for Synology custom DDNS provider.")
        parser.add_argument('--hostname', required=True, help='The DNS hostname(s) to update. Multiple domains can be separated with "--" (e.g., domain1.com--domain2.com)')
        parser.add_argument('--myip', required=True, help='The IP address to set')
        parser.add_argument('--username', required=True, help='Cloudflare account email (see Cloudflare dashboard)')
        parser.add_argument('--password', required=True, help='Cloudflare API token (see docs)')
        args = parser.parse_args()
        
        hostname = args.hostname
        myip = args.myip
        username = args.username
        password = args.password

    # Split the hostname by "--" to handle multiple domains
    hostnames = hostname.split('--')
    
    success = True
    for single_hostname in hostnames:
        single_hostname = single_hostname.strip()  # Remove any whitespace
        if not single_hostname:
            continue
            
        try:
            cf = CloudFlare(
                email=username,
                api_key=password,
                domain=single_hostname
            )
            # Update the DNS record with the current IP
            cf.sync_dns_from_my_ip()
            # Continue with other domains even if one succeeds
        except Exception as e:
            success = False
            print(f"Error updating {single_hostname}: {str(e)}", file=sys.stderr)
    
    if success:
        print('good')
        return 0
    else:
        print('911')
        sys.exit(1)

if __name__ == '__main__':
    main()
