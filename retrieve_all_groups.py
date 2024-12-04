import requests
import csv
import sys
import os
from datetime import datetime

def retrieve_groups(instance_url, output_dir, token):
    # Extract the first subdomain for the filename
    subdomain = instance_url.split("//")[-1].split(".")[0]
    # Get current date and time
    current_time = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
    # Construct the output file name
    output_file = os.path.join(output_dir, f"{subdomain}_all_groups_{current_time}.csv")

    url = f"{instance_url}/api/v1/Groups"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            groups = response.json()  # Parse the JSON response

            # Write data to the CSV file
            with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Write the header
                writer.writerow(["Group ID", "Group Name"])

                # Write group data
                for group in groups:
                    writer.writerow([group.get("GroupId"), group.get("GroupName")])

            print(f"Groups saved successfully to {output_file}")
        else:
            print(f"Failed to fetch groups. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <INSTANCE_URL> <OUTPUT_DIRECTORY> <TOKEN>")
    else:
        instance_url = sys.argv[1]
        output_dir = sys.argv[2]
        token = sys.argv[3]
        retrieve_groups(instance_url, output_dir, token)
