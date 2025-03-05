#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def get_aws_billing(start_date: str, end_date: str) -> None:
    """
    Retrieve the AWS billing cost for a specified time period using the Cost Explorer API.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    """
    ce = boto3.client('ce')
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['BlendedCost']
        )
        results = response.get('ResultsByTime', [])
        if results:
            cost_amount = results[0]['Total']['BlendedCost']['Amount']
            print(f"AWS Billing Cost from {start_date} to {end_date}: {cost_amount} USD")
        else:
            print("No cost data found for the specified period.")
    except Exception as e:
        logging.error(f"Error retrieving AWS billing data: {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve AWS Billing Cost using the AWS Cost Explorer API."
    )
    parser.add_argument(
        '--start-date', type=str, default='2023-01-01',
        help="Start date for billing period (YYYY-MM-DD). Default: 2023-01-01"
    )
    parser.add_argument(
        '--end-date', type=str, default='2023-01-31',
        help="End date for billing period (YYYY-MM-DD). Default: 2023-01-31"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    get_aws_billing(args.start_date, args.end_date)

if __name__ == "__main__":
    main()
