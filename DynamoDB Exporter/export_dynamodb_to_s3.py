#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys
import json

def export_dynamodb_to_s3(table_name: str, bucket_name: str, file_name: str, dry_run: bool = False) -> None:
    """
    Export all items from a DynamoDB table to a JSON file stored in an S3 bucket.
    
    This function scans the specified DynamoDB table (with pagination support)
    and exports the data as a formatted JSON file to the given S3 bucket.
    
    Args:
        table_name (str): The name of the DynamoDB table.
        bucket_name (str): The destination S3 bucket.
        file_name (str): The S3 object key (e.g., backup.json) for the exported data.
        dry_run (bool): If True, simulate the export without uploading to S3.
    """
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    table = dynamodb.Table(table_name)
    
    try:
        data = table.scan()
        items = data.get('Items', [])
        # Handle pagination if necessary.
        while 'LastEvaluatedKey' in data:
            data = table.scan(ExclusiveStartKey=data['LastEvaluatedKey'])
            items.extend(data.get('Items', []))
    except Exception as e:
        logging.error(f"Error scanning DynamoDB table '{table_name}': {e}")
        sys.exit(1)
    
    # Convert the data to a formatted JSON string.
    json_data = json.dumps(items, indent=4, default=str)
    
    if dry_run:
        print(f"Dry run: Would export data from DynamoDB table '{table_name}' to s3://{bucket_name}/{file_name}.")
    else:
        try:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=json_data)
            print(f"Data exported to s3://{bucket_name}/{file_name}")
        except Exception as e:
            logging.error(f"Error uploading data to S3: {e}")
            sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export data from a DynamoDB table to an S3 bucket as a JSON file."
    )
    parser.add_argument(
        'table_name',
        help="Name of the DynamoDB table."
    )
    parser.add_argument(
        'bucket_name',
        help="Name of the destination S3 bucket."
    )
    parser.add_argument(
        'file_name',
        help="Name of the file to create in S3 (e.g., backup.json)."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Simulate the export without actually uploading data to S3."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    export_dynamodb_to_s3(args.table_name, args.bucket_name, args.file_name, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
