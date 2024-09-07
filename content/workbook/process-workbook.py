import os
import json
import re


def convert_json(j):
    for k in j:
        print(j[k])


def process_workbook(file_path):
    json_found = ""
    inside_json = False

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Strip leading and trailing whitespace

                if not line.startswith('{'):
                    if inside_json:
                        json_found += line  # Add line to the buffer
                    else:
                        # this is not JSON, but markdown, just output
                        print(line)

                # Start of a JSON object
                else:
                    inside_json = True
                    json_found = line  # Start buffering JSON content

                # End of JSON
                if line.endswith('}'):
                    inside_json = False
                    # Try to parse the buffered content as JSON
                    try:
                        json_part = json.loads(json_found)
                        print(convert_json(json_part))
                    except json.JSONDecodeError:
                        # Skip the buffer if it's not valid JSON
                        pass
                    finally:
                        json_found = ""  # Reset buffer after attempting to parse

    except FileNotFoundError:
        print(f"File {file_path} not found.")


current_directory = os.path.dirname(os.path.abspath(__file__))

file_path = "/lesson0/les0a.md"
json_data = process_workbook(current_directory+file_path)
print(json_data)
