# Data Backup & Restore

This project automates the management of AWS EC2 EBS volumes using Python and the Boto3 AWS SDK. The project consists of three key components:

1. **Creating Backups for EC2 Volumes**  
2. **Cleaning Up Old Snapshots**  
3. **Restoring EC2 Volumes from Snapshots**

## Technologies

- **Python**: Programming language used to write the scripts.
- **Boto3**: AWS SDK for Python to interact with AWS services like EC2.
- **AWS EC2**: Cloud service for provisioning and managing virtual servers (EC2 instances) and associated storage (EBS volumes).
- **AWS Snapshots**: A backup mechanism to create point-in-time copies of EBS volumes.

## Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your machine.
- **Boto3**: Install the Boto3 library to interact with AWS services. Install it via pip:
  ```bash
  pip install boto3
  ```

## Scripts
1. volume-backups.py
This script automatically creates snapshots for all EC2 volumes tagged with Environment: dev. It is intended to create backups of volumes on a regular basis.

```python
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

```

This script queries EC2 for volumes tagged with Environment: dev and creates snapshots every 12 hours.
The schedule library runs the snapshot creation function periodically.
The boto3.client is used to interact with AWS EC2, and describe_volumes fetches the list of volumes.


2. cleanup-snapshots.py
This script cleans up old EC2 snapshots by retaining only the most recent snapshots for each volume. It is useful for managing snapshot retention.

```python
import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="us-east-1")

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'tag:Environment',
            'Values': ['dev']
        }
    ]
)

for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    for snap in sorted_by_date[2:]:
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        print(response)
```

This script lists all snapshots for volumes tagged with Environment: dev and sorts them by the creation date.
It keeps only the most recent two snapshots and deletes older ones.


3. restore-volume.py
This script restores a volume from the latest snapshot of a given EC2 instance. It creates a new volume from the most recent snapshot and attaches it to the instance.

```python
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

```

This script identifies the EC2 instance's volume, finds the most recent snapshot, and creates a new volume from it.
After the volume is created, it waits for it to become available and attaches it to the instance.


## Conclusion
This project helps automate EC2 volume backup and restore operations, making it easier to manage your AWS infrastructure by maintaining an efficient snapshot lifecycle.
