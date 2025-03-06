#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def check_open_security_groups(cidr_filter: str = "0.0.0.0/0") -> None:
    """
    Check and list security groups that allow open access based on a specified CIDR filter.

    Args:
        cidr_filter (str): The CIDR block to check for (default: "0.0.0.0/0").
    """
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_security_groups()
        groups = response.get('SecurityGroups', [])
    except Exception as e:
        logging.error(f"Error retrieving security groups: {e}")
        sys.exit(1)
    
    open_groups_found = False
    for group in groups:
        group_id = group.get('GroupId')
        group_name = group.get('GroupName', 'N/A')
        for permission in group.get('IpPermissions', []):
            for ip_range in permission.get('IpRanges', []):
                if ip_range.get('CidrIp') == cidr_filter:
                    print(f"Security Group {group_id} ({group_name}) has open access with CIDR {cidr_filter}!")
                    open_groups_found = True

    if not open_groups_found:
        print(f"No security groups found with open access (CIDR {cidr_filter}).")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check AWS EC2 security groups for open access based on a specified CIDR."
    )
    parser.add_argument(
        "--cidr",
        type=str,
        default="0.0.0.0/0",
        help="CIDR block to check for open access (default: 0.0.0.0/0)."
    )
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    check_open_security_groups(cidr_filter=args.cidr)

if __name__ == "__main__":
    main()
