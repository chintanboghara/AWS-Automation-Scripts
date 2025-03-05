# Steps to Run the Script

1. **Install Dependencies:**  
   Make sure you have Python installed (version 3.6 or higher recommended) and install the `boto3` package if you haven’t already:
   ```bash
   pip install boto3
   ```

2. **Configure AWS Credentials:**  
   Ensure your AWS credentials are set up. You can do this by running:
   ```bash
   aws configure
   ```
   This will prompt you for your AWS Access Key, Secret Key, region, and output format. Alternatively, set the credentials using environment variables.

3. **Save the Script:**  
   Save the refined script to a file, for example: `manage_ec2.py`.

4. **Make the Script Executable (Optional):**  
   On Linux or macOS, you can make the script executable:
   ```bash
   chmod +x manage_ec2.py
   ```

5. **Run the Script:**  
   Use the following command format to run the script:
   ```bash
   python manage_ec2.py <instance_id> <action>
   ```
   For example, to start an instance with ID `i-0123456789abcdef0`:
   ```bash
   python manage_ec2.py i-0123456789abcdef0 start
   ```
   If you made the script executable and have the proper shebang (`#!/usr/bin/env python3`), you can also run it directly:
   ```bash
   ./manage_ec2.py i-0123456789abcdef0 start
   ```

6. **Review the Output:**  
   The script will print a confirmation that the action has been initiated along with the response from AWS. If there’s an error, it will display an error message.
