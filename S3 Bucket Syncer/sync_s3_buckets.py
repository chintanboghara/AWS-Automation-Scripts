#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def sync_s3_buckets(source_bucket: str, destination_bucket: str, dry_run: bool = False) -> None:
    """
    Sync objects from a source S3 bucket to a destination S3 bucket.
    
    For each object in the source bucket, the script copies it to the destination bucket.
    Use the dry_run flag to simulate the process without actually copying the objects.
    
    Args:
        source_bucket (str): The name of the source S3 bucket.
        destination_bucket (str): The name of the destination S3 bucket.
        dry_run (bool): If True, simulate the sync without making any changes.
    """
    s3 = boto3.resource('s3')
    source = s3.Bucket(source_bucket)
    
    try:
        for obj in source.objects.all():
            copy_source = {'Bucket': source_bucket, 'Key': obj.key}
            if dry_run:
                print(f"Dry run: Would copy '{obj.key}' from '{source_bucket}' to '{destination_bucket}'.")
            else:
                s3.Object(destination_bucket, obj.key).copy(copy_source)
                print(f"Copied '{obj.key}' from '{source_bucket}' to '{destination_bucket}'.")
    except Exception as e:
        logging.error(f"Error syncing buckets: {e}")
        sys.exit(1)
    
    if not dry_run:
        print(f"Data synced from '{source_bucket}' to '{destination_bucket}'.")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync objects from a source S3 bucket to a destination S3 bucket."
    )
    parser.add_argument(
        'source_bucket',
        help="The name of the source S3 bucket."
    )
    parser.add_argument(
        'destination_bucket',
        help="The name of the destination S3 bucket."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Simulate the sync operation without actually copying objects."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    sync_s3_buckets(args.source_bucket, args.destination_bucket, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
