import csv
import json

with open('/Users/user1/Documents/Product Management/Productboard/20250502_roadmap.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    data = list(csv.DictReader(csvfile))

with open('./roadmap/20250502_roadmap.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)