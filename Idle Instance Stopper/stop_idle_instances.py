#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def stop_idle_instances(core_threshold: int, dry_run: bool = False) -> None:
    """
    Stop running EC2 instances that are considered idle based on their CPU core count.

    Instances with a core count less than the specified threshold are considered idle.

    Args:
        core_threshold (int): The CPU core count threshold below which an instance is considered idle.
        dry_run (bool): If True, simulate stopping the instances without taking action.
    """
    ec2 = boto3.client('ec2')
    try:
        instances = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
    except Exception as e:
        logging.error(f"Error retrieving instances: {e}")
        sys.exit(1)
    
    stopped_any = False
    for reservation in instances.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instance_id = instance.get('InstanceId')
            cpu_options = instance.get('CpuOptions', {})
            core_count = cpu_options.get('CoreCount', 0)
            if core_count < core_threshold:
                if dry_run:
                    print(f"Dry run: Would stop idle instance {instance_id} (Core count: {core_count})")
                else:
                    try:
                        ec2.stop_instances(InstanceIds=[instance_id])
                        print(f"Stopped idle instance {instance_id} (Core count: {core_count})")
                        stopped_any = True
                    except Exception as e:
                        logging.error(f"Error stopping instance {instance_id}: {e}")

    if not stopped_any and not dry_run:
        print("No idle instances found or all instances meet the core threshold.")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stop idle EC2 instances based on a CPU core threshold."
    )
    parser.add_argument(
        '--threshold', type=int, default=5,
        help="CPU core count threshold below which an instance is considered idle. Default is 5."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Simulate stopping idle instances without actually stopping them."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    stop_idle_instances(core_threshold=args.threshold, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
