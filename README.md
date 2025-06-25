# Configuration Validation 

## Prerequisites

Before diving in, it's important to assume a working familiarity with:

    * Ansible and its core modules
    * Vendor-specific modules like cisco.ios.ios_facts, ios_command, and ios_config
    * YAML syntax and structure

This is critical, as the playbook expects input configuration lines to be structured in YAML format—not plain text. 

 The Validation Playbook

Let’s walk through the core elements of the playbook.

> Key Highlights

    1. Inventory Targeting The playbook runs against a host group named cisco, as defined in your Ansible inventory.
    2. External Variable File A pointer is provided to ./vars/policies.yml, which should contain expected configuration lines in a structured YAML format.
    3. Authentication Task Inclusion A separate set of login or session initialization tasks is imported via default-authentication-tasks.yml.
    4. Configuration Gathering The cisco.ios.ios_facts module is used to extract the device’s current configuration using the config subset. The result is stored in the variable device_cfg.
    5. Error Handling A rescue block ensures that any failure during configuration retrieval is gracefully captured and logged for troubleshooting.
    6. Policy Checking After collecting the device configuration, the playbook imports another task file—check_policies.yml—that performs compliance checks using assertions.

### Purpose of check_policies.yml

The file check_policies.yml is an imported task file (via import_tasks) used to validate configurations on Cisco devices against a known good policy defined in variables (typically in a policies.yml file). It performs structured checks using Ansible's assert and rescue features. 

### How It Works

> Policy Input:

```yml
---
ios_domain:
    - 'ip domain-lookup'
    - 'ip name-server 208.67.222.222 208.67.220.220'
ios_aaa_tacacs:
    - 'aaa new-model'
    - 'aaa group server tacacs+ TACACS'
    - ' server name tac01'
    - ' server name tac02'
    - 'aaa authentication login default group TACACS local'
    - 'aaa authentication enable default group TACACS enable'
    - 'aaa authentication console local'
    - 'aaa authorization config-commands'
    - 'aaa authorization exec default group TACACS if-authenticated'
    - 'aaa authorization commands 7 default group TACACS local if-authenticated'
    - 'aaa authorization commands 15 default group TACACS local if-authenticated'
    - 'aaa accounting exec default start-stop group TACACS'
    - 'aaa accounting commands 7 default start-stop group TACACS'
    - 'aaa accounting commands 15 default start-stop group TACACS'
    - 'tacacs-server directed-request'
    - 'tacacs server tac01'
    - ' address ipv4 10.0.0.1'
    - ' key 7 123456789'
    - 'tacacs server tac02'
    - ' address ipv4 10.0.0.2'
    - ' key 7 123456789'
    - 'ip tacacs source-interface Loopback0'
ios_ntp:
    - 'ntp peer 10.1.1.1'
    - 'ntp peer 10.2.2.2'
...
```

2. Validation Block:

    assert is used to ensure each line exists in the live device config (ansible_net_config, retrieved earlier via ios_facts).
    If successful, it logs a success message per line.

3. Rescue Block:

    If any check fails, the rescue section is triggered.
    Optionally applies corrective configuration using ios_config.
    Logs failure details to a file for later review

4. Always Block:

    Used to continue execution regardless of the outcome.

Workflow Summary

```
policies.yml → contains expected config lines
     ↓
check_policies.yml → iterates through config lines
     ↓
assert → checks line presence
     ↓         ↘
 success     failure
     ↓           ↘
continue     rescue → optional fix + log to file
```