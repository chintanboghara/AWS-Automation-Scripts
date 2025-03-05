#!/usr/bin/env python3
import boto3
import argparse
import sys
import logging

def delete_unused_ebs_volumes(dry_run: bool = False) -> None:
    """
    Delete all unused (available) EBS volumes in your AWS account.
    
    Args:
        dry_run (bool): If True, only print which volumes would be deleted without actually deleting them.
    """
    ec2 = boto3.client('ec2')
    try:
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    except Exception as e:
        logging.error(f"Error retrieving volumes: {e}")
        sys.exit(1)

    if not volumes['Volumes']:
        print("No available volumes to delete.")
        return

    for volume in volumes['Volumes']:
        volume_id = volume.get('VolumeId')
        try:
            if dry_run:
                print(f"Dry run: Volume {volume_id} would be deleted.")
            else:
                ec2.delete_volume(VolumeId=volume_id)
                print(f"Deleted volume: {volume_id}")
        except Exception as e:
            logging.error(f"Error deleting volume {volume_id}: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Delete all unused (available) EBS volumes in your AWS account."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Perform a dry run without actually deleting volumes."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    delete_unused_ebs_volumes(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
