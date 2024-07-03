import csv
import json
import sys

def read_csv(file_path):
    """Reads a CSV file and returns its content as a list of dictionaries."""
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        return [row for row in csv_reader]

def check_items_in_csv(items, csv_content):
    """Checks if each item is in the CSV content."""
    for item in items:
        if item in csv_content:
            print(f"Item exists in CSV: {item}")
        else:
            print(f"Item does not exist in CSV: {item}")

def main():
    # if len(sys.argv) != 3:
    #     print("Usage: python check_items.py <path_to_csv_file> <items>")
    #     sys.exit(1)
    lst = []
    
    file_path = 'ip.csv' #sys.argv[1]
    # items_json = sys.argv[1]
       # Parse the items
    items = {"Hostname":"dbserver01","Ip_Address":"10.10.10.2/24"}    #json.loads(items_json)
    # print (items["Hostname"])
    lst.append (items)
    print (lst)
    
    # Read the CSV content
    # csv_content = read_csv(file_path)
    # for i in csv_content:
    #     print (i['Hostname'])
    #     for data in items:
    #         print ("data in api req: ", data )
    #         if data["Hostname"] == i['Hostname'] and data["Ip_Address"] == i["Ip_Address"]:
    #             print ('Found it !', i)
    #         else:
    #             print ('Not found')
        
    # print (csv_content)
    
 
    # Check if items exist in CSV content
    # check_items_in_csv(items, csv_content)

if __name__ == "__main__":
    main()
