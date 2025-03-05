#!/usr/bin/env python3
import boto3
import argparse
import datetime
import logging
import sys

def delete_old_s3_objects(bucket_name: str, days: int = 30, dry_run: bool = False) -> None:
    """
    Delete S3 objects in the specified bucket that are older than the given number of days.

    Args:
        bucket_name (str): The name of the S3 bucket.
        days (int): Delete objects older than this number of days.
        dry_run (bool): If True, simulate deletion without actually removing objects.
    """
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
    except Exception as e:
        logging.error(f"Error listing objects in bucket '{bucket_name}': {e}")
        sys.exit(1)
    
    objects = response.get('Contents', [])
    if not objects:
        print(f"No objects found in bucket '{bucket_name}'.")
        return

    now = datetime.datetime.now(datetime.timezone.utc)
    for obj in objects:
        last_modified = obj.get('LastModified')
        if not last_modified:
            continue
        age = (now - last_modified).days
        if age > days:
            if dry_run:
                print(f"Dry run: Would delete '{obj['Key']}' (Age: {age} days)")
            else:
                try:
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    print(f"Deleted '{obj['Key']}' from '{bucket_name}' (Age: {age} days)")
                except Exception as e:
                    logging.error(f"Error deleting object '{obj['Key']}' from bucket '{bucket_name}': {e}")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete S3 objects older than a specified number of days."
    )
    parser.add_argument(
        'bucket_name',
        help="The name of the S3 bucket."
    )
    parser.add_argument(
        '--days', type=int, default=30,
        help="Delete objects older than this number of days. Default is 30."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Simulate deletion without actually deleting any objects."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    delete_old_s3_objects(args.bucket_name, days=args.days, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
