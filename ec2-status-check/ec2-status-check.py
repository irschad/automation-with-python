# Import the boto3 library for AWS SDK and schedule library for task scheduling
import boto3
import schedule

# Create an EC2 client to interact with the AWS EC2 service in the specified region (us-east-1)
ec2_client = boto3.client('ec2', region_name="us-east-1")

# Define a function to check and display the status of EC2 instances
def check_instance_status():
    # Retrieve the instance statuses, including those not in the running state
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    # Iterate over the retrieved instance statuses and print details for each
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']  # Current state of the instance (e.g., running)
        print(f"Instance {status['InstanceId']} is {state} with instance status {ins_status} and system status {sys_status}")
    print("#############################\n")  # Separator for readability in output

# Schedule the check_instance_status function to run every 5 seconds
schedule.every(5).seconds.do(check_instance_status)

# Infinite loop to keep the scheduling active
while True:
    # Run any scheduled tasks that are due
    schedule.run_pending()
