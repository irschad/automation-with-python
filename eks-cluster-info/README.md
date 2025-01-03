# Automate Displaying EKS Cluster Information

## Overview
This project automates the process of retrieving and displaying detailed information about Amazon Elastic Kubernetes Service (EKS) clusters using a Python script. By leveraging AWS's `boto3` SDK, the script lists all the EKS clusters in a specified AWS region, retrieves their status, endpoint, and version, and displays this information in a clear and concise format.

## Features
- Lists all EKS clusters in the specified AWS region.
- Retrieves and displays the status, endpoint, and version of each EKS cluster.
- Provides a simple and automated way to monitor EKS cluster details.

## Prerequisites
To run this project, ensure you have the following:
1. **Python 3.7 or higher** installed.
2. **AWS CLI** installed and configured with appropriate credentials.
3. The **`boto3` library** installed. You can install it using:
   ```bash
   pip install boto3
   ```
4. Proper AWS IAM permissions to:
   - List EKS clusters (`eks:ListClusters`).
   - Describe EKS clusters (`eks:DescribeCluster`).

## Installation
1. Navigate to the project directory:
   ```bash
   cd eks-cluster-info
   ```
2. Ensure you have the `boto3` library installed:
   ```bash
   pip install boto3
   ```

## Usage
1. Run the script using Python:
   ```bash
   python eks-cluster-status-check.py
   ```
2. The script will output details about all the EKS clusters in the specified region, including their:
   - Status
   - Endpoint
   - Version

### Example Output
```plaintext
Cluster my-eks-cluster-1 status is ACTIVE
Cluster endpoint: https://<cluster-endpoint>
Cluster version: 1.31
```

## Customization
- **Region**: Modify the `region_name` parameter in the script to target a different AWS region.
- **Output Format**: Enhance the script to write cluster details to a file (e.g., CSV or JSON) for better record-keeping.

## Project File
- `eks-cluster-status-check.py`: The main Python script that retrieves and displays EKS cluster information.

## Description of Python Code

The `eks-cluster-status-check.py` Python script interacts with AWS EKS using the `boto3` SDK to automate the retrieval and display of information about EKS clusters. Here's an overview of how the code works:

1. **Setup AWS EKS Client**:  
   The script creates a client for EKS using the `boto3.client()` function. The `region_name` parameter specifies the AWS region to query for EKS clusters.
   ```python
   client = boto3.client('eks', region_name="us-east-1")
   ```

2. **List Clusters**:
   It then lists all EKS clusters in the region using the list_clusters() method. This returns a list of cluster names.
   ```python
   clusters = client.list_clusters()['clusters']
   ```

3. **Describe Clusters**:
   For each cluster, the script calls describe_cluster() to retrieve detailed information about the cluster, including its status, endpoint, and version.
   ```python
   response = client.describe_cluster(name=cluster)
   ```
    
 4. **Extract and Display Cluster Information**:
   The relevant information (status, endpoint, version) is extracted from the response and printed in a user-friendly format.
   ```python 
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']
    
    print(f"Cluster {cluster} status is {cluster_status}")
    print(f"Cluster endpoint: {cluster_endpoint}")
    print(f"Cluster version: {cluster_version}")
   ```
    
    ---
