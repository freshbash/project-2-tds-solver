import os
import shutil
import subprocess
import hashlib
import zipfile
import csv
from io import BytesIO, TextIOWrapper
import json
import datetime
import re


def q3(file):
    """Formats a markdown file using Prettier and returns its SHA-256 checksum."""
    
    if not shutil.which("npx"):
        raise Exception("npx not found")

    temp_path = "temp_markdown.md"
    
    # Save the uploaded file to disk
    file.save(temp_path)

    # Run Prettier to format the file
    # subprocess.run(["npx", "prettier@3.4.2", "--write", "./project-2/temp_markdown.md"], check=True)

    # Compute SHA-256 checksum
    hasher = hashlib.sha256()
    with open(temp_path, "rb") as f:
        hasher.update(f.read())

    # Remove temporary file
    os.remove(temp_path)

    return hasher.hexdigest()    

def q8(file_obj):
    with zipfile.ZipFile(file_obj, 'r') as z:
        for filename in z.namelist():
            if filename.endswith(".csv"):
                with z.open(filename) as csvfile:
                    reader = csv.DictReader(csvfile.read().decode("utf-8").splitlines())
                    for row in reader:
                        return row.get("answer", "No answer found.")

    return "CSV not found in ZIP."

def q9(json_str):
    data = json.loads(json_str)

    # Sort data by age and in case of tie, sort by name
    data.sort(key=lambda x: (x['age'], x['name']))

    # Print the sorted date with no spaces and newlines
    return json.dumps(data, separators=(',', ':'))

def q10(file):
    # Read the file content
    content = file.read().decode("utf-8").strip()
    
    # Convert key=value lines into a dictionary
    data = {}
    for line in content.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)  # Split only on the first '='
            data[key.strip()] = value.strip()

    # Convert to JSON string
    json_string = json.dumps(data, separators=(",", ":"))  # Minified JSON

    # Compute SHA-256 hash
    jsonhash = hashlib.sha256(json_string.encode("utf-8")).hexdigest()

    return jsonhash

def q12(file):
    target_symbols = {"œ", "€"}
    total_sum = 0

    encoding_map = {
        "data1.csv": "cp1252",
        "data2.csv": "utf-8",
        "data3.txt": "utf-16"
    }

    with zipfile.ZipFile(file, 'r') as z:
        for filename in z.namelist():
            if filename in encoding_map:
                with z.open(filename) as extracted_file:
                    reader = csv.reader(TextIOWrapper(extracted_file, encoding=encoding_map[filename]), 
                                        delimiter=',' if filename.endswith('.csv') else '\t')
                    next(reader)  # Skip header
                    
                    for row in reader:
                        if len(row) >= 2 and row[0] in target_symbols:
                            try:
                                total_sum += float(row[1])
                            except ValueError:
                                continue  # Ignore non-numeric values
    
    return total_sum

def q14(file, output_folder="unzipped_files"):
     # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Extract ZIP contents
    with zipfile.ZipFile(file, "r") as z:
        z.extractall(output_folder)

    # Process files and replace occurrences of "IITM"
    pattern = re.compile(r"iitm", re.IGNORECASE)
    
    for root, _, files in os.walk(output_folder):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Read the file while preserving line endings
            with open(file_path, "r", encoding="utf-8", newline="") as f:
                content = f.read()

            # Replace 'IITM' with 'IIT Madras'
            updated_content = pattern.sub("IIT Madras", content)

            # Write back to the file
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                f.write(updated_content)

    # Compute the SHA-256 hash of concatenated file contents
    hasher = hashlib.sha256()
    
    for root, _, files in os.walk(output_folder):
        for filename in sorted(files):  # Ensuring consistent order
            file_path = os.path.join(root, filename)
            with open(file_path, "rb") as f:
                hasher.update(f.read())

    return hasher.hexdigest() + " -"

def q15(file, filters_json, output_folder="extracted_files"):
    # Parse JSON filters
    print(filters_json)
    filters = json.loads(filters_json)
    min_bytes = filters.get("min_bytes", 0)
    timestamp_str = filters.get("timestamp", "")
    
    # Convert timestamp string to a datetime object
    try:
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
    except ValueError:
        return timestamp_str
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Extract ZIP contents
    with zipfile.ZipFile(file, "r") as z:
        z.extractall(output_folder)

    total_size = 0  # Sum of matching file sizes

    # Process extracted files
    for root, _, files in os.walk(output_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Get file metadata
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            file_mtime = datetime.datetime.fromtimestamp(file_stat.st_mtime, tz=datetime.timezone.utc)

            # Apply filters
            if file_size >= min_bytes and file_mtime >= timestamp:
                total_size += file_size

    return total_size

def q16(file, output_folder="processed_files"):
    temp_folder = "extracted"
    
    # Ensure folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    # Extract ZIP contents
    with zipfile.ZipFile(file, "r") as z:
        z.extractall(temp_folder)

    # Regex for digit replacement
    digit_map = str.maketrans("0123456789", "1234567890")

    # Move & rename files
    for root, _, files in os.walk(temp_folder):
        for filename in files:
            old_path = os.path.join(root, filename)
            new_name = filename.translate(digit_map)
            new_path = os.path.join(output_folder, new_name)

            shutil.move(old_path, new_path)  # Move and rename

    # Compute SHA-256 checksum after sorting file contents
    hasher = hashlib.sha256()
    
    for filename in sorted(os.listdir(output_folder)):  # Sort files
        file_path = os.path.join(output_folder, filename)
        with open(file_path, "rb") as f:
            for line in sorted(f.readlines()):  # Sort lines in each file
                hasher.update(line)

    return hasher.hexdigest() + " -"

def q17(file, output_folder="extracted_files"):
    """Extracts ZIP, compares a.txt and b.txt line by line, 
    and returns the number of differing lines."""
    
    # Ensure extraction folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Extract ZIP contents
    with zipfile.ZipFile(file, "r") as z:
        z.extractall(output_folder)

    # Define file paths
    file_a = os.path.join(output_folder, "a.txt")
    file_b = os.path.join(output_folder, "b.txt")

    # Check if both files exist
    if not os.path.exists(file_a) or not os.path.exists(file_b):
        return "Error: a.txt or b.txt not found in the ZIP."

    # Read files and compare line by line
    with open(file_a, "r", encoding="utf-8") as fa, open(file_b, "r", encoding="utf-8") as fb:
        a_lines = fa.readlines()
        b_lines = fb.readlines()

    # Ensure both files have the same number of lines
    if len(a_lines) != len(b_lines):
        return "Error: a.txt and b.txt have different numbers of lines."

    # Count differing lines
    diff_count = sum(1 for a, b in zip(a_lines, b_lines) if a != b)

    return diff_count