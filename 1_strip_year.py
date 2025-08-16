import csv
from datetime import datetime

input_file = 'hildebrand_output.csv'
output_file = 'filtered_year.csv'

filteryear = int(input("Enter a year to filter for:"))
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        try:
            dt = datetime.fromisoformat(row['dateTime'].replace('Z', '+00:00'))
            if dt.year == filteryear:
                writer.writerow(row)
        except Exception as e:
            continue  # skip rows with bad data
