# Command to Run the Script

- **To tag an EC2 instance:**
  ```bash
  python tag_ec2_instance.py i-1234567890abcdef0 --tags Owner=DevOps --tags Environment=Production
  ```

- **To simulate tagging without making changes (dry run):**
  ```bash
  python tag_ec2_instance.py i-1234567890abcdef0 --tags Owner=DevOps --dry-run
  ```
