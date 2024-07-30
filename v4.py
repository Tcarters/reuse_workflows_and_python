#!/bin/python3
# This py is used to verify the content of a valid CSV file in our IP groups automation

import sys
import csv
import ipaddress

# Check if valid IP address in CSV file
def check_valid_ip_and_mask(csv_file_name):
    with open(csv_file_name, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=2):
            try:
                # The 'Ip_Address' column contains the IP/mask
                ip_with_mask = row['Ip_Address']
                ipaddress.ip_network(ip_with_mask, strict=False)
            except ValueError as e:
                print(f"Error in row {row_number}: {e} - {ip_with_mask}")
                return False
            except KeyError:
                print(f"Error in row {row_number}: 'Ip_Address' column is missing.")
                return False
            except Exception as e:
                print(f"An unexpected error occurred in row {row_number}: {e}")
                return False
    return True

# Check that exactly 2 columns exist in CSV file
def two_columns_exist(header):
    required_columns = ['Hostname', 'Ip_Address']
    if len(header) != 2:
        print("Error: CSV file must contain exactly two columns.")
        return False
    if required_columns[0] not in header or required_columns[1] not in header:
        print("Error: CSV file must contain 'Hostname' and 'Ip_Address' columns.")
        return False
    if header[0] != 'Hostname' or header[1] != 'Ip_Address':
        print("Error: First row must contain 'Hostname' and 'Ip_Address'.")
        return False
    return True

# Check that no empty rows exist
def there_is_empty_value_in_column(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=2):
            hostname = row.get('Hostname')
            ip_address = row.get('Ip_Address')
            
            if not hostname:
                print(f'Empty value for Hostname detected at row {row_number}')
                return False
            
            if not ip_address:
                print(f'Empty value for Ip_Address detected at row {row_number}')
                return False
    return True

# Check that delimiter is ','
def is_good_delimiter(file_path):
    try:
        with open(file_path, 'r') as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)  # Reset the file pointer to the beginning of the file
            if dialect.delimiter == ',':
                return True
            else:
                print('Not a valid CSV file...')
                return False
    except (csv.Error, FileNotFoundError):
        print("Error: The detected delimiter is not a comma. Please use ',' as the delimiter.")
        return False

# Check that no duplicate rows exist in the CSV file
def is_there_duplicates(file_path):
    data = set()  # Create an empty data table
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        row_number = 2
        for row in reader:
            row_data = tuple(row)
            if row_data in data:
                print(f"Duplicate data found in row {row_number}.")
                return False
            data.add(row_data)
            row_number += 1
    return True

def remove_empty_lines(rows):
    return [row for row in rows if any(row.values())]

def is_csv_file(file_path):
    if not file_path.lower().endswith('.csv'):
        print("Error: The file does not have a .csv extension.")
        return False
    return True

## Main section
def main():
    if len(sys.argv) != 2:
        print("Usage: python filecsv.py <input_csv_file>")
        sys.exit(1)
    
    input_csv_file = sys.argv[1]  # Take first argument as input file path
    
    if not is_csv_file(input_csv_file):
        sys.exit(1)
    
    try:
        with open(input_csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            rows = list(reader)
            
            if not two_columns_exist(header):
                print("Checking if two columns exist in CSV file... Failed ❌")
                sys.exit(1)
            else:
                print("Checking if two columns exist in CSV file... PASSED ✅")
            
            if not there_is_empty_value_in_column(input_csv_file):
                print("Checking for empty values in columns... Failed ❌")
                sys.exit(1)
            else:
                print("Checking for empty values in columns... PASSED ✅")
            
            if not is_good_delimiter(input_csv_file):
                print("Checking if the delimiter is correct... Failed ❌")
                sys.exit(1)
            else:
                print("Checking if the delimiter is correct... PASSED ✅")
            
            if not is_there_duplicates(input_csv_file):
                print("Checking if there are duplicate values in the CSV file... Failed ❌")
                sys.exit(1)
            else:
                print("Checking if there are duplicate values in the CSV file... PASSED ✅")
            
            if not check_valid_ip_and_mask(input_csv_file):
                print("Checking if IP addresses are valid... Failed ❌")
                sys.exit(1)
            else:
                print("Checking if IP addresses are valid... PASSED ✅")
                
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
