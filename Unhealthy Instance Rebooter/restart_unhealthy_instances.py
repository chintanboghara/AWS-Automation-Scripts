import boto3
import logging
from botocore.exceptions import ClientError

# Initialize a session using Amazon EC2
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_REGION_NAME'
)

ec2 = session.client('ec2')


def get_unhealthy_instances():
    """Retrieve unhealthy EC2 instances."""
    try:
        response = ec2.describe_instance_status(
            Filters=[{'Name': 'instance-status.status', 'Values': ['impaired']}]
        )
        return [instance['InstanceId'] for instance in response['InstanceStatuses']]
    except ClientError as e:
        logging.error(e)
        return []


def reboot_instances(instance_ids):
    """Reboot the given EC2 instances."""
    try:
        ec2.reboot_instances(InstanceIds=instance_ids)
        logging.info(f'Rebooted instances: {instance_ids}')
    except ClientError as e:
        logging.error(e)


def main():
    """Main function to reboot unhealthy instances."""
    unhealthy_instances = get_unhealthy_instances()
    if unhealthy_instances:
        reboot_instances(unhealthy_instances)
    else:
        logging.info('No unhealthy instances found.')


if __name__ == '__main__':
    main()
