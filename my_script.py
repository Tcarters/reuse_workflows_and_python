#!/bin/python3# 
# This py is used to verify the content fo a valid csv file in our IP groups automation

import sys, os
import csv
import ipaddress

# Check if valid ip address in CSV file
def check_valid_ip_and_mask(csv_file_name): 
    with open(csv_file_name, mode='r', newline='') as file: 
        reader = csv.reader(file) 
        # skip the header row 
        next(reader, None) 
        for row_number, row in enumerate(reader, start=2): 
            try: 
                # The second column contains the IP/mask 
                ip_with_mask = row[1] 
                # print ("row: ", ip_with_mask ) 
                # # This will create an IPv4Network or IPv6Network object if valid 
                # # strict=False allows the host bits to be non-zero for the network address 
                ipaddress.ip_network(ip_with_mask, strict=False) 
            except ValueError as e: 
                print(f"Error in row {row_number}: {e} - {ip_with_mask}") 
                return False 
            except IndexError as e: 
                print(f"Error in row {row_number}: The row does not have a second column.") 
                return False 
            except Exception as e: 
                print(f"An unexpected error occurred in row {row_number}: {e}") 
                return False 
    return True

# Check that 2 columns exist in CSV file
def two_columns_exist(header): 
    required_columns = ['Hostname', 'Ip_Address'] 
    if required_columns[0] not in header or required_columns[1] not in header: 
        print("Error: CSV file must contain 'Hostname' and 'Ip_Address' columns.") 
        return False 
    if header[0] != 'Hostname' or header[1] != 'Ip_Address':
        print("Error: First row must contain 'Hostname' and 'Ip_address'.") 
        return False 
    return True

# Check that no empty rows exist
def there_is_empty_value_in_column(file_path): 
    data = set() 
    with open(file_path, 'r') as file: 
        reader = csv.DictReader(file) 
        for row in reader:
            hostname = row['Hostname'] 
            ip_address = row['Ip_Address'] 
            
            if not hostname: #is None or hostname == " ": 
                print (f'Empty value for Hostname detected at row { row }') 
                return False # Return False if empty value found 
            
            if not ip_address: # is None or ip_address == " ": 
                print (f'Empty value Ip_Address detected at row { row }') 
                return False 
            
            if (hostname, ip_address) in data: 
                return False # Return False if duplicate found 
            
            data.add((hostname, ip_address)) 
    return True # Return True if no duplicates or empty values found

# Check that delimeter is ','

def is_good_delimiter(file_path): 
    try: 
        with open(file_path, 'r') as file: 
            dialect = csv.Sniffer().sniff(file.read(1024)) 
            # print ("this delimiter", dialect.delimiter) 
            
            if dialect.delimiter == ',': 
                return True 
            else: 
                print ('Not a valid CSV file...') 
                return False 
            
    except (csv.Error, FileNotFoundError): 
        print("Error: The detected delimiter is not a comma. Please use ',' as the delimiter.") 
        return False


# Check that no duplicates values exist in a row
def is_there_duplicates(file_path): 
    data = set() # create an empty data table 
    with open(file_path, 'r') as file: 
        reader = csv.reader(file) 
        row_number = 1 
        for row in reader: 
            # Convert the row to a tuple to check for duplicates
            row_data = tuple(row)
            if row_data in data: 
                print(f"Duplicate data found in row {row_number}.") 
                return False 
            data.add(row_data) 
            row_number += 1 
    return True


def remove_empty_lines(rows): 
    return [ row for row in rows if any( row.values() ) ]

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
    
    input_csv_file = sys.argv[1] # Take first argument as input file path
    
    if not is_csv_file(input_csv_file): 
        sys.exit(1) 
    
    try: 
        with open(input_csv_file, newline='') as csvfile: 
            reader = csv.DictReader(csvfile) 
            header = reader.fieldnames 
            rows = list(reader) 
            # print ("list rows: ", rows ) 
            
            if not two_columns_exist(header):
                print ("Checking, if Two columns exist in csv file... Failed ❌" )
                sys.exit(1)
            else:
                print ("Checking if Two columns exist in csv file... PASSED ✅" )
            
            if not there_is_empty_value_in_column(input_csv_file): 
                sys.exit(1) 
            
            if not is_good_delimiter(input_csv_file): 
                sys.exit(1) 
            
            # if not check_ip_format(rows): 
                # sys.exit(1) 
            
            if not is_there_duplicates(input_csv_file):
                print ("Checking, if there exists duplicates values in csv file... Failed ❌" )
                sys.exit(1)
            else:
                print ("Checking, if Two columns exist in csv file... PASSED ✅" )
            
            if not check_valid_ip_and_mask(input_csv_file): 
                sys.exit(1)
                
    except FileNotFoundError: 
        print(f"Error: File {input_csv_file} not found.") 
        sys.exit(1) 
    
    except csv.Error as e: 
        print(f"CSV error: {e}") 
        sys.exit(1) 
    
    except Exception as e: 
        print(f"An error occurred: {e}") 
        sys.exit(1)

# cleaned_rows = remove_empty_lines(rows) 
# # # print ("Cleaned rows are: ", cleaned_rows ) 
# # output_csv_file = "./fortimanager/scripts/results/clean_csvfile.csv" 
# # if os.path.exists (output_csv_file): # try: # with open(output_csv_file, 'w', newline='') as csvfile: # writer = csv.DictWriter(csvfile, fieldnames=header) 
# # writer.writeheader() # writer.writerows(cleaned_rows) # print(f"CSV file validation succeeded. Cleaned file saved as {output_csv_file}") 
# # except Exception as e: # print(f"An error occurred: {e}") # sys.exit(1)
if __name__ == "__main__": 
    main() 
    sys.exit(0) # Exit with zero to indicate success

# def is_good_delimiter(file_path):# with open(file_path, 'r', newline='') as csvfile:# # Sniff to deduce the dialect (if needed)# dialect = csv.Sniffer().sniff(csvfile.read(1024))# csvfile.seek(0) # Reset file pointer to the beginning# # Check if the detected delimiter is a comma# if dialect.delimiter != ',':# print("Error: The detected delimiter is not a comma. Please use ',' as the delimiter.")# return False# # Create a CSV reader object using the detected dialect# reader = csv.reader(csvfile, dialect)# # Iterate over each row and check for the correct number of fields# for row_number, row in enumerate(reader, start=1):# if len(row) <= 1:# print(f"Error: Row {row_number} does not seem to use ',' as a delimiter.")# return False# print("All rows use ',' as the delimiter.")# return True