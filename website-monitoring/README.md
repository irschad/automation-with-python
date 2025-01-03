# Website Monitoring and Recovery

## Project Overview

This project automates the monitoring and recovery of a website hosted on an EC2 instance. It involves creating a server on Amazon EC2, installing Docker, running a web application within a Docker container, and monitoring the website's availability. If the website is down, the system will send email notifications, automatically restart the application, and reboot the server to ensure uptime.

## Technologies

- **Python**: For writing the monitoring and recovery logic.
- **Amazon EC2**: For hosting the web application and running the Docker container.
- **Docker**: For containerizing the web application.
- **Linux**: EC2 instance runs Ubuntu (or any other distribution), and the monitoring script is executed within it.

## Features

- **Website Monitoring**: Continuously monitors the website's HTTP status.
- **Email Notification**: Sends email alerts when the website is down.
- **Automated Recovery**: Restarts the Docker container and EC2 instance if necessary.
- **Scheduling**: Monitors the website at regular intervals (every 5 minutes).

## Setup Instructions

### 1. Prerequisites

- An **EC2** instance running a Linux distribution (Ubuntu is assumed).
- **Docker** installed on the EC2 instance.
- A web application running inside a Docker container.
- Python 3.x installed.
- Install necessary Python libraries:
    ```bash
    pip install boto3 requests paramiko schedule
    ```

### 2. Environment Variables

Ensure the following environment variables are set in your EC2 instance:
- `EMAIL_ADDRESS`: The sender's email address (e.g., Gmail).
- `EMAIL_PASSWORD`: The password for the sender's email account (use App Password if using Gmail 2FA).
- `INSTANCE_ID`: The AWS EC2 instance ID.
- `EC2_HOSTNAME`: The public IP or DNS of the EC2 instance.
- `SSH_KEY_PATH`: The path to the SSH private key used for connecting to the EC2 instance.


### 3. Running the Monitoring Script
Save the Python script (monitor-website.py) to your EC2 instance and run it:
```bash
python monitor-website.py
```

### 4. Docker Container Configuration
Ensure your Docker container is running a web application, for example:
```bash
sudo docker run -d -p 8080:80 your-web-app-image
```

#### Python Script Breakdown
1. **Imports and Environment Setup**
  ```python
  import boto3
  import requests
  import smtplib
  import os
  import paramiko
  import time
  import schedule
  ```

  - boto3: AWS SDK for Python, used to interact with EC2.
  - requests: Used to send HTTP requests to check if the website is reachable.
  - smtplib: Used for sending email notifications when the website is down.
  - paramiko: Used for SSH connections to the EC2 instance to restart Docker containers.
  - os: Access environment variables (e.g., email credentials, instance ID).
  - time: For adding delays during instance monitoring and recovery.
  - schedule: To schedule the monitoring task to run periodically.

2. **EC2 Client Initialization**
   ```python
   ec2_client = boto3.client('ec2', region_name="us-east-1")
   ```
   - This initializes the AWS EC2 client to interact with the EC2 instance and manage its lifecycle (e.g., reboot).

3. **Restart EC2 and Docker Container**
   ```python
   def restart_server_and_container():
    print('Rebooting the EC2 instance...')
    ec2_client.reboot_instances(InstanceIds=[INSTANCE_ID])  # Reboot EC2

    while True:
        response = ec2_client.describe_instance_status(InstanceIds=[INSTANCE_ID])
        statuses = response['InstanceStatuses']
        if statuses and statuses[0]['InstanceState']['Name'] == 'running':
            print('Instance is running again.')
            time.sleep(20)
            restart_container()
            break
        print('Waiting for instance to be running...')
        time.sleep(5)
    ```
    - Reboots the EC2 instance and waits until the instance is back in the "running" state before restarting the Docker container.
    
4. **Restart Docker Container**
   ```python
   def restart_container():
    print('Restarting the application container...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=HOSTNAME, username='ubuntu', key_filename=SSH_KEY_PATH)
    stdin, stdout, stderr = ssh.exec_command('sudo docker start <container_id>')
    print(stdout.readlines())
    ssh.close()
   ```
   - Connects to the EC2 instance via SSH and restarts the Docker container using the provided container ID.
   
5. **Send Email Notification**
   ```python
   def send_notification(email_msg):
    print('Sending notification email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
   ```
   - Sends an email via Gmail's SMTP server notifying about the downtime of the application.

6. **Monitor website and recover, if needed**
    ```python
    def monitor_application():
    try:
        print("Monitoring application at hostname:", HOSTNAME)
        response = requests.get(f'http://{HOSTNAME}:8080/')
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application is down. Restarting...')
            msg = f'Application returned status code {response.status_code}'
            send_notification(msg)
            restart_container()
    except Exception as ex:
        print(f'Error: {ex}')
        msg = 'Application not accessible at all'
        send_notification(msg)
        restart_server_and_container()
    ```
    - Continuously checks if the web application is accessible by sending an HTTP request.
    - If the site is down (status code not 200), it restarts the container and sends an email notification.
    - If an error occurs (e.g., no response from the website), it restarts the EC2 instance and the Docker container.
        
7. **Schedule the monitoring task**
    '''python
    schedule.every(5).minutes.do(monitor_application)

    while True:
        schedule.run_pending()
        time.sleep(1)
    ```
    - Schedules the monitor_application() function to run every 5 minutes.
    - Keeps the script running continuously, checking the website at regular intervals.


---






