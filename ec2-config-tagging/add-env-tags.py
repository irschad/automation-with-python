import boto3

# Create an EC2 client and resource for the us-east-1 region
ec2_client_us = boto3.client('ec2', region_name="us-east-1")
ec2_resource_us = boto3.resource('ec2', region_name="us-east-1")

# Create an EC2 client and resource for the eu-west-3 (Paris) region
ec2_client_paris = boto3.client('ec2', region_name="eu-west-3")
ec2_resource_paris = boto3.resource('ec2', region_name="eu-west-3")

# Lists to store instance IDs from each region
instance_ids_us = []
instance_ids_paris = []

# Retrieve and store all instance IDs from the us-east-1 region
reservations_us = ec2_client_us.describe_instances()['Reservations']
for res in reservations_us:
    instances = res['Instances']
    for ins in instances:
        instance_ids_us.append(ins['InstanceId'])

# Add a "prod" tag to all instances in the us-east-1 region
response = ec2_resource_us.create_tags(
    Resources=instance_ids_us,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

# Retrieve and store all instance IDs from the eu-west-3 (Paris) region
reservations_paris = ec2_client_paris.describe_instances()['Reservations']
for res in reservations_paris:
    instances = res['Instances']
    for ins in instances:
        instance_ids_paris.append(ins['InstanceId'])

# Add a "dev" tag to all instances in the eu-west-3 region
response = ec2_resource_paris.create_tags(
    Resources=instance_ids_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)
