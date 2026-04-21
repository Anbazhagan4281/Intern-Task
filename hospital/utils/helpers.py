# utils/helpers.py

from datetime import datetime


# Generate ID
def generate_id(prefix, data):
    return f"{prefix}{len(data)+1:03d}"


# Format date
def format_date(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# Stats calculation
def calculate_stats(*values):
    if not values:
        return (0, 0, 0)
    return (min(values), max(values), sum(values)/len(values))


# Closure function
def session_tracker():
    count = 0

    def track(operation):
        nonlocal count
        count += 1
        print(f"Session Operations: {count} ({operation})")

    return track


# Recursive search
def search_recursive(data, key, value, index=0):
    if index >= len(data):
        return None
    if data[index].get(key) == value:
        return data[index]
    return search_recursive(data, key, value, index + 1)


# Lambda functions
sort_by_name  = lambda patients: sorted(patients, key=lambda p: p["name"])
sort_by_age   = lambda patients: sorted(patients, key=lambda p: p["age"])
filter_adults = lambda patients: [p for p in patients if p["age"] >= 18]