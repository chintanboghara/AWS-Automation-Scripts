#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def delete_unused_ebs_volumes(dry_run: bool = False) -> None:
    """
    Delete all available (unused) EBS volumes in your AWS account.

    Args:
        dry_run (bool): If True, simulate the deletion without actually deleting volumes.
    """
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    except Exception as e:
        logging.error(f"Error retrieving volumes: {e}")
        sys.exit(1)
    
    volumes = response.get('Volumes', [])
    if not volumes:
        print("No available volumes found to delete.")
        return

    for volume in volumes:
        volume_id = volume.get('VolumeId')
        try:
            if dry_run:
                print(f"Dry run: Would delete volume: {volume_id}")
            else:
                ec2.delete_volume(VolumeId=volume_id)
                print(f"Deleted volume: {volume_id}")
        except Exception as e:
            logging.error(f"Error deleting volume {volume_id}: {e}")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete all unused (available) EBS volumes."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simulate deletion without actually deleting any volumes."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    delete_unused_ebs_volumes(dry_run=args.dry_run)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
