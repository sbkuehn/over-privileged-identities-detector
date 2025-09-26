# Over-Privileged Identities Detector

This repository provides scripts in **PowerShell** and **Python** that use Microsoft Graph to identify over-privileged identities in Entra ID.

## Features
- Detects accounts and service principals assigned to high-risk roles
- Works with both PowerShell and Python
- Exports results to console and CSV (Python)
- Demonstrates how to use Microsoft Graph for identity governance

## Prerequisites
- Entra ID Premium P1 or P2
- Microsoft Graph PowerShell SDK or Python MSAL library
- Microsoft 365 tenant with administrative access
- API permissions:
  - RoleManagement.Read.All
  - Directory.Read.All

## PowerShell Usage
1. Install Microsoft Graph SDK:
   ```powershell
   Install-Module -Name Microsoft.Graph -Scope CurrentUser
   ```
2. Run the script:
   ```powershell
   ./powershell/Get-OverPrivilegedIdentities.ps1
   ```

## Python Usage
1. Install dependencies:
   ```bash
   pip install msal requests
   ```
2. Edit the script and add your Tenant ID, Client ID, and Client Secret.
3. Run the script:
   ```bash
   python python/get_over_privileged_identities.py
   ```

The Python script prints results to the console and exports them to a CSV file with a timestamp in the name.

## Next Steps
- Review privileged role assignments
- Remove unnecessary privileges
- Implement Entra ID Privileged Identity Management (PIM)
- Automate reporting with scheduled tasks, CI/CD, or cron jobs

## License
MIT License
