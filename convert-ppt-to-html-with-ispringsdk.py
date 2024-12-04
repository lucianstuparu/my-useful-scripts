import os
import sys
import subprocess
import time

# Check if the executable path and input file/folder are passed as command-line arguments
if len(sys.argv) < 3:
    print("Usage: python convert-ppt-to-html.py <ispring_exe_path> <input_folder_or_file>")
    sys.exit(1)

# Get the iSpring executable path and input path from the command-line arguments
ispring_exe = sys.argv[1]
input_path = sys.argv[2]

# Verify if the provided iSpring executable exists
if not os.path.isfile(ispring_exe):
    print(f"Error: The iSpring executable '{ispring_exe}' does not exist.")
    sys.exit(1)

# Verify if the provided input path exists
if not os.path.exists(input_path):
    print(f"Error: The path '{input_path}' does not exist.")
    sys.exit(1)

# Prepare to track success and errors
success_count = 0
error_files = []

# Define a function to process a single file
def process_pptx_file(pptx_path, file_index, total_files):
    global success_count

    # Prepare paths for the ZIP and HTML files
    base_dir = os.path.dirname(pptx_path)
    base_name = os.path.splitext(os.path.basename(pptx_path))[0]
    zip_output_path = os.path.join(base_dir, f"{base_name}.zip")
    html_output_path = os.path.join(base_dir, "index.html")  # Always name the main HTML file index.html

    # Get original file size
    original_file_size = os.path.getsize(pptx_path) / (1024 * 1024)  # Size in MB

    # Print the starting delimiter and file info
    print(f"\n---{file_index}/{total_files}--------------------------")
    print(f"Processing file: {pptx_path} (Size: {original_file_size:.2f} MB)...")

    # Start the timer
    start_time = time.time()

    # Build the command
    command = [
        ispring_exe,
        "h",
        "-f", "solid",
        "-z", "-zof", zip_output_path,
        "-fw",
        "-piq", "0",
        "-giq", "0",
        "--advanced-smart-art-processing",
        "-om", "on",
        "--skin", "none",
        "-v", pptx_path,
        html_output_path
    ]

    try:
        # Execute the command with real-time output
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Stop the timer and calculate processing time
        processing_time = time.time() - start_time

        # Get resulting ZIP file size
        if os.path.exists(zip_output_path):
            resulting_file_size = os.path.getsize(zip_output_path) / (1024 * 1024)  # Size in MB
        else:
            resulting_file_size = 0

        print(f"Successfully converted: {pptx_path} to {zip_output_path}")
        print(f" - Processing time: {processing_time:.2f} seconds")
        print(f" - Resulting ZIP size: {resulting_file_size:.2f} MB")
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"Error converting {pptx_path}:")
        print(f" - Command: {' '.join(command)}")
        print(f" - Exit Code: {e.returncode}")
        print(f" - Stdout: {e.stdout.decode().strip() if e.stdout else 'None'}")
        print(f" - Stderr: {e.stderr.decode().strip() if e.stderr else 'None'}")
        error_files.append(pptx_path)
    except Exception as e:
        print(f"An unexpected error occurred while processing {pptx_path}: {e}")
        error_files.append(pptx_path)
    finally:
        # Add a clear ending delimiter after processing each file
        print("-----------------------------")

# If the input is a directory, process all .pptx files in the directory
if os.path.isdir(input_path):
    pptx_files = [os.path.join(input_path, file_name) for file_name in os.listdir(input_path) if file_name.endswith(".pptx")]
    total_files = len(pptx_files)
    for index, pptx_file in enumerate(pptx_files, start=1):
        process_pptx_file(pptx_file, index, total_files)
# If the input is a single file, process only that file
elif os.path.isfile(input_path) and input_path.endswith(".pptx"):
    process_pptx_file(input_path, 1, 1)
else:
    print(f"Error: Unsupported file type or invalid input '{input_path}'. Please provide a .pptx file or directory.")
    sys.exit(1)

# Print final summary
print("\n--- Conversion Summary ---")
total_files = len(pptx_files) if os.path.isdir(input_path) else 1
print(f"Total files processed: {total_files}")
print(f"Successfully converted: {success_count}")
if error_files:
    print(f"Files with errors ({len(error_files)}):")
    for error_file in error_files:
        print(f" - {error_file}")
else:
    print("No errors encountered.")
