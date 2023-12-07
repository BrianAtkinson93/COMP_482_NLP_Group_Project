import csv
import json

# Reading data from scrapes.csv and converting it to json format

def csv_to_json(csv_file, output_file):
    json_data = []

    with open(csv_file, 'r', encoding="utf8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            question = row['Question']
            answer = row['Answer']
            json_data.append({"input": question, "output": answer})

    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

# Replace 'scrapes.csv' with the path to your CSV file

csv_file_path = 'scrapes.csv'
output_json_path = 'training_data.json' 

csv_to_json(csv_file_path, output_json_path)
print(f"JSON data written to {output_json_path}")
