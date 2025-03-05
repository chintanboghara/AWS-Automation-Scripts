# Command to Run the Script

- **To perform an actual export:**
  ```bash
  python export_dynamodb_to_s3.py my-table my-bucket backup.json
  ```

- **To simulate the export without uploading (dry run):**
  ```bash
  python export_dynamodb_to_s3.py my-table my-bucket backup.json --dry-run
  ```
