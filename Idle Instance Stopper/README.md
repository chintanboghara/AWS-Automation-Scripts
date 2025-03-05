# Command to Run the Script

- **To actually stop idle instances (core count below 5 by default):**
  ```bash
  python stop_idle_instances.py --threshold 5
  ```

- **To perform a dry run (simulate stopping without actual action):**
  ```bash
  python stop_idle_instances.py --threshold 5 --dry-run
  ```
