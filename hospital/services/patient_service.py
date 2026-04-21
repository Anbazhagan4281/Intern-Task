# services/patient_service.py

import json
import os

from models.patient import Patient
from models.prescription import Prescription
from utils.validators import (
    is_valid_name,
    is_valid_contact,
    is_valid_blood_group
)
from utils.helpers import (
    generate_id,
    sort_by_name,
    search_recursive,
    calculate_stats
)
from exceptions import (
    InvalidPatientDataError,
    InvalidAgeError,
    InvalidContactError,
    PatientNotFoundError,
    FileOperationError
)

# ✅ Base directory (hospital folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ Correct data file path
DATA_FILE = os.path.join(BASE_DIR, "data", "patients.json")


# ==============================
# Load data from JSON
# ==============================
def load_data():
    try:
        data_dir = os.path.join(BASE_DIR, "data")

        # create folder if not exists
        os.makedirs(data_dir, exist_ok=True)

        # create file if not exists
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

        # read data
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        # corrupted file → reset
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error loading file")


# ==============================
# Save data to JSON
# ==============================
def save_data(data):
    try:
        data_dir = os.path.join(BASE_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error saving file")


# ==============================
# Add Patient
# ==============================
def add_patient(name, age, blood_group, contact, **kwargs):

    if not is_valid_name(name):
        raise InvalidPatientDataError("Invalid name")

    if not (1 <= age <= 120):
        raise InvalidAgeError(age)

    if not is_valid_contact(contact):
        raise InvalidContactError(contact)

    if not is_valid_blood_group(blood_group):
        raise InvalidPatientDataError("Invalid blood group")

    data = load_data()

    patient_id = generate_id("P", data)

    patient = Patient(patient_id, name, age, blood_group.upper(), contact)

    data.append(patient.to_dict())
    save_data(data)

    return patient


# ==============================
# View All Patients
# ==============================
def view_all_patients():
    data = load_data()

    if not data:
        print("No patients found")
        return

    data = sort_by_name(data)

    print("\n--- PATIENT LIST ---")
    for p in data:
        print(f"{p['patient_id']} | {p['name']} | {p['age']} | {p['blood_group']}")


# ==============================
# Search Patient
# ==============================
def search_patient(patient_id):
    data = load_data()

    patient = search_recursive(data, "patient_id", patient_id)

    if not patient:
        raise PatientNotFoundError(patient_id)

    return patient


# ==============================
# Update Patient
# ==============================
def update_patient(patient_id, **kwargs):
    data = load_data()

    patient = search_recursive(data, "patient_id", patient_id)

    if not patient:
        raise PatientNotFoundError(patient_id)

    for key, value in kwargs.items():
        if key in patient and value:
            patient[key] = value

    save_data(data)


# ==============================
# Delete Patient
# ==============================
def delete_patient(patient_id):
    data = load_data()

    new_data = [p for p in data if p["patient_id"] != patient_id]

    if len(data) == len(new_data):
        raise PatientNotFoundError(patient_id)

    save_data(new_data)


# ==============================
# Add Prescription
# ==============================
def add_prescription(patient_id, medicine, dosage, days):
    data = load_data()

    patient = search_recursive(data, "patient_id", patient_id)

    if not patient:
        raise PatientNotFoundError(patient_id)

    prescription = Prescription(medicine, dosage, days)

    if "prescriptions" not in patient:
        patient["prescriptions"] = []

    patient["prescriptions"].append(prescription.to_dict())

    save_data(data)


# ==============================
# Get Statistics
# ==============================
def get_statistics():
    data = load_data()

    if not data:
        return {}

    ages = [p["age"] for p in data]

    total = len(data)
    youngest, oldest, avg = calculate_stats(*ages)

    blood_groups = {}
    for p in data:
        bg = p["blood_group"]
        blood_groups[bg] = blood_groups.get(bg, 0) + 1

    unique_bg = set(blood_groups.keys())

    return {
        "total": total,
        "average": round(avg, 2),
        "youngest": youngest,
        "oldest": oldest,
        "blood_counts": blood_groups,
        "unique": unique_bg
    }