# step3_remove_outliers.py

import csv
from datetime import datetime
from collections import defaultdict
import statistics

input_file = 'filtered_year.csv'
output_file = 'filtered_year_no_outliers.csv'

data_by_group = defaultdict(list)

# Group data
with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dt = datetime.fromisoformat(row['dateTime'].replace('Z', '+00:00'))
        kWh = float(row['kWh'])
        weekday = dt.weekday()
        hour = dt.hour
        group = (weekday, 'night' if 0 <= hour < 5 else 'day')
        data_by_group[group].append((dt, kWh, row))

# Filter out outliers
with open(output_file, 'w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=['epochTimestamp', 'kWh', 'dateTime'])
    writer.writeheader()

    for group, entries in data_by_group.items():
        kWh_values = [e[1] for e in entries]
        if len(kWh_values) < 10:
            continue
        mean = statistics.mean(kWh_values)
        stdev = statistics.stdev(kWh_values)

        for dt, kWh, row in entries:
            if abs(kWh - mean) <= 2 * stdev:
                writer.writerow(row)
