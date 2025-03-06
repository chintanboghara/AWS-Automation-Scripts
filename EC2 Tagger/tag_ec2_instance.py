#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def tag_ec2_instance(instance_id: str, tags: list, dry_run: bool = False) -> None:
    """
    Tag an EC2 instance with specified key-value pairs.

    Args:
        instance_id (str): The ID of the EC2 instance.
        tags (list): List of tags in the format [{'Key': key, 'Value': value}, ...].
        dry_run (bool): If True, simulate tagging without making any changes.
    """
    ec2 = boto3.client('ec2')
    try:
        if dry_run:
            print(f"Dry run: Would tag instance {instance_id} with tags: {tags}")
        else:
            ec2.create_tags(Resources=[instance_id], Tags=tags)
            print(f"Tagged instance {instance_id} with tags: {tags}")
    except Exception as e:
        logging.error(f"Error tagging instance {instance_id}: {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tag an EC2 instance with specified key-value pairs."
    )
    parser.add_argument(
        "instance_id",
        help="The ID of the EC2 instance (e.g., i-1234567890abcdef0)"
    )
    parser.add_argument(
        "--tags",
        action="append",
        required=True,
        help="Tag in the format Key=Value. Example: --tags Owner=DevOps"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate tagging without actually applying changes."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    # Parse tags from key=value strings to the required dictionary format.
    tags = []
    for tag in args.tags:
        if '=' not in tag:
            logging.error(f"Invalid tag format: '{tag}'. Expected format is Key=Value.")
            sys.exit(1)
        key, value = tag.split('=', 1)
        tags.append({'Key': key, 'Value': value})
    tag_ec2_instance(args.instance_id, tags, dry_run=args.dry_run)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
