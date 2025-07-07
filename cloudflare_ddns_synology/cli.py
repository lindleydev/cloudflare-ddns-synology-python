import sys
import argparse
from cloudflare_ddns.cloudflare import CloudFlare

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
