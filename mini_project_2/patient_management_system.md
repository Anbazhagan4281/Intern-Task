
# 🏥 Patient Management System
### Python Mini Project

---

## 📋 Project Overview

Build a **Hospital Patient Management System** as a Command Line Application where doctors can add patients, record prescriptions, search records, generate reports and save everything to files.

---

## 📁 Project Structure

```
hospital/
│
├── main.py                   ← Entry point — start app here
├── exceptions.py             ← All custom exceptions
│
├── models/
│   ├── __init__.py
│   ├── patient.py            ← Patient class
│   ├── doctor.py             ← Doctor class
│   └── prescription.py      ← Prescription class
│
├── services/
│   ├── __init__.py
│   ├── patient_service.py    ← Business logic
│   └── report_service.py     ← Reports and exports
│
├── utils/
│   ├── __init__.py
│   ├── validators.py         ← Input validations
│   └── helpers.py            ← Helper functions
│
└── data/
    ├── patients.json         ← Patient records saved here
    └── reports/              ← Generated report files go here
```

---

## ✅ App Features

1. Add a new patient
2. View all patients
3. Search patient by ID
4. Update patient details
5. Delete a patient
6. Add prescription to a patient
7. View hospital statistics
8. Generate patient report as `.txt` file
9. Export all patients to CSV file

---

## 📌 File-by-File Instructions

---

### exceptions.py

Create custom exceptions for every possible error in the app.

```
HospitalError                 ← Base exception (parent of all)
├── PatientNotFoundError      ← When patient ID does not exist
├── InvalidPatientDataError   ← When input data is wrong
├── InvalidAgeError           ← When age is out of valid range
├── InvalidContactError       ← When phone number format is wrong
├── DuplicatePatientError     ← When patient already exists
└── FileOperationError        ← When file save or load fails
```

Every exception must:
- Store meaningful data in `self` e.g. `self.age`, `self.patient_id`
- Pass a clear readable message to the parent using `super().__init__()`

---

### models/patient.py

Create a `Patient` class.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `patient_id` | string | Unique ID like `P001` |
| `name` | string | Full name |
| `age` | int | Age of patient |
| `blood_group` | string | A+, B+, O- etc |
| `contact` | string | 10-digit phone number |
| `prescriptions` | list | List of prescriptions |
| `admitted_on` | datetime | Auto set when patient is created |

**Methods:**

| Method | Description |
|--------|-------------|
| `__init__()` | Set up all attributes |
| `__str__()` | Readable display of patient |
| `__repr__()` | Developer-friendly display |
| `__eq__()` | Compare two patients by `patient_id` |
| `add_prescription()` | Add prescription to the list |
| `get_summary()` | Return patient info as dictionary |
| `to_dict()` | Convert to dict for saving to JSON |
| `from_dict()` | Class method — create Patient from dict |

**Also include:**
- A class variable `total_patients = 0` that increases every time a new Patient is created
- A static method `validate_blood_group(bg)` that checks if blood group is valid

---

### models/doctor.py

Create a `Doctor` class.

**Attributes:**
- `doctor_id`
- `name`
- `specialization`
- `patients_treated` — list of patient IDs

**Methods:**
- `__init__()`
- `__str__()`
- `assign_patient(patient_id)` — add patient ID to the list
- `get_patient_count()` — return total number of patients treated

---

### models/prescription.py

Create a `Prescription` class.

**Attributes:**
- `medicine_name`
- `dosage`
- `days`
- `prescribed_on` — datetime set automatically

**Methods:**
- `__init__()`
- `__str__()`
- `to_dict()` — for saving to JSON
- `is_active()` — return `True` if prescription period has not ended yet

---

### utils/validators.py

Write input validation functions using the `re` module.

| Function | What It Checks |
|----------|----------------|
| `is_valid_name(name)` | Only letters and spaces, 2 to 50 characters |
| `is_valid_contact(contact)` | Exactly 10 digits |
| `is_valid_email(email)` | Proper email format |
| `is_valid_blood_group(bg)` | Only A+, A-, B+, B-, O+, O-, AB+, AB- |

All functions must:
- Return `True` or `False` only
- Handle any unexpected input safely without crashing

---

### utils/helpers.py

Write these helper functions:

**`generate_id(prefix, data)`**
- Generates unique IDs like `P001`, `P002`, `P003`
- Returns a formatted string

**`format_date(dt)`**
- Takes a datetime object and returns a readable date string

**`calculate_stats(*values)`**
- Accepts any number of values
- Returns `(minimum, maximum, average)` as a tuple

**`session_tracker()`**
- A closure function
- Tracks how many operations have been done in this session
- Each call increases the count and prints the operation name

**`search_recursive(data, key, value, index=0)`**
- Searches through a list recursively
- Returns the matched item or `None` if not found

**Also define these as lambda functions:**
```python
sort_by_name  = lambda patients: sorted(patients, key=lambda p: p["name"])
sort_by_age   = lambda patients: sorted(patients, key=lambda p: p["age"])
filter_adults = lambda patients: [p for p in patients if p["age"] >= 18]
```

---

### services/patient_service.py

Write the core business logic functions:

**`add_patient(name, age, blood_group, contact, **kwargs)`**
- Validate all inputs — raise appropriate custom exceptions if invalid
- Create a `Patient` object
- Save to JSON file

**`view_all_patients()`**
- Load from JSON
- Display all patients in a clean formatted way
- Sorted by name

**`search_patient(patient_id)`**
- Use `search_recursive()` to find the patient
- Raise `PatientNotFoundError` if not found
- Return patient data

**`update_patient(patient_id, **kwargs)`**
- Find the patient by ID
- Update only the fields passed in `**kwargs`
- Save back to JSON

**`delete_patient(patient_id)`**
- Remove the patient from the list
- Raise `PatientNotFoundError` if ID does not exist
- Save updated list

**`add_prescription(patient_id, medicine, dosage, days)`**
- Find the patient
- Create a `Prescription` object
- Add to patient's prescriptions list
- Save to JSON

**`get_statistics()`**
- Return total patients, average age, youngest, oldest
- Count of each blood group
- Set of unique blood groups present

---

### services/report_service.py

Write all file-related functions:

**`export_to_json(patients)`**
- Save all patients to `data/patients.json`
- Use proper indentation for readability

**`export_to_csv(patients)`**
- Save all patients to `data/patients.csv`
- Include proper column headers

**`load_from_json()`**
- Load and return the patient list from JSON file
- Return empty list `[]` if file does not exist

**`generate_report(patient)`**
- Create a `.txt` report for one patient
- Include all patient details and prescriptions
- Save to `data/reports/P001_report.txt`

**`encode_backup(data)`**
- Encode all data to bytes using UTF-8
- Save as binary file `data/backup.bin`

---

### main.py

Connect everything together here.

- Show a clean menu in a loop
- Call the correct service function based on user choice
- Track total operations using `session_tracker()` closure
- Exit cleanly using `sys.exit()`
- Wrap every menu action in `try/except` — no raw crashes allowed
- Must end with `if __name__ == "__main__": main()`

---

## 💻 Expected Output

```
╔══════════════════════════════════╗
║   🏥 PATIENT MANAGEMENT SYSTEM   ║
╚══════════════════════════════════╝
Session Operations: 0

1. Add Patient          5. Delete Patient
2. View All Patients    6. Add Prescription
3. Search Patient       7. View Statistics
4. Update Patient       8. Generate Report
                        9. Export to CSV
                        0. Exit
==================================
Enter choice: 1

--- Add Patient ---
Enter Name        : Ravi Kumar
Enter Age         : 28
Enter Blood Group : B+
Enter Contact     : 9876543210

✅ Patient Added Successfully!
🪪 Patient ID : P001
📅 Admitted   : 2024-01-15 10:30:00
Session Operations: 1

==================================
Enter choice: 3

--- Search Patient ---
Enter Patient ID: P001

╔══════════════════════╗
║   PATIENT DETAILS    ║
╠══════════════════════╣
║ ID         : P001    ║
║ Name       : Ravi    ║
║ Age        : 28      ║
║ Blood Group: B+      ║
║ Contact    : 9876..  ║
╚══════════════════════╝

==================================
Enter choice: 7

📊 Hospital Statistics
==============================
Total Patients    : 3
Average Age       : 31.5
Youngest          : 22
Oldest            : 45
Unique Blood Groups: {B+, O+, A-}
Blood Group Counts:
  B+  : 2 patients
  O+  : 1 patient
  A-  : 1 patient
Session Operations: 3
==============================

==================================
Enter choice: 8
Enter Patient ID: P001

✅ Report generated!
📁 Saved: data/reports/P001_report.txt

====== PATIENT REPORT ======
ID          : P001
Name        : Ravi Kumar
Age         : 28
Blood Group : B+
Admitted    : 2024-01-15

Prescriptions:
1. Paracetamol | 500mg  | 5 days  | Active ✅
2. Vitamin C   | 250mg  | 10 days | Active ✅
============================
```

---

## ⚠️ Rules

1. Must use the **folder structure** shown above — do not put everything in one file
2. Every folder must have an `__init__.py` file
3. Every class must have `__str__` and `__repr__` methods
4. All file operations must be wrapped in `try/except`
5. Use **custom exceptions** for all errors — do not use plain `ValueError` or `Exception`
6. Add a short comment above every function explaining what it does
7. App must run with `python main.py`
8. Code must run without any errors before submitting

---


*Build it one file at a time. Start with `exceptions.py`, then `models/`, then `utils/`, then `services/`, and finally `main.py`. Good luck! 💪*