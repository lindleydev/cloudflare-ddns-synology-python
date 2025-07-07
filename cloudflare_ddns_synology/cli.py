import sys
import argparse
from cloudflare_ddns.cloudflare_ddns import CloudflareDDNS

def main():
    parser = argparse.ArgumentParser(description="Cloudflare DDNS updater for Synology custom DDNS provider.")
    parser.add_argument('--hostname', required=True, help='The DNS hostname to update')
    parser.add_argument('--myip', required=True, help='The IP address to set')
    parser.add_argument('--username', required=True, help='Cloudflare account email (see Cloudflare dashboard)')
    parser.add_argument('--password', required=True, help='Cloudflare API token (see docs)')
    args = parser.parse_args()

    cf = CloudflareDDNS(
        email=args.username,
        api_key=args.password,
        zone=None,
        record=args.hostname,
        ip=args.myip
    )
    try:
        cf.update_dns()
        print('good')
    except Exception as e:
        print('911')
        sys.exit(1)

if __name__ == '__main__':
    main()
