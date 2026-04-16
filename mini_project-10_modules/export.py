import csv
import os
from file_handler import load_data
from utils import calculate_age, calculate_avg, get_status, get_grade

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "students.csv")


def export_to_csv():
    data = load_data()

    if not data:
        print("No data to export")
        return

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID", "Name", "DOB", "Age", "Phone", "Email",
                "Marks", "Average", "Status", "Grade"
            ])

            for s in data:
                dob = s.get("date_of_birth") or s.get("date of birth")

                avg = calculate_avg(s["marks"])
                status = get_status(avg)
                grade = get_grade(avg)

                writer.writerow([
                    s["id"],
                    s["name"],
                    dob,
                    calculate_age(dob),
                    s.get("phone", ""),
                    s["email"],
                    " ".join(map(str, s["marks"])),
                    round(avg, 2),
                    status,
                    grade
                ])

        print("CSV file created successfully!")

    except Exception as e:
        print("Error exporting CSV:", e)