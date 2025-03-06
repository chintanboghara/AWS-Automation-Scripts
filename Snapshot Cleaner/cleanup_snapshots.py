#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys
from datetime import datetime, timezone

def cleanup_snapshots(retention_days: int = 30, dry_run: bool = False) -> None:
    """
    Delete EC2 snapshots older than the specified retention period.

    Args:
        retention_days (int): Snapshots older than this number of days will be deleted.
        dry_run (bool): If True, simulate deletion without actually deleting snapshots.
    """
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_snapshots(OwnerIds=['self'])
        snapshots = response.get('Snapshots', [])
    except Exception as e:
        logging.error(f"Error retrieving snapshots: {e}")
        sys.exit(1)

    now = datetime.now(timezone.utc)
    deleted_any = False

    for snapshot in snapshots:
        start_time = snapshot.get('StartTime')
        if start_time is None:
            continue
        age_days = (now - start_time).days
        if age_days > retention_days:
            snapshot_id = snapshot.get('SnapshotId')
            if dry_run:
                print(f"Dry run: Would delete snapshot {snapshot_id} (Age: {age_days} days)")
            else:
                try:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted snapshot {snapshot_id} (Age: {age_days} days)")
                    deleted_any = True
                except Exception as e:
                    logging.error(f"Error deleting snapshot {snapshot_id}: {e}")

    if not deleted_any and not dry_run:
        print("No snapshots older than the retention period were found.")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean up EC2 snapshots older than a specified number of days."
    )
    parser.add_argument(
        "--retention-days",
        type=int,
        default=30,
        help="Retention period in days (default: 30). Snapshots older than this will be deleted."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deletion without actually deleting any snapshots."
    )
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    cleanup_snapshots(retention_days=args.retention_days, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
