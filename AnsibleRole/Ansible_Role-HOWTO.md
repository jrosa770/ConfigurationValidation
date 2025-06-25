```
# Directory structure for Ansible Cisco Compliance Role

# Root folder: ansible-cisco-compliance/
# ├── roles/
# │   └── compliance_validator/
# │       ├── tasks/
# │       │   ├── main.yml
# │       │   └── check_policy.yml
# │       ├── vars/
# │       │   └── main.yml
# │       ├── defaults/
# │       │   └── main.yml
# │       └── templates/
# │           └── failure_report.txt.j2
# ├── inventories/
# │   └── production/
# │       ├── hosts
# │       └── group_vars/
# │           └── all.yml
# ├── playbooks/
# │   └── validate_compliance.yml
# └── outputs/
#     └── failure_report.txt

```
```yml
# ----------------------------
# roles/compliance_validator/tasks/main.yml
# ----------------------------
- name: Run Compliance Policy Checks
  import_tasks: check_policy.yml
  vars:
    config_section_name: "DNS"
    config_lines: "{{ ios_domain }}"
    config_variable: dns_check

- import_tasks: check_policy.yml
  vars:
    config_section_name: "AAA"
    config_lines: "{{ ios_aaa_tacacs }}"
    config_variable: aaa_check

- import_tasks: check_policy.yml
  vars:
    config_section_name: "NTP"
    config_lines: "{{ ios_ntp }}"
    config_variable: ntp_check

# ----------------------------
# roles/compliance_validator/tasks/check_policy.yml
# ----------------------------
- name: Validate {{ config_section_name }} Configuration
  block:
    - name: Assert expected {{ config_section_name }} lines exist
      ansible.builtin.assert:
        that:
          - "item in ansible_net_config"
        fail_msg: "{{ config_section_name }} line '{{ item }}' is missing"
        success_msg: "{{ config_section_name }} line '{{ item }}' is present"
      loop: "{{ config_lines }}"
      register: "{{ config_variable }}"

  rescue:
    - name: Apply missing {{ config_section_name }} lines
      cisco.ios.ios_config:
        lines: "{{ item }}"
      loop: "{{ config_lines }}"

    - name: Set failure result fact
      set_fact:
        check_result:
          host: "{{ inventory_hostname }}"
          section: "{{ config_section_name }}"
          status: "FAIL"
          message: "{{ lookup('vars', config_variable).results | to_nice_yaml }}"

    - name: Log failure to file
      lineinfile:
        insertafter: EOF
        create: yes
        dest: "outputs/failure_report.txt"
        line: |
          ---
          Host: {{ check_result.host }}
          Section: {{ check_result.section }}
          Status: {{ check_result.status }}
          Reason:
          {{ check_result.message | indent(2) }}

  always:
    - debug:
        msg: "Finished checking {{ config_section_name }}."

# ----------------------------
# roles/compliance_validator/vars/main.yml
# ----------------------------
ios_domain:
  - ip domain-name corp.local
  - ip name-server 8.8.8.8

ios_aaa_tacacs:
  - aaa new-model
  - tacacs-server host 10.10.10.1

ios_ntp:
  - ntp server 192.168.1.1

# ----------------------------
# playbooks/validate_compliance.yml
# ----------------------------
- name: Cisco Compliance Validation
  hosts: cisco
  gather_facts: false
  vars_files:
    - "../roles/compliance_validator/vars/main.yml"
  tasks:
    - name: Gather configuration facts
      cisco.ios.ios_facts:
        gather_subset: config

    - name: Run compliance validator role
      include_role:
        name: compliance_validator
```