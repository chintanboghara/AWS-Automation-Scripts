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
  This AWS SDK for Python is required to interact with AWS services. Install it via pip:
  ```bash
  pip install boto3
  ```

- **AWS CLI (Optional but recommended)**  
  The AWS Command Line Interface helps manage AWS credentials and configurations. Install it from the [AWS CLI official page](https://aws.amazon.com/cli/).

- **AWS Credentials**  
  Configure AWS credentials so that the scripts can authenticate with your AWS account:
  ```bash
  aws configure
  ```
  Alternatively, set the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

## Creating a Virtual Environment

It's a good practice to use a virtual environment to manage dependencies. Follow these steps:

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies within the virtual environment:**
   ```bash
   pip install boto3
   ```
