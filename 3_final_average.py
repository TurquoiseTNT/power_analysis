# step4_final_average_to_csv.py

import csv
from datetime import datetime
from collections import defaultdict

input_file = 'filtered_year_no_outliers.csv'
output_file = 'final_weekday_averages.csv'

# Accumulate kWh by weekday and time period
usage = defaultdict(lambda: {'night': [], 'day': []})

with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dt = datetime.fromisoformat(row['dateTime'].replace('Z', '+00:00'))
        kWh = float(row['kWh'])
        weekday = dt.weekday()  # 0 = Monday
        hour = dt.hour

        if 0 <= hour < 5:
            usage[weekday]['night'].append(kWh)
        else:
            usage[weekday]['day'].append(kWh)

# Prepare output rows
weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output_rows = []

for wd in range(7):
    day_kWh = usage[wd]['day']
    night_kWh = usage[wd]['night']
    day_avg = sum(day_kWh) / len(day_kWh) if day_kWh else 0
    night_avg = sum(night_kWh) / len(night_kWh) if night_kWh else 0

    output_rows.append({
        '': weekday_names[wd],
        'Avg. Day Use': round(day_avg, 3),
        'Avg. Night Use (Midnight-5AM)': round(night_avg, 3)
    })

# Write CSV
with open(output_file, 'w', newline='') as f:
    fieldnames = ['', 'Avg. Day Use', 'Avg. Night Use (Midnight-5AM)']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print(f"✅ Output written to: {output_file}")
