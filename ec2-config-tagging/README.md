# Automate Configuring EC2 Server Instances

## Project Overview
This project demonstrates automating the process of adding environment-specific tags to EC2 server instances across multiple AWS regions using Python and Boto3. Environment tags, such as `prod` or `dev`, are essential for resource management, cost tracking, and organizing cloud infrastructure efficiently.

## Features
- Automates tagging EC2 instances in specified AWS regions.
- Tags instances with environment-specific tags (`prod` for `us-east-1` and `dev` for `eu-west-3`).
- Uses Python and Boto3 for scripting and interaction with AWS services.

## Prerequisites
1. **Python Environment**: Ensure Python 3.x is installed on your system.
2. **AWS CLI Setup**: Install and configure the AWS CLI with appropriate credentials and permissions to manage EC2 instances.
3. **Boto3**: Install the AWS SDK for Python using pip:
   ```bash
   pip install boto3
   ```
4. **IAM Permissions**: Ensure the IAM user or role running the script has the following permissions:
   - `ec2:DescribeInstances`
   - `ec2:CreateTags`

## Python Script: `add-env-tags.py`
This script automates the tagging of EC2 instances across the `us-east-1` and `eu-west-3` regions. Below is a detailed explanation of its functionality.

### Script Walkthrough
```python
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
```

### Code Highlights
1. **AWS Region Setup**: The script interacts with two regions, `us-east-1` and `eu-west-3`. You can modify the regions or add more based on your requirements.

2. **Retrieving Instances**: The script retrieves all EC2 instance IDs using `describe_instances`. Each instance ID is stored in a list corresponding to its region.

3. **Tagging Instances**: Environment-specific tags are applied using the `create_tags` method of the EC2 resource object. Tags help organize and manage resources effectively.

### Key Functions and Methods
- `boto3.client('ec2')`: Initializes an EC2 client for API interactions.
- `boto3.resource('ec2')`: Creates a resource object for higher-level actions on AWS services.
- `describe_instances()`: Retrieves details about EC2 instances, including their IDs.
- `create_tags(Resources, Tags)`: Applies tags to specified resources.

### Output
The script applies the following tags:
- `environment: prod` to all instances in `us-east-1`.
- `environment: dev` to all instances in `eu-west-3`.

## Usage Instructions
1. Save the script as `add-env-tags.py`.
2. Run the script using Python:
   ```bash
   python add-env-tags.py
   ```
3. Verify that the tags have been applied by checking the AWS Management Console or using the AWS CLI:
   ```bash
   aws ec2 describe-instances --region us-east-1
   aws ec2 describe-instances --region eu-west-3
   ```

## Conclusion
This project highlights how Python and Boto3 can automate routine AWS tasks, saving time and ensuring consistency in resource management. By tagging EC2 instances with environment identifiers, this script lays the groundwork for better cloud infrastructure organization.
