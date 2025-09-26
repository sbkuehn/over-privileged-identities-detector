"""
Identify over-privileged identities in Entra ID using Microsoft Graph.

This script uses MSAL to authenticate and the Microsoft Graph REST API
to list users and service principals assigned to high-privilege roles.

It prints results to the console and exports them to a CSV file for reporting.

Author: Shannon B. Eldridge-Kuehn - 2025
Version: 1.0

Requirements:
    pip install msal requests

API Permissions Required:
    - RoleManagement.Read.All
    - Directory.Read.All
"""

import requests
import msal
import csv
from datetime import datetime

TENANT_ID = "<YOUR_TENANT_ID>"
CLIENT_ID = "<YOUR_CLIENT_ID>"
CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

HIGH_PRIVILEGE_ROLES = [
    "Global Administrator",
    "Privileged Role Administrator",
    "Application Administrator"
]

def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_silent(SCOPE, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Failed to obtain access token.")

def get_directory_roles(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{GRAPH_API_ENDPOINT}/directoryRoles"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])

def get_role_members(access_token, role_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{GRAPH_API_ENDPOINT}/directoryRoles/{role_id}/members"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])

def main():
    print("Fetching privileged identities from Entra ID...")
    token = get_access_token()
    roles = get_directory_roles(token)
    results = []

    for role in roles:
        if role.get("displayName") in HIGH_PRIVILEGE_ROLES:
            print(f"\nRole: {role['displayName']}")
            members = get_role_members(token, role["id"])
            if not members:
                print("  No members found.")
            for member in members:
                member_type = member.get("@odata.type", "")
                if "user" in member_type.lower():
                    entry = {
                        "Role": role["displayName"],
                        "Type": "User",
                        "Name": member.get("displayName"),
                        "Identifier": member.get("userPrincipalName")
                    }
                elif "serviceprincipal" in member_type.lower():
                    entry = {
                        "Role": role["displayName"],
                        "Type": "Service Principal",
                        "Name": member.get("displayName"),
                        "Identifier": member.get("appId")
                    }
                else:
                    entry = {
                        "Role": role["displayName"],
                        "Type": "Other",
                        "Name": str(member),
                        "Identifier": ""
                    }
                results.append(entry)
                print(f"  {entry['Type']}: {entry['Name']} ({entry['Identifier']})")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"over_privileged_identities_{timestamp}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Role", "Type", "Name", "Identifier"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults exported to {filename}")

if __name__ == "__main__":
    main()
