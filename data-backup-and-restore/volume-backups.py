import boto3
import schedule

# Initialize the EC2 client for the us-east-1 region
ec2_client = boto3.client('ec2', region_name="us-east-1")


def create_volume_snapshots():
    """
    Function to create snapshots for all EBS volumes tagged with 'Environment: dev'.
    """
    # Retrieve all volumes with the 'Environment' tag set to 'dev'
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Environment',
                'Values': ['dev']
            }
        ]
    )
    # Iterate over the list of volumes
    for volume in volumes['Volumes']:
        try:
            # Attempt to create a snapshot for each volume
            new_snapshot = ec2_client.create_snapshot(
                VolumeId=volume['VolumeId']
            )
            print(f"Snapshot created: {new_snapshot}")
        except Exception as e:
            # Handle errors during snapshot creation
            print(f"Failed to create snapshot for VolumeId {volume['VolumeId']}: {str(e)}")


# Schedule the snapshot creation function to run every 12 hours
schedule.every(12).hours.do(create_volume_snapshots)

# Keep the script running to execute scheduled tasks
while True:
    schedule.run_pending()
