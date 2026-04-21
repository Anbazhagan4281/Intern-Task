# services/report_service.py

import json
import csv
import os
from exceptions import FileOperationError

# ✅ Base directory (hospital folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ Correct paths
DATA_FILE = os.path.join(BASE_DIR, "data", "patients.json")
CSV_FILE = os.path.join(BASE_DIR, "data", "patients.csv")
REPORT_DIR = os.path.join(BASE_DIR, "data", "reports")
BACKUP_FILE = os.path.join(BASE_DIR, "data", "backup.bin")


# ==============================
# Load JSON
# ==============================
def load_from_json():
    try:
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r") as f:
            return json.load(f)

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error loading JSON")


# ==============================
# Export JSON
# ==============================
def export_to_json(patients):
    try:
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

        with open(DATA_FILE, "w") as f:
            json.dump(patients, f, indent=4)

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error saving JSON")


# ==============================
# Export CSV
# ==============================
def export_to_csv(patients):
    try:
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["ID", "Name", "Age", "Blood Group", "Contact"])

            for p in patients:
                writer.writerow([
                    p["patient_id"],
                    p["name"],
                    p["age"],
                    p["blood_group"],
                    p["contact"]
                ])

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error exporting CSV")


# ==============================
# Generate TXT Report
# ==============================
def generate_report(patient):
    try:
        os.makedirs(REPORT_DIR, exist_ok=True)

        file_path = os.path.join(
            REPORT_DIR,
            f"{patient['patient_id']}_report.txt"
        )

        with open(file_path, "w") as f:
            f.write("====== PATIENT REPORT ======\n")
            f.write(f"ID          : {patient['patient_id']}\n")
            f.write(f"Name        : {patient['name']}\n")
            f.write(f"Age         : {patient['age']}\n")
            f.write(f"Blood Group : {patient['blood_group']}\n\n")

            f.write("Prescriptions:\n")

            for i, p in enumerate(patient.get("prescriptions", []), 1):
                f.write(
                    f"{i}. {p['medicine_name']} | {p['dosage']} | {p['days']} days\n"
                )

            f.write("============================\n")

        return file_path

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error generating report")


# ==============================
# Backup encode
# ==============================
def encode_backup(data):
    try:
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

        with open(BACKUP_FILE, "wb") as f:
            f.write(json.dumps(data).encode("utf-8"))

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Backup failed")