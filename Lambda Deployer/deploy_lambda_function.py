#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys
import os

def deploy_lambda_function(function_name: str, zip_file_path: str, dry_run: bool = False) -> None:
    """
    Deploy an updated Lambda function code using the provided ZIP file.

    Args:
        function_name (str): The name or ARN of the Lambda function.
        zip_file_path (str): The path to the Lambda deployment package (ZIP file).
        dry_run (bool): If True, simulate the deployment without updating the function.
    """
    # Check if the zip file exists
    if not os.path.exists(zip_file_path):
        logging.error(f"Zip file not found: {zip_file_path}")
        sys.exit(1)

    # Read the zip file content
    try:
        with open(zip_file_path, 'rb') as f:
            zip_file_data = f.read()
    except Exception as e:
        logging.error(f"Error reading zip file '{zip_file_path}': {e}")
        sys.exit(1)

    # Dry run mode: only simulate deployment
    if dry_run:
        print(f"Dry run: Would update Lambda function '{function_name}' with zip file '{zip_file_path}'.")
        return

    # Update the Lambda function code
    lambda_client = boto3.client('lambda')
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_file_data
        )
        print(f"Lambda function '{function_name}' updated successfully.")
        print(response)
    except Exception as e:
        logging.error(f"Error updating Lambda function '{function_name}': {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deploy or update an AWS Lambda function using a provided ZIP file."
    )
    parser.add_argument(
        'function_name',
        help="The name or ARN of the Lambda function to update."
    )
    parser.add_argument(
        'zip_file_path',
        help="The file path to the Lambda deployment package (ZIP file)."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simulate the deployment without updating the Lambda function."
    )
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    deploy_lambda_function(args.function_name, args.zip_file_path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
