# Command to Run the Script

- **To perform actual deletion:**
  ```bash
  python delete_old_s3_objects.py my-bucket --days 30
  ```

- **To simulate deletion (dry run):**
  ```bash
  python delete_old_s3_objects.py my-bucket --days 30 --dry-run
  ```
