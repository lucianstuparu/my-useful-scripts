import csv
import requests
import os
import sys
from datetime import datetime

def assign_courses_to_groups(instance_url, token, input_courses_file, input_groups_file, output_dir):
    # Construct the output file name
    current_time = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
    output_file = os.path.join(output_dir, f"course_assignments_{current_time}.csv")

    # Base URL for assigning courses to groups
    api_url_template = f"{instance_url}/api/v1/Groups/{{groupId}}/Courses"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        # Open input files and output file
        with open(input_courses_file, mode="r", encoding="utf-8") as courses_file, \
             open(input_groups_file, mode="r", encoding="utf-8") as groups_file, \
             open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

            courses_reader = csv.DictReader(courses_file)
            groups_reader = csv.DictReader(groups_file)
            writer = csv.writer(outfile)

            # Write the header for the output file
            writer.writerow(["Group ID", "Group Name", "Courses Assigned", "Result"])

            # Create a list of groups for quick matching
            groups = [
                {"Group ID": row["Group ID"], "Group Name": row["Group Name"],
                 "Grade": row["Grade"], "Language": row["Language"]}
                for row in groups_reader
            ]

            # Organize courses by grade and language
            courses = [
                {"Course ID": row["Course ID"], "Grade": row["Grade"], "Language": row["Language"]}
                for row in courses_reader
            ]

            # Match courses to groups and prepare API payloads
            for group in groups:
                group_id = group["Group ID"]
                group_name = group["Group Name"]
                grade = group["Grade"]
                language = group["Language"]

                # Find courses matching the group's grade and language
                matching_courses = [
                    {"CourseId": int(course["Course ID"]), "Priority": "Default"}
                    for course in courses
                    if course["Grade"] == grade and course["Language"] == language
                ]

                # Skip if no matching courses
                if not matching_courses:
                    continue

                # Construct the API URL for the group
                api_url = api_url_template.format(groupId=group_id)

                # Make the POST request with all matching courses
                response = requests.post(api_url, json=matching_courses, headers=headers)

                # Determine the result of the API call
                if response.status_code in [200, 204]:
                    result = "Success"
                else:
                    result = f"Fail ({response.status_code}: {response.text})"
                    # Print and stop the script on failure
                    print(f"API call failed for Group ID {group_id}: {result}")
                    sys.exit(1)

                # Write the result to the output file
                writer.writerow([group_id, group_name, len(matching_courses), result])

                # Print the result in CLI
                print(f"Group ID: {group_id}, Group Name: {group_name}, Courses Assigned: {len(matching_courses)}, Result: {result}")

            print(f"Course assignments saved successfully to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <INSTANCE_URL> <INPUT_COURSES_FILE> <INPUT_GROUPS_FILE> <OUTPUT_DIRECTORY> <TOKEN>")
    else:
        instance_url = sys.argv[1]
        input_courses_file = sys.argv[2]
        input_groups_file = sys.argv[3]
        output_dir = sys.argv[4]
        token = sys.argv[5]
        assign_courses_to_groups(instance_url, token, input_courses_file, input_groups_file, output_dir)
