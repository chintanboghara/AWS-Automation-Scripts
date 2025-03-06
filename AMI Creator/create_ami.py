#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def create_ami(instance_id: str, ami_name: str, dry_run: bool = False) -> None:
    """
    Create an Amazon Machine Image (AMI) from an existing EC2 instance.

    Args:
        instance_id (str): The ID of the EC2 instance.
        ami_name (str): The name to assign to the new AMI.
        dry_run (bool): If True, simulate the creation without making any changes.
    """
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            NoReboot=True,
            DryRun=dry_run
        )
        if dry_run:
            print(f"Dry run: AMI creation simulated for instance {instance_id} with name '{ami_name}'.")
        else:
            print(f"AMI '{ami_name}' created for instance {instance_id}.")
            print(f"Response: {response}")
    except Exception as e:
        logging.error(f"Error creating AMI for instance {instance_id}: {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an AMI from an EC2 instance without rebooting it."
    )
    parser.add_argument(
        "instance_id",
        help="The ID of the EC2 instance (e.g., i-1234567890abcdef0)."
    )
    parser.add_argument(
        "ami_name",
        help="The name for the new AMI (e.g., my-ami-backup)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the AMI creation without actually creating it."
    )
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    create_ami(args.instance_id, args.ami_name, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
