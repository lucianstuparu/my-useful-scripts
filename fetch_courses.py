import sys
import os
import requests
import json
from datetime import datetime

def fetch_and_process_courses(instance_url, bearer_token, output_directory):
    api_endpoint = f"{instance_url}/api/v3/admin/categoriesAndCourses?publishedCourses=true"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }

    try:
        # Fetch the data from API
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Process the data
        categories = [
            {
                "Id": offer["Id"],
                "Names": offer["Names"],
                "Logo": offer["Logo"]
            }
            for offer in data.get("Offers", [])
        ]

        courses = [
            {
                "CourseID": course["Id"],
                "URL": f"{instance_url}/#/course/{course['Id']}/item/null",
                "CategoryID": course["ParentId"],
                "ContentLanguage": course["ContentLanguage"],
                "ParentCourseId": course["ParentCourseId"],
                "Name": course["Name"].replace("\n", " "),
                "Description": course["Description"].replace("\n", "<br>"),
                "Logo": course["Logo"],
                "IsCertificate": course["IsCertificate"],
                "NumPublishedLessons": course["NumPublishedLessons"],
                "NumPublishedKCs": course["NumPublishedKCs"]
            }
            for course in data.get("CourseItems", [])
        ]

        processed_data = {
            "Categories": categories,
            "Courses": courses
        }

        # Prepare output file name
        domain_name = instance_url.split("//")[1].split(".")[0]  # Extract domain prefix (e.g., 'yhub')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Current date and time
        file_name = f"{domain_name}_courses_{timestamp}.json"
        file_path = os.path.join(output_directory, file_name)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(processed_data, file, indent=4, ensure_ascii=False)

        # Output results
        print(f"{len(categories)} categories and {len(courses)} courses retrieved.")
        print(f"Data saved to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python fetch_courses.py <instance_url> <bearer_token> <output_directory>")
        sys.exit(1)

    instance_url = sys.argv[1]
    bearer_token = sys.argv[2]
    output_directory = sys.argv[3]

    # Validate output directory
    if not os.path.isdir(output_directory):
        print(f"Error: {output_directory} is not a valid directory.")
        sys.exit(1)

    fetch_and_process_courses(instance_url, bearer_token, output_directory)
