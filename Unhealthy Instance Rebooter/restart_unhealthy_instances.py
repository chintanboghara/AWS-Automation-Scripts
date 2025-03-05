#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def restart_unhealthy_instances(dry_run: bool = False) -> None:
    """
    Restart all EC2 instances that are unhealthy based on their instance status.
    
    Unhealthy instances (where the instance status is not 'ok') are rebooted.
    The dry_run option allows you to simulate the reboot actions without making any changes.
    
    Args:
        dry_run (bool): If True, simulate the reboot actions.
    """
    ec2 = boto3.client('ec2')
    
    try:
        statuses = ec2.describe_instance_status(IncludeAllInstances=True)
    except Exception as e:
        logging.error(f"Error retrieving instance statuses: {e}")
        sys.exit(1)
    
    instance_statuses = statuses.get('InstanceStatuses', [])
    
    if not instance_statuses:
        print("No instance statuses available to check.")
        return

    for status in instance_statuses:
        instance_id = status.get('InstanceId')
        inst_status = status.get('InstanceStatus', {}).get('Status', 'unknown')
        
        if inst_status.lower() != 'ok':
            if dry_run:
                print(f"Dry run: Would reboot instance {instance_id} (status: {inst_status}).")
            else:
                try:
                    ec2.reboot_instances(InstanceIds=[instance_id])
                    print(f"Rebooted instance {instance_id} (status: {inst_status}).")
                except Exception as e:
                    logging.error(f"Error rebooting instance {instance_id}: {e}")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Restart all EC2 instances with unhealthy status."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Simulate the reboot actions without actually rebooting instances."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    restart_unhealthy_instances(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
