#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def create_rds_snapshot(db_instance_identifier: str, snapshot_id: str, dry_run: bool = False) -> None:
    """
    Create an RDS snapshot for a specified DB instance.

    Args:
        db_instance_identifier (str): The identifier of the RDS DB instance.
        snapshot_id (str): The identifier for the snapshot to be created.
        dry_run (bool): If True, simulate the snapshot creation without executing it.
    """
    if dry_run:
        print(f"Dry run: Would create snapshot '{snapshot_id}' for DB instance '{db_instance_identifier}'.")
        return

    rds = boto3.client('rds')
    try:
        response = rds.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_id,
            DBInstanceIdentifier=db_instance_identifier
        )
        print(f"Snapshot '{snapshot_id}' created for DB instance '{db_instance_identifier}'.")
        print("Response:", response)
    except Exception as e:
        logging.error(f"Error creating snapshot '{snapshot_id}' for DB instance '{db_instance_identifier}': {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an RDS snapshot for a specified DB instance."
    )
    parser.add_argument(
        "db_instance_identifier",
        help="The identifier of the RDS DB instance (e.g., my-db-instance)."
    )
    parser.add_argument(
        "snapshot_id",
        help="The identifier for the snapshot (e.g., my-db-snapshot)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the snapshot creation without executing it."
    )
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    create_rds_snapshot(args.db_instance_identifier, args.snapshot_id, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
