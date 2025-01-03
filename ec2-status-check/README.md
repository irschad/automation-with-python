# Health Check: EC2 Status Checks

## Overview
The **Health Check: EC2 Status Checks** project automates the monitoring of EC2 instances' statuses on AWS using Python and Boto3. The project integrates infrastructure provisioning with Terraform and Python scripting to provide real-time updates on instance statuses.

## Features
- **EC2 Instance Provisioning**: Automate EC2 instance creation using Terraform.
- **Real-Time Status Monitoring**: Continuously monitor the status of EC2 instances.
- **Interval Scheduling**: Python script fetches and displays EC2 statuses at a specified interval.
- **AWS Integration**: Uses Boto3 to interact seamlessly with AWS EC2 services.

---

## Technologies Used
- **Python**: For scripting and automation.
- **Boto3**: AWS SDK for Python to interact with EC2 services.
- **Terraform**: Infrastructure as Code (IaC) tool for provisioning EC2 instances.
- **AWS**: Cloud provider for EC2 instance hosting.

---

## Getting Started

### Prerequisites
- Python 3.7 or later
- Terraform
- AWS CLI configured with valid credentials
- AWS account with access to EC2 services
- Install required Python dependencies:
  ```bash
  pip install boto3
  pip install schedule
  ```

---

### Initial set-up

#### Set Up Python Environment
```bash
pip install boto3 schedule
```

#### Provision EC2 Instances with Terraform
1. Navigate to the Terraform directory:
   ```bash
   cd terraform
   ```
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Create a plan:
   ```bash
   terraform plan -out=tfplan
   ```
4. Apply the plan:
   ```bash
   terraform apply tfplan
   ```
5. Note the IDs of the provisioned EC2 instances for reference.

---

### Usage

#### Run the Python Script
1. Navigate to the project directory.
2. Execute the script:
   ```bash
   python ec2-status-check.py
   ```

The script will continuously check the statuses of all EC2 instances in the `us-east-1` region at 5-second intervals and print the following details:
- Instance ID
- Current state (e.g., running, stopped)
- Instance status
- System status

---

## Explanation of the Python script

The `ec2-status-check.py` script monitors the status of EC2 instances in real-time:

1. **Importing Libraries**:
   - `boto3`: AWS SDK for Python, used to interact with EC2 services.
   - `schedule`: A library for scheduling tasks at regular intervals.

2. **Creating an EC2 Client**:
   - `ec2_client = boto3.client('ec2', region_name="us-east-1")`
   - Initializes a connection to the EC2 service in the specified AWS region (`us-east-1`).

3. **Defining the Status Check Function**:
   - `check_instance_status()` fetches and prints the status of all EC2 instances:
     - Uses `ec2_client.describe_instance_status(IncludeAllInstances=True)` to retrieve status data.
     - Iterates over `statuses['InstanceStatuses']` to extract and print details:
       - `Instance ID`
       - `Current state` (e.g., running, stopped)
       - `Instance status` (health check result of the instance)
       - `System status` (health check result of the underlying hardware).

4. **Scheduling the Status Check**:
   - `schedule.every(5).seconds.do(check_instance_status)` runs the status check every 5 seconds.

5. **Running the Scheduler**:
   - The script enters an infinite loop (`while True`) to continuously execute any due scheduled tasks using `schedule.run_pending()`.

---


## Acknowledgments
- AWS Documentation: [Boto3 EC2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
- Terraform Documentation: [Terraform by HashiCorp](https://www.terraform.io/)
