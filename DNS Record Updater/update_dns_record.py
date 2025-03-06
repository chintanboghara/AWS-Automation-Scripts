#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def update_dns_record(domain_name: str, ip_address: str, hosted_zone_id: str, dry_run: bool = False) -> None:
    """
    Update (or upsert) a DNS A record in Route 53.

    Args:
        domain_name (str): The domain name to update (e.g., example.com).
        ip_address (str): The IP address to associate with the domain.
        hosted_zone_id (str): The ID of the Route 53 hosted zone.
        dry_run (bool): If True, simulate the update without making any changes.
    """
    route53 = boto3.client('route53')
    
    change_batch = {
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': domain_name,
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': ip_address}]
                }
            }
        ]
    }
    
    if dry_run:
        print("Dry run: The following DNS record change would be applied:")
        print(f"  Domain Name: {domain_name}")
        print(f"  IP Address: {ip_address}")
        print(f"  Hosted Zone ID: {hosted_zone_id}")
        print(f"  Change Batch: {change_batch}")
        return

    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        print(f"DNS Record Updated: {domain_name} -> {ip_address}")
        print("Response:", response)
    except Exception as e:
        logging.error(f"Error updating DNS record for {domain_name}: {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update (or upsert) a DNS A record in AWS Route 53."
    )
    parser.add_argument(
        "domain_name",
        help="The domain name to update (e.g., example.com)."
    )
    parser.add_argument(
        "ip_address",
        help="The IP address to associate with the domain (e.g., 192.168.1.1)."
    )
    parser.add_argument(
        "hosted_zone_id",
        help="The ID of the Route 53 hosted zone (e.g., ZXXXXXXXXXXXXX)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the DNS update without actually making changes."
    )
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    update_dns_record(args.domain_name, args.ip_address, args.hosted_zone_id, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
