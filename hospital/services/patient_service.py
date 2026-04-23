import json
import os
import matplotlib.pyplot as plt

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

# ==============================
# BASE PATH
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "patients.json")


# ==============================
# LOAD DATA
# ==============================
def load_data():
    try:
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

        with open(DATA_FILE, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []

    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error loading file")


# ==============================
# SAVE DATA
# ==============================
def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("DEBUG:", e)
        raise FileOperationError("Error saving file")


# ==============================
# RISK DETECTION
# ==============================
def detect_risk(age, blood_group):
    if age > 60:
        return "HIGH (Senior Citizen)"
    elif age < 10:
        return "MEDIUM (Child)"
    elif blood_group in ["O-", "AB-"]:
        return "MEDIUM (Rare Blood Group)"
    else:
        return "LOW"


# ==============================
# ADD PATIENT
# ==============================
def add_patient(name, age, blood_group, contact):

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

    patient_dict = patient.to_dict()

    # 🔥 Risk Detection
    patient_dict["risk_level"] = detect_risk(age, blood_group.upper())

    # 🔥 Doctor Assign
    doctor_id = input("Assign Doctor ID (D001/D002): ")
    patient_dict["doctor_id"] = doctor_id

    # 🚨 EMERGENCY ALERT
    if "HIGH" in patient_dict["risk_level"]:
        print("🚨 EMERGENCY ALERT! High risk patient!")

    # Save
    data.append(patient_dict)
    save_data(data)

    # 🚑 Emergency Check
    check_emergency(patient_dict)

    return patient_dict


# ==============================
# VIEW ALL
# ==============================
def view_all_patients():
    data = load_data()

    if not data:
        print("No patients found")
        return

    data = sort_by_name(data)

    print("\n--- PATIENT LIST ---")
    for p in data:
        print(f"{p['patient_id']} | {p['name']} | {p['age']} | {p['blood_group']} | {p.get('risk_level','-')}")


# ==============================
# SEARCH
# ==============================
def search_patient(patient_id):
    data = load_data()

    patient = search_recursive(data, "patient_id", patient_id)

    if not patient:
        raise PatientNotFoundError(patient_id)

    return patient


# ==============================
# UPDATE
# ==============================
def update_patient(patient_id, name=None, age=None):

    data = load_data()

    for p in data:
        if p["patient_id"] == patient_id:

            if name:
                p["name"] = name

            if age:
                p["age"] = age

            save_data(data)
            return p

    raise PatientNotFoundError(patient_id)


# ==============================
# DELETE
# ==============================
def delete_patient(patient_id):
    data = load_data()

    new_data = [p for p in data if p["patient_id"] != patient_id]

    if len(data) == len(new_data):
        raise PatientNotFoundError(patient_id)

    save_data(new_data)


# ==============================
# ADD PRESCRIPTION
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
# VIEW PRESCRIPTIONS
# ==============================
def view_prescriptions(patient_id):
    patient = search_patient(patient_id)

    if "prescriptions" not in patient:
        print("No prescriptions found")
        return

    print(f"\nPrescriptions for {patient['name']}:")
    for p in patient["prescriptions"]:
        print(f"{p['medicine']} | {p['dosage']} | {p['days']} days")


# ==============================
# STATISTICS
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

    return {
        "total": total,
        "average": round(avg, 2),
        "youngest": youngest,
        "oldest": oldest,
        "blood_counts": blood_groups
    }


# ==============================
# GRAPH
# ==============================
def show_graph():
    data = load_data()

    if not data:
        print("No data")
        return

    blood_groups = {}

    for p in data:
        bg = p["blood_group"]
        blood_groups[bg] = blood_groups.get(bg, 0) + 1

    plt.bar(list(blood_groups.keys()), list(blood_groups.values()))
    plt.xlabel("Blood Group")
    plt.ylabel("Patients")
    plt.title("Blood Group Distribution")
    plt.show()


# ==============================
# EMERGENCY ALERT
# ==============================
def check_emergency(patient_dict):

    risk = patient_dict.get("risk_level", "")

    if "HIGH" in risk:
        print("\n🚨 EMERGENCY ALERT 🚨")
        print("==============================")
        print(f"Patient ID : {patient_dict['patient_id']}")
        print(f"Name       : {patient_dict['name']}")
        print(f"Risk Level : {risk}")
        print("Immediate medical attention required!")
        print("==============================\n")