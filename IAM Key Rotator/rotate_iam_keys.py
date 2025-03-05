#!/usr/bin/env python3
import boto3
import argparse
import logging
import sys

def rotate_iam_keys(username: str, dry_run: bool = False) -> None:
    """
    Rotate IAM access keys for the specified user.

    This function lists and deletes all existing access keys for the given IAM user
    and then creates a new access key. Use the dry run option to simulate the actions without making any changes.

    Args:
        username (str): The IAM username whose keys will be rotated.
        dry_run (bool): If True, simulate the deletion and creation process.
    """
    iam = boto3.client('iam')
    
    try:
        response = iam.list_access_keys(UserName=username)
        old_keys = response.get('AccessKeyMetadata', [])
    except Exception as e:
        logging.error(f"Failed to list access keys for user '{username}': {e}")
        sys.exit(1)
    
    if old_keys:
        for key in old_keys:
            key_id = key['AccessKeyId']
            if dry_run:
                print(f"Dry run: Would delete access key: {key_id} for user: {username}")
            else:
                try:
                    iam.delete_access_key(UserName=username, AccessKeyId=key_id)
                    print(f"Deleted access key: {key_id} for user: {username}")
                except Exception as e:
                    logging.error(f"Error deleting access key {key_id} for user '{username}': {e}")
    else:
        print(f"No existing access keys found for user '{username}'.")
    
    if dry_run:
        print("Dry run: Would create a new access key.")
    else:
        try:
            new_key = iam.create_access_key(UserName=username)
            access_key = new_key['AccessKey']
            print(f"New access key created for user '{username}':")
            print(f"  Access Key ID: {access_key['AccessKeyId']}")
            print(f"  Secret Access Key: {access_key['SecretAccessKey']}")
        except Exception as e:
            logging.error(f"Failed to create new access key for user '{username}': {e}")
            sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Rotate IAM access keys for a specified user by deleting existing keys and creating a new one."
    )
    parser.add_argument(
        'username',
        help="The IAM username whose access keys will be rotated."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simulate the key rotation without making any changes."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    rotate_iam_keys(args.username, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
