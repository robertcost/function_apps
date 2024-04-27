import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
import csv

def list_users_with_roles(exclude_domain):
    # Authenticate to Azure using DefaultAzureCredential
    credential = DefaultAzureCredential()
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    authorization_client = AuthorizationManagementClient(credential, subscription_id)

    # Retrieve all users with assigned roles
    users_with_roles = authorization_client.role_assignments.list()

    # Prepare CSV data
    data = [["User Principal Name", "Manager", "Usage Location", "User Enabled"]]

    for user in users_with_roles:
        user_principal_name = user.principal_id
        if user_principal_name.endswith(exclude_domain):
            continue

        # Fetch user details
        user_details = authorization_client.users.get(user_principal_name)

        # Manager, Usage Location, and User Enabled are not directly available
        # You might need to fetch this information from another Azure service or source
        # For demonstration purposes, I'll just leave these fields empty
        manager = ""
        usage_location = ""
        user_enabled = ""

        data.append([user_principal_name, manager, usage_location, user_enabled])

    return data

def save_to_csv(data):
    with open("users_with_roles.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def main():
    exclude_domain = "@example.com"  # Change this to your specific domain
    users_data = list_users_with_roles(exclude_domain)
    save_to_csv(users_data)

if __name__ == "__main__":
    main()
