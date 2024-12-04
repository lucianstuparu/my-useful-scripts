import csv
import re
import os
import sys
from datetime import datetime

def extract_groups_by_naming_convention(input_file, output_dir):
    # Define valid grade and language values
    valid_grades = ["KG1", "KG2", "KG3", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9",
                    "G10", "G11H", "G11SC", "G12SG", "G12LH", "G12SV", "G12SE"]
    valid_languages = ["EN", "FR", "AR"]

    # Construct the output file name
    current_time = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
    output_file = os.path.join(output_dir, f"filtered_groups_{current_time}.csv")

    # Regex pattern to match naming convention
    naming_pattern = re.compile(r"^(\d+)-(" + "|".join(valid_grades) + ")-(" + "|".join(valid_languages) + r")-.*$")

    try:
        with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)

            # Write the header for the output file
            writer.writerow(["Group ID", "Group Name", "Grade", "Language"])

            # Process each group in the input file
            for row in reader:
                group_name = row["Group Name"]
                match = naming_pattern.match(group_name)
                if match:
                    school_id, grade, language = match.groups()
                    writer.writerow([row["Group ID"], group_name, grade, language])

            print(f"Filtered groups saved successfully to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <INPUT_FILE> <OUTPUT_DIRECTORY>")
    else:
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
        extract_groups_by_naming_convention(input_file, output_dir)
