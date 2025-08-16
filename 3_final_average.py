# step3_final_average_to_csv.py

import csv
from datetime import datetime
from collections import defaultdict

input_file = 'filtered_year_no_outliers.csv'
output_file = 'final_weekday_averages.csv'

# Structure: weekday (0-6) → list of per-day totals {'day': float, 'night': float}
daily_usage_by_weekday = defaultdict(list)

# Structure: date string (YYYY-MM-DD) → {'weekday': int, 'day': [], 'night': []}
per_day_data = defaultdict(lambda: {'weekday': None, 'day': [], 'night': []})

# Read and group data per day
with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dt = datetime.fromisoformat(row['dateTime'].replace('Z', '+00:00'))
        kWh = float(row['kWh'])
        date_str = dt.date().isoformat()
        hour = dt.hour

        if per_day_data[date_str]['weekday'] is None:
            per_day_data[date_str]['weekday'] = dt.weekday()

        if 0 <= hour < 5:
            per_day_data[date_str]['night'].append(kWh)
        else:
            per_day_data[date_str]['day'].append(kWh)

# Calculate total usage per day and group by weekday
for date, data in per_day_data.items():
    weekday = data['weekday']
    day_total = sum(data['day'])
    night_total = sum(data['night'])
    daily_usage_by_weekday[weekday].append({'day': day_total, 'night': night_total})

# Prepare output
weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output_rows = []

for wd in range(7):
    all_days = daily_usage_by_weekday[wd]
    num_days = len(all_days)

    if num_days > 0:
        avg_day = sum(d['day'] for d in all_days) / num_days
        avg_night = sum(d['night'] for d in all_days) / num_days
    else:
        avg_day = avg_night = 0

    output_rows.append({
        '': weekday_names[wd],
        'Avg. Day Use': round(avg_day, 3),
        'Avg. Night Use (Midnight-5AM)': round(avg_night, 3)
    })

# Write to CSV
with open(output_file, 'w', newline='') as f:
    fieldnames = ['', 'Avg. Day Use', 'Avg. Night Use (Midnight-5AM)']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print(f"✅ Output written to: {output_file}")
