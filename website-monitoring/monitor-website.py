import boto3
import requests
import smtplib
import os
import paramiko
import time
import schedule

# Environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # Email address for notifications
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # App password for Gmail SMTP
INSTANCE_ID = os.environ.get('INSTANCE_ID')  # EC2 instance ID to be managed
HOSTNAME = os.environ.get('EC2_HOSTNAME')  # Public or private IP of the EC2 instance
SSH_KEY_PATH = os.environ.get('SSH_KEY_PATH')  # Path to the private SSH key for EC2 access

# Initialize AWS EC2 client
ec2_client = boto3.client('ec2', region_name="us-east-1")  # Adjust region as needed

# Restarts the EC2 instance and ensures it is running before restarting the Docker container
def restart_server_and_container():
    print('Rebooting the EC2 instance...')
    print(ec2_client.describe_instance_status(InstanceIds=[INSTANCE_ID]))  # Log current instance status
    ec2_client.reboot_instances(InstanceIds=[INSTANCE_ID])  # Reboot the instance

    # Wait for the instance to transition to 'running' state
    while True:
        response = ec2_client.describe_instance_status(InstanceIds=[INSTANCE_ID])
        statuses = response['InstanceStatuses']
        if statuses and statuses[0]['InstanceState']['Name'] == 'running':
            print('Instance is running again.')
            time.sleep(20)  # Allow some time for the instance to fully initialize
            restart_container()  # Restart the application container
            break
        print('Waiting for instance to be running...')
        time.sleep(5)

# Connects to the EC2 instance via SSH and restarts the specified Docker container
def restart_container():
    print('Restarting the application container...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys
    ssh.connect(hostname=HOSTNAME, username='ubuntu', key_filename=SSH_KEY_PATH)  # Adjust username as per your AMI
    stdin, stdout, stderr = ssh.exec_command('sudo docker start 3f2f187d2906')  # Replace with your container ID
    print(stdout.readlines())  # Print command output for debugging
    ssh.close()

# Sends a notification email via Gmail SMTP when the application goes down
def send_notification(email_msg):
    print('Sending notification email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

# Monitor the application and attempt to restart if it's down and send email notification
def monitor_application():
    try:
        print("Monitoring application at hostname:", HOSTNAME)
        response = requests.get(f'http://{HOSTNAME}:8080/')
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application is down. Restarting...')
            msg = f'Application returned status code {response.status_code}'
            send_notification(msg)  # Notify about the issue
            restart_container()  # Restart the container
    except Exception as ex:
        print(f'Error: {ex}')
        msg = 'Application not accessible at all'
        send_notification(msg)  # Notify about the complete failure
        restart_server_and_container()  # Restart the server and container

# Schedule the monitoring task to run every 5 minutes
schedule.every(5).minutes.do(monitor_application)

# Keep the script running to check tasks at the scheduled intervals
while True:
    schedule.run_pending()
    time.sleep(1)
