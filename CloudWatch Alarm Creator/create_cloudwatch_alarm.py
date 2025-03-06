#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def create_cloudwatch_alarm(instance_id: str, threshold: float = 70.0, sns_topic_arn: str = None, dry_run: bool = False) -> None:
    """
    Create a CloudWatch alarm for CPU utilization for an EC2 instance.

    Args:
        instance_id (str): The ID of the EC2 instance.
        threshold (float): CPU utilization threshold for the alarm. Default is 70.0.
        sns_topic_arn (str): The SNS topic ARN to send alarm notifications.
        dry_run (bool): If True, simulate the creation without making changes.
    """
    if not sns_topic_arn:
        logging.error("SNS topic ARN is required. Provide it using the '--sns-topic-arn' argument.")
        sys.exit(1)

    alarm_name = f"CPU_Utilization_{instance_id}"
    parameters = {
        "AlarmName": alarm_name,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Statistic": "Average",
        "Period": 300,
        "EvaluationPeriods": 1,
        "Threshold": threshold,
        "ComparisonOperator": "GreaterThanThreshold",
        "AlarmActions": [sns_topic_arn],
        "Dimensions": [{"Name": "InstanceId", "Value": instance_id}]
    }
    
    if dry_run:
        print("Dry run: The following CloudWatch alarm parameters would be used:")
        for key, value in parameters.items():
            print(f"  {key}: {value}")
        return

    try:
        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_alarm(**parameters)
        print(f"CloudWatch alarm '{alarm_name}' created for instance {instance_id}.")
    except Exception as e:
        logging.error(f"Error creating CloudWatch alarm for instance {instance_id}: {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a CloudWatch alarm for CPU utilization of an EC2 instance."
    )
    parser.add_argument(
        "instance_id",
        help="The ID of the EC2 instance (e.g., i-1234567890abcdef0)."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=70.0,
        help="CPU utilization threshold for the alarm (default: 70.0)."
    )
    parser.add_argument(
        "--sns-topic-arn",
        required=True,
        help="The SNS topic ARN for alarm notifications."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the alarm creation without making any changes."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    create_cloudwatch_alarm(
        instance_id=args.instance_id,
        threshold=args.threshold,
        sns_topic_arn=args.sns_topic_arn,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
