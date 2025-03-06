# Command to Run the Script

- **To perform the actual cleanup:**
  ```bash
  python cleanup_snapshots.py
  ```
- **To simulate the cleanup without deleting snapshots (dry run):**
  ```bash
  python cleanup_snapshots.py --dry-run
  ```
- **To use a custom retention period (e.g., 45 days):**
  ```bash
  python cleanup_snapshots.py --retention-days 45
  ```
