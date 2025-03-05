#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def cleanup_old_lambda_versions(function_name: str, dry_run: bool = False) -> None:
    """
    Clean up old versions of a Lambda function.

    This function lists all versions of the specified Lambda function and deletes
    every version except '$LATEST'. A dry run mode is available to simulate the deletions.

    Args:
        function_name (str): The name or ARN of the Lambda function.
        dry_run (bool): If True, simulates deletion without making changes.
    """
    lambda_client = boto3.client('lambda')
    
    try:
        response = lambda_client.list_versions_by_function(FunctionName=function_name)
        versions = response.get('Versions', [])
    except Exception as e:
        logging.error(f"Failed to list versions for function '{function_name}': {e}")
        sys.exit(1)
    
    # Filter out the '$LATEST' version
    deletable_versions = [v for v in versions if v.get('Version') != '$LATEST']
    if not deletable_versions:
        print("No old versions found for deletion.")
        return
    
    for version in deletable_versions:
        version_number = version.get('Version')
        if dry_run:
            print(f"Dry run: Would delete Lambda version {version_number}")
        else:
            try:
                lambda_client.delete_function(FunctionName=function_name, Qualifier=version_number)
                print(f"Deleted Lambda version {version_number}")
            except Exception as e:
                logging.error(f"Error deleting version {version_number} for function '{function_name}': {e}")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean up old versions of a Lambda function (excluding '$LATEST')."
    )
    parser.add_argument(
        'function_name',
        help="The name or ARN of the Lambda function."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simulate deletion without actually deleting any versions."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    cleanup_old_lambda_versions(args.function_name, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
