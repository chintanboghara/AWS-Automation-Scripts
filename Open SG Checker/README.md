# Command to Run the Script

- **To check for security groups with default open access (0.0.0.0/0):**
  ```bash
  python check_open_security_groups.py
  ```

- **To check for security groups with a custom CIDR (e.g., 192.168.1.0/24):**
  ```bash
  python check_open_security_groups.py --cidr 192.168.1.0/24
  ```
