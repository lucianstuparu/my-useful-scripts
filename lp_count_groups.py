import requests
import sys

def get_number_of_groups(instance_url, access_token):
    # Construct the API URL
    api_url = f"{instance_url.rstrip('/')}/api/v1/Groups"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        # Make the GET request
        response = requests.get(api_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            number_of_groups = len(data)  # Get the number of groups
            print(f"Number of groups: {number_of_groups}")
        else:
            print(f"Failed to fetch groups. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get arguments from the command line
    if len(sys.argv) != 3:
        print("Usage: python get_groups.py <INSTANCE_URL> <ACCESS_TOKEN>")
    else:
        instance_url = sys.argv[1]
        access_token = sys.argv[2]
        get_number_of_groups(instance_url, access_token)
