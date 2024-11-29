import boto3
from operator import itemgetter

# Create EC2 client and resource objects for the 'us-east-1' region
ec2_client = boto3.client('ec2', region_name="us-east-1")
ec2_resource = boto3.resource('ec2', region_name="us-east-1")

# ID of the EC2 instance where operations will be performed
instance_id = "i-04e7a8ab01a267cce"

# Get the list of volumes attached to the specified instance
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

# Assume there is at least one volume attached and fetch the first one
instance_volume = volumes['Volumes'][0]

# Fetch all snapshots owned by the user for the specified volume
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],  # Look for snapshots owned by the current AWS account
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

# Sort snapshots by creation time in descending order and pick the latest one
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])  # Print the start time of the latest snapshot

# Create a new volume from the latest snapshot in the specified availability zone
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="us-east-1a",
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Environment',
                    'Value': 'dev'
                }
            ]
        }
    ]
)

# Wait for the new volume to become available before attaching it to the instance
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)  # Print the current state of the volume
    if vol.state == 'available':  # Check if the volume is in the 'available' state
        # Attach the new volume to the specified instance
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'  # Specify the device name for the attached volume
        )
        break  # Exit the loop once the volume is attached
