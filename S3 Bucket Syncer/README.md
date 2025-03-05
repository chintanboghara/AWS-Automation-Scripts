# Command to Run the Script

- **To perform an actual sync:**
  ```bash
  python sync_s3_buckets.py source-bucket-name destination-bucket-name
  ```

- **To simulate the sync without making changes (dry run):**
  ```bash
  python sync_s3_buckets.py source-bucket-name destination-bucket-name --dry-run
  ```
