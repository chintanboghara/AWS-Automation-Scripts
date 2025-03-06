# Command to Run the Script

- **To create the CloudWatch alarm:**

  ```bash
  python create_cloudwatch_alarm.py i-1234567890abcdef0 --sns-topic-arn arn:aws:sns:region:account-id:topic --threshold 70.0
  ```

- **To simulate the creation (dry run):**

  ```bash
  python create_cloudwatch_alarm.py i-1234567890abcdef0 --sns-topic-arn arn:aws:sns:region:account-id:topic --threshold 70.0 --dry-run
  ```
