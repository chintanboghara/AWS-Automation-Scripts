# AWS Automation Scripts

This repository contains a collection of Python scripts for automating AWS operations using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

## Installation

- **Python 3.6+**  
  Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

- **pip**  
  The Python package installer should come with Python. Verify it with:
  ```bash
  pip --version
  ```

- **boto3**  
  This AWS SDK for Python is required to interact with AWS services. You can install it via pip:
  ```bash
  pip install boto3
  ```

- **AWS CLI (Optional but recommended)**  
  The AWS Command Line Interface helps manage AWS credentials and configurations. Install it from the [AWS CLI official page](https://aws.amazon.com/cli/).

- **AWS Credentials**  
  Configure AWS credentials so that the scripts can authenticate with your AWS account.
  ```bash
  aws configure
  ```
  Alternatively, set the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

![AWS-Automation-Scripts](https://github.com/user-attachments/assets/bb616579-a208-4023-b73b-38a9f3f62e42)
