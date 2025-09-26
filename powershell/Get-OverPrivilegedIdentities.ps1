<#
.SYNOPSIS
    Identify over-privileged identities in Entra ID using Microsoft Graph.

.DESCRIPTION
    Connects to Microsoft Graph and lists all users and service principals
    assigned to high-privilege roles such as Global Administrator,
    Privileged Role Administrator, and Application Administrator.

.AUTHOR
    Shannon B. Eldridge-Kuehn - 2025

.REQUIREMENTS
    - Entra ID Premium P1 or P2
    - Microsoft Graph PowerShell SDK
    - RoleManagement.Read.All and Directory.Read.All permissions

.VERSION
    1.0

.EXAMPLE
    PS> ./Get-OverPrivilegedIdentities.ps1
#>

# Import Microsoft Graph module
Import-Module Microsoft.Graph

# Connect to Microsoft Graph with required scopes
Connect-MgGraph -Scopes "RoleManagement.Read.All", "Directory.Read.All"

function Get-PrivilegedIdentities {
    Write-Host "Fetching privileged roles..." -ForegroundColor Yellow

    # Get all directory roles
    $roles = Get-MgDirectoryRole

    # Define high-privilege roles
    $highPrivilegeRoles = @(
        "Global Administrator",
        "Privileged Role Administrator",
        "Application Administrator"
    )

    foreach ($role in $roles) {
        if ($highPrivilegeRoles -contains $role.DisplayName) {
            Write-Host "`nRole: $($role.DisplayName)" -ForegroundColor Cyan
            $members = Get-MgDirectoryRoleMember -DirectoryRoleId $role.Id

            foreach ($member in $members) {
                $memberDetails = Get-MgUser -UserId $member.Id -ErrorAction SilentlyContinue
                if ($memberDetails) {
                    Write-Host "User: $($memberDetails.DisplayName) ($($memberDetails.UserPrincipalName))" -ForegroundColor Green
                } else {
                    Write-Host "Service Principal: $($member.Id)" -ForegroundColor Magenta
                }
            }
        }
    }
}

# Execute the function
Get-PrivilegedIdentities
