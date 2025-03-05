#!/usr/bin/env python3
import boto3
import argparse
import sys

def manage_ec2_instance(instance_id: str, action: str) -> None:
    """
    Manage an EC2 instance by performing the specified action.

    Args:
        instance_id (str): The EC2 instance ID.
        action (str): The action to perform: start, stop, restart, or terminate.
    """
    ec2 = boto3.client('ec2')
    
    actions = {
        'start': 'start_instances',
        'stop': 'stop_instances',
        'restart': 'reboot_instances',
        'terminate': 'terminate_instances'
    }
    
    if action not in actions:
        print(f"Invalid action: {action}. Use 'start', 'stop', 'restart', or 'terminate'.")
        sys.exit(1)
    
    try:
        # Dynamically call the corresponding EC2 method
        method = getattr(ec2, actions[action])
        response = method(InstanceIds=[instance_id])
        print(f"{action.capitalize()} action initiated for instance {instance_id}.")
        print(response)
    except Exception as e:
        print(f"Error while performing {action} on instance {instance_id}: {e}")
        sys.exit(1)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage an EC2 instance with start, stop, restart, or terminate actions."
    )
    parser.add_argument(
        'instance_id',
        help="The ID of the EC2 instance (e.g., i-0123456789abcdef0)"
    )
    parser.add_argument(
        'action',
        choices=['start', 'stop', 'restart', 'terminate'],
        help="Action to perform on the instance"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    manage_ec2_instance(args.instance_id, args.action.lower())

if __name__ == "__main__":
    main()
