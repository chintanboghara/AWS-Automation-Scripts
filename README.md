[![Lint Code Base](https://github.com/chintanboghara/AWS-Automation-Scripts/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/chintanboghara/AWS-Automation-Scripts/actions/workflows/ci.yml)

# AWS Automation Scripts

This repository contains a collection of Python scripts designed to automate various AWS operations using the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library. These scripts aim to simplify and streamline common AWS tasks, making it easier to manage your AWS resources programmatically.

## Installation

### Prerequisites

- **Python 3.6+**: Required for certain language features used in the scripts. Download from [python.org](https://www.python.org/downloads/).
- **pip**: Ensure it's up to date by running:
  ```bash
  pip install --upgrade pip
  ```
- **boto3**: The AWS SDK for Python. Install via:
  ```bash
  pip install boto3
  ```
- **AWS CLI** (optional but recommended): Simplifies credential management and provides additional AWS tools. Install from the [AWS CLI official page](https://aws.amazon.com/cli/).

### Setting up the Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chintanboghara/AWS-Automation-Scripts.git
   cd AWS-Automation-Scripts
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install boto3
   ```

5. **Configure AWS credentials:**
   Choose one of the following methods:
   - Run:
     ```bash
     aws configure
     ```
     Follow the prompts to set your access key, secret key, region, and output format.
   - Set environment variables:
     ```bash
     export AWS_ACCESS_KEY_ID=your_access_key
     export AWS_SECRET_ACCESS_KEY=your_secret_key
     export AWS_DEFAULT_REGION=your_region
     ```
     If using temporary credentials, also set:
     ```bash
     export AWS_SESSION_TOKEN=your_session_token
     ```
   - Use an AWS credentials file. See [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for details.

   After you're finished, deactivate the virtual environment by running:
   ```bash
   deactivate
   ```

## Usage

To use these scripts, navigate to the script's directory and run it with Python. For example:

```bash
python script_name.py
```
