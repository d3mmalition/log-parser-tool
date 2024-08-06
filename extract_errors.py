import re
import os
import sys

# ** CONFIGURATION VARIABLES **
LOG_DIR = '/path/to/your/log_files'  # Directory where log files are located
OUTPUT_DIR = os.path.join(LOG_DIR, 'output')  # Directory where output files should be saved

def extract_essential_error_info(lines, index):
    line = lines[index]
    match = re.search(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} (.*)', line)
    if match:
        log_entry = match.group(1)
        if 'WARN' in log_entry or 'ERROR' in log_entry or 'SEVERE' in log_entry:
            extended_entry = log_entry
            i = index + 1
            while i < len(lines) and re.search(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} ', lines[i]) is None:
                if re.search(r'^\s*Caused by:', lines[i]):
                    extended_entry += "\n" + lines[i].strip()
                i += 1
            return extended_entry
    return None

def extract_errors(log_file, output_file):
    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()
    except FileNotFoundError:
        print(f"Log file '{log_file}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Permission denied for '{log_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{log_file}': {str(e)}")
        sys.exit(1)

    essential_errors = []
    warn_found = False
    error_found = False
    severe_found = False

    for i in range(len(logs)):
        essential_info = extract_essential_error_info(logs, i)
        if essential_info:
            essential_errors.append(essential_info)
            if 'WARN' in essential_info:
                warn_found = True
            if 'ERROR' in essential_info:
                error_found = True
            if 'SEVERE' in essential_info:
                severe_found = True

    with open(output_file, 'w') as file:
        if not essential_errors:
            file.write("No WARN, ERROR, or SEVERE entries found.\n")
        else:
            for error in essential_errors:
                file.write(f"{error}\n\n")

        file.write("----\n\n")

        if not warn_found:
            file.write("There are no WARN entries.\n")
        if not error_found:
            file.write("There are no ERROR entries.\n")
        if not severe_found:
            file.write("There are no SEVERE errors.\n")

    print(f"Extracted errors from '{log_file}' to '{output_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_errors.py <log_file_name>")
        sys.exit(1)

    log_filename = sys.argv[1]

    log_file = os.path.join(LOG_DIR, log_filename)  # Input log file
    output_file = os.path.join(OUTPUT_DIR, f"{os.path.splitext(log_filename)[0]}_output.log")  # Output file

    # Check if the output directory exists
    if not os.path.isdir(OUTPUT_DIR):
        print(f"Output directory '{OUTPUT_DIR}' does not exist. Please create it or update the path.")
        sys.exit(1)

    extract_errors(log_file, output_file)
