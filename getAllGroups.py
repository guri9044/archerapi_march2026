import requests
import csv
import json

url = "https://archer-irm.com/Archer/platformapi/core/system/group"

headers = {"Authorization": "Archer session-id=\"8F70794A378AE67E34FBDC268B05D912\""}

response = requests.get(url, headers=headers)

print(response.text)
data = response.json()
# Open a new CSV file to write to
with open('groups.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['id', 'name'])
    
    # Iterate over each item and extract the right fields
    for item in data:
        obj = item.get("RequestedObject", {})
        
        group_id = obj.get("Id")
        name = obj.get("Name")
        
        # Write the row
        writer.writerow([group_id, name])
print("CSV conversion complete!")