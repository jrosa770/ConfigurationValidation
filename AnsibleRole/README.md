## 📘 Overview
This role validates and enforces Cisco IOS device configurations using Ansible. It supports compliance checks for standard settings like DNS, AAA/TACACS, NTP, and more, using reusable assertion logic with automated remediation.

## 🧰 Features
- Modular task for checking and correcting configuration lines
- Supports Cisco IOS via `cisco.ios` modules
- Logs discrepancies to `outputs/failure_report.txt`
- Designed for use in **AWX/Tower** and CLI workflows

## 🧾 Requirements
- Ansible >= 2.10
- Cisco IOS network devices
- Ansible Collections:
  - `cisco.ios`

Install required collection:
```bash
ansible-galaxy collection install cisco.ios
```

## 📂 Directory Structure
```
ansible-cisco-compliance/
├── inventories/
│   └── production/
│       ├── hosts
│       └── group_vars/
│           └── all.yml
├── outputs/
│   └── failure_report.txt
├── playbooks/
│   └── validate_compliance.yml
└── roles/
    └── compliance_validator/
        ├── tasks/
        │   ├── main.yml
        │   └── check_policy.yml
        ├── vars/
        │   └── main.yml
        ├── defaults/
        │   └── main.yml
        └── templates/
            └── failure_report.txt.j2
```

## 🚀 Usage
### Command Line:
```bash
ansible-playbook -i inventories/production/hosts playbooks/validate_compliance.yml
```

### AWX / Ansible Tower
1. **Project**: Link to Git repo with this role structure
2. **Inventory**: Define Cisco devices (e.g., in `inventories/production/hosts`)
3. **Job Template**:
   - Playbook: `playbooks/validate_compliance.yml`
   - Credentials: Network CLI for Cisco (SSH)
4. **Extra Vars** (optional):
   ```yaml
   config_section_name: "Custom Section"
   config_lines:
     - custom config line 1
     - custom config line 2
   ```

## 🛠 Sample Inventory
**inventories/production/hosts**
```ini
[cisco]
192.0.2.10 ansible_user=admin ansible_password=yourpass ansible_network_os=cisco.ios.ios ansible_connection=network_cli
```

## 📄 Outputs
All failures are logged to:
```
outputs/failure_report.txt
```
Example entry:
```yaml
---
Host: 192.0.2.10
Section: DNS
Status: FAIL
Reason:
  - Line 'ip name-server 8.8.8.8' not found
```

## 🧩 Extending
To add new checks:
1. Add expected config list to `vars/main.yml`
2. Add `import_tasks` call in `tasks/main.yml` with:
   ```yaml
   config_section_name: "NewSection"
   config_lines: "{{ ios_newsection }}"
   config_variable: newsection_check
   ```

## 👤 Author
Jose Rosa

## 📘 License
MIT License 