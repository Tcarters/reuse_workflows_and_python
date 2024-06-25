#!/bin/python3

import sys
import csv
import ipaddress
import os

# Check if valid IP address in CSV file
def is_valid_ip(ip_str):
    try:
        ipaddress.ip_network(ip_str, strict=False)
        return True
    except ValueError:
        return False

# Check that 2 columns exist in CSV file
def check_columns(header):
    required_columns = ['Hostname', 'Ip_Address']
    if required_columns[0] not in header or required_columns[1] not in header:
        print("Error: CSV file must contain 'Hostname' and 'Ip_Address' columns.")
        return False
    if header[0] != 'Hostname' or header[1] != 'Ip_Address':
        print("Error: First row must contain 'Hostname' and 'Ip_address'.")
        return False
    return True

# Check that no empty rows exist
def check_empty_values(rows):
    for row in rows:
        if not row['Hostname'] or not row['Ip_Address']:
            print(f"Error: CSV file contains empty values in row {row}.")
            return False
    return True

# Check that delimiter is ','
def check_delimiter(file_path):
    with open(file_path, 'r', newline='') as csvfile:
        # Sniff to deduce the dialect (if needed)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)  # Reset file pointer to the beginning

        # Check if the detected delimiter is a comma
        if dialect.delimiter != ',':
            print("Error: The detected delimiter is not a comma. Please use ',' as the delimiter.")
            return False

        # Create a CSV reader object using the detected dialect
        reader = csv.reader(csvfile, dialect)

        # Iterate over each row and check for the correct number of fields
        for row_number, row in enumerate(reader, start=1):
            if len(row) <= 1:
                print(f"Error: Row {row_number} does not seem to use ',' as a delimiter.")
                return False
        print("All rows use ',' as the delimiter.")
        return True

# Check for valid IP address
def check_ip_format(rows):
    for row in rows:
        if not is_valid_ip(row['Ip_Address']):
            print(f"Error: IP address '{row['Ip_Address']}' is not valid.")
            return False
    return True

# Check that no duplicate values exist in a row
def check_duplicates(rows):
    hostnames = set()
    ip_addresses = set()
    for row in rows:
        if row['Hostname'] in hostnames:
            print(f"Error: Duplicate hostname '{row['Hostname']}' found.")
            return False
        if row['Ip_Address'] in ip_addresses:
            print(f"Error: Duplicate IP address '{row['Ip_Address']}' found.")
            return False
        hostnames.add(row['Hostname'])
        ip_addresses.add(row['Ip_Address'])
    return True

# Remove empty lines from rows
def remove_empty_lines(rows):
    return [row for row in rows if any(row.values())]

# Check if the file is a valid CSV file
def is_csv_file(file_path):
    if not file_path.lower().endswith('.csv'):
        print("Error: The file does not have a .csv extension.")
        return False

    try:
        with open(file_path, 'r') as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            if dialect.delimiter in [',', ';']:
                return True
            else:
                print("Error: The file does not contain ',' or ';' as delimiters.")
                return False
    except (csv.Error, FileNotFoundError):
        print("Error: The file is not a valid CSV file.")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python filecsv.py <input_csv_file>")
        sys.exit(1)

    input_csv_file = sys.argv[1]

    if not is_csv_file(input_csv_file):
        sys.exit(1)

    try:
        with open(input_csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            rows = list(reader)

            if not check_columns(header):
                sys.exit(1)

            if not check_empty_values(rows):
                sys.exit(1)

            if not check_delimiter(input_csv_file):
                sys.exit(1)

            if not check_ip_format(rows):
                sys.exit(1)

            if not check_duplicates(rows):
                sys.exit(1)

            cleaned_rows = remove_empty_lines(rows)
            output_csv_file = "validated_" + input_csv_file
            
            with open(output_csv_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                writer.writerows(cleaned_rows)

            print(f"CSV file validation succeeded. Cleaned file saved as {output_csv_file}")
    except FileNotFoundError:
        print(f"Error: File {input_csv_file} not found.")
        sys.exit(1)
    except csv.Error as e:
        print(f"CSV error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)  # Exit with zero to indicate success
