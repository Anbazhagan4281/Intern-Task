# Hospital Management System — Code Review
# Issues & Solutions for Intern

Date      : 2026-04-26
Project   : Hospital Patient Management System

Read every issue carefully.
Understand the problem.
Apply the solution in the actual code file.
Check the box once fixed: change [ ] to [x]

---

## CRITICAL BUGS (Fix These First)

---

### ISSUE 1 — ID Collision After Delete
- [ ] Fixed

**File:** `hospital/utils/helpers.py` — Line 8

**Problem:**
The ID is generated using `len(data) + 1`.
If you add 3 patients (P001, P002, P003), delete P002,
then add a new patient — `len(data)` is 2, so it generates P003 again.
P003 already exists. Now you have two patients with the same ID.
This will cause wrong search results, wrong updates, and wrong deletes.

**Current Code:**
```python
def generate_id(prefix, data):
    return f"{prefix}{len(data)+1:03d}"
```

**Solution:**
Find the highest existing number in the IDs and add 1 to it.

**Fixed Code:**
```python
def generate_id(prefix, data):
    if not data:
        return f"{prefix}001"
    existing = [
        int(p["patient_id"][len(prefix):])
        for p in data
        if p["patient_id"].startswith(prefix)
    ]
    return f"{prefix}{max(existing)+1:03d}"
```

---

### ISSUE 2 — Indentation Bug Causes Crash in Statistics
- [ ] Fixed

**File:** `hospital/main.py` — Lines 105 to 109

**Problem:**
The `for` loop and the last two `print` lines are OUTSIDE the `else` block.
When there are no patients, `stats` is an empty dict `{}`.
Python still runs those lines and crashes with a `KeyError` on `stats["blood_counts"]`.

**Current Code:**
```python
if not stats:
 print("No data available")
else:
 print("\n Hospital Statistics")
 print("=" * 30)
 print(f"Total Patients     : {stats['total']}")
 print(f"Average Age        : {stats['average']}")
 print(f"Youngest           : {stats['youngest']}")
 print(f"Oldest             : {stats['oldest']}")

 print("\nBlood Group Counts:")
for bg, count in stats["blood_counts"].items():   # <-- WRONG: outside else
    print(f"  {bg}  : {count} patients")

print(f"\nUnique Blood Groups: {stats['unique']}")  # <-- WRONG: outside else
print("=" * 30)
```

**Solution:**
Move the `for` loop and the last two prints INSIDE the `else` block by increasing their indentation.

**Fixed Code:**
```python
if not stats:
    print("No data available")
else:
    print("\n Hospital Statistics")
    print("=" * 30)
    print(f"Total Patients     : {stats['total']}")
    print(f"Average Age        : {stats['average']}")
    print(f"Youngest           : {stats['youngest']}")
    print(f"Oldest             : {stats['oldest']}")

    print("\nBlood Group Counts:")
    for bg, count in stats["blood_counts"].items():
        print(f"  {bg}  : {count} patients")

    print(f"\nUnique Blood Groups: {stats['unique']}")
    print("=" * 30)
```

---

### ISSUE 3 — from_dict Does Not Restore Prescriptions or Admitted Date
- [ ] Fixed

**File:** `hospital/models/patient.py` — Lines 52 to 60

**Problem:**
`from_dict()` creates a new Patient using `datetime.now()` as `admitted_on`.
This means every time you reconstruct a patient from saved data, their
admission date resets to right now — losing the real date.
Also, the saved prescriptions in the dict are completely ignored.
They are never loaded back into `patient.prescriptions`.

**Current Code:**
```python
@classmethod
def from_dict(cls, data):
    patient = cls(
        data["patient_id"],
        data["name"],
        data["age"],
        data["blood_group"],
        data["contact"]
    )
    return patient   # admitted_on is wrong, prescriptions are lost
```

**Solution:**
After creating the patient, override `admitted_on` with the stored value
and rebuild the prescriptions list from the stored data.

**Fixed Code:**
```python
from datetime import datetime
from models.prescription import Prescription   # add this import at top of file

@classmethod
def from_dict(cls, data):
    patient = cls(
        data["patient_id"],
        data["name"],
        data["age"],
        data["blood_group"],
        data["contact"]
    )
    # restore real admission date
    patient.admitted_on = datetime.fromisoformat(data["admitted_on"])

    # restore all prescriptions
    patient.prescriptions = [
        Prescription(
            p["medicine_name"],
            p["dosage"],
            p["days"]
        )
        for p in data.get("prescriptions", [])
    ]
    return patient
```

---

### ISSUE 4 — Recursive Search Will Crash With Many Patients
- [ ] Fixed

**File:** `hospital/utils/helpers.py` — Lines 36 to 41

**Problem:**
The search function calls itself recursively, one step per patient.
Python has a default recursion limit of 1000.
If you ever have 1000+ patients, this will raise a `RecursionError` and crash.
There is no reason to use recursion here. A simple loop does the same job safely.

**Current Code:**
```python
def search_recursive(data, key, value, index=0):
    if index >= len(data):
        return None
    if data[index].get(key) == value:
        return data[index]
    return search_recursive(data, key, value, index + 1)
```

**Solution:**
Replace the recursion with a simple loop using `next()`.
Keep the function name the same so nothing else breaks.

**Fixed Code:**
```python
def search_recursive(data, key, value, index=0):
    return next((item for item in data if item.get(key) == value), None)
```

---

## LOGIC ISSUES (Fix After Critical)

---

### ISSUE 5 — Update Patient Skips Falsy Values
- [ ] Fixed

**File:** `hospital/services/patient_service.py` — Line 152

**Problem:**
The condition `if key in patient and value:` checks if `value` is truthy.
If you try to set age to `0` or clear a name to `""`, the update is silently skipped.
Python treats `0`, `""`, `[]` as falsy, so they never get saved.

**Current Code:**
```python
for key, value in kwargs.items():
    if key in patient and value:
        patient[key] = value
```

**Solution:**
Change the condition to check `is not None` instead of checking truthiness.

**Fixed Code:**
```python
for key, value in kwargs.items():
    if key in patient and value is not None:
        patient[key] = value
```

---

### ISSUE 6 — Patient.total_patients Counter Is Unreliable
- [ ] Fixed

**File:** `hospital/models/patient.py` — Lines 7 and 18

**Problem:**
`total_patients` is a class variable that increments every time a `Patient()`
object is created in memory — including temporary objects.
It never decrements when a patient is deleted.
It does not match the actual count of patients saved in the JSON file.
This counter gives wrong information and should not be trusted.

**Current Code:**
```python
class Patient:
    total_patients = 0

    def __init__(self, ...):
        ...
        Patient.total_patients += 1
```

**Solution:**
Remove `total_patients` from the model entirely.
To get the real count, use `len(load_data())` inside `get_statistics()`.
The statistics service already returns the correct total — use that.

**Fixed Code:**
Remove these two lines from `patient.py`:
```python
total_patients = 0        # delete this line
Patient.total_patients += 1  # delete this line
```

---

### ISSUE 7 — Duplicate Contact Numbers Are Allowed
- [ ] Fixed

**File:** `hospital/services/patient_service.py` — Inside `add_patient()` function

**Problem:**
Two different patients can be registered with the exact same contact number.
Example: P001 and P006 in the current `patients.json` both have `9443565172`.
There is no check to prevent this. Contact numbers should be unique per patient.

**Solution:**
Before saving, check if the contact already exists in the data.
Raise an error if it does.

**Fixed Code — add this block inside `add_patient()` after loading data:**
```python
data = load_data()

# check for duplicate contact
for existing in data:
    if existing["contact"] == contact:
        raise InvalidPatientDataError(
            f"Contact {contact} is already registered to patient {existing['patient_id']}"
        )

patient_id = generate_id("P", data)
```

---

### ISSUE 8 — search_patient Returns a Dict, Not a Patient Object
- [ ] Fixed

**File:** `hospital/services/patient_service.py` — Line 137

**Problem:**
`add_patient()` returns a `Patient` object.
`search_patient()` returns a raw dictionary from the JSON file.
These are inconsistent. In `main.py` line 65, `print(p)` prints a messy dict
instead of the clean `Patient ID - Name (Age)` format from `__str__`.

**Current Code:**
```python
def search_patient(patient_id):
    data = load_data()
    patient = search_recursive(data, "patient_id", patient_id)
    if not patient:
        raise PatientNotFoundError(patient_id)
    return patient   # returns a dict
```

**Solution:**
Convert the found dict to a Patient object before returning.

**Fixed Code:**
```python
from models.patient import Patient   # already imported

def search_patient(patient_id):
    data = load_data()
    patient_dict = search_recursive(data, "patient_id", patient_id)
    if not patient_dict:
        raise PatientNotFoundError(patient_id)
    return Patient.from_dict(patient_dict)   # return a proper Patient object
```

Note: fix ISSUE 3 first, because this depends on `from_dict` working correctly.

---

## CODE QUALITY (Fix Last)

---

### ISSUE 9 — DEBUG Prints Leak Raw Errors to Users
- [ ] Fixed

**Files:**
- `hospital/services/patient_service.py` — Lines 60 and 76
- `hospital/services/report_service.py` — Lines 32, 47, 73, 108, 121

**Problem:**
Every `except` block does `print("DEBUG:", e)` before raising the proper error.
This exposes raw Python exception messages to the user.
For example: `DEBUG: [Errno 13] Permission denied: '/data/patients.json'`
Users should never see internal debug messages. Logs are for developers.

**Current Code (example):**
```python
except Exception as e:
    print("DEBUG:", e)
    raise FileOperationError("Error loading file")
```

**Solution:**
Remove all `print("DEBUG:", e)` lines.
If you want to keep logging for developers, use Python's `logging` module instead.

**Fixed Code:**
```python
import logging

except Exception as e:
    logging.error(f"File load error: {e}")   # goes to log, not to user screen
    raise FileOperationError("Error loading file")
```

Or simply delete the `print("DEBUG:", e)` line if logging setup is too much for now.

---

### ISSUE 10 — Dead Code That Is Never Used
- [ ] Fixed

**Problem:**
The following items are defined but never imported or called anywhere.
They add confusion and make the codebase harder to understand.

| What | File | Why Unused |
|---|---|---|
| `Doctor` class | `models/doctor.py` | Never imported anywhere |
| `export_to_json()` | `services/report_service.py` Line 39 | Never called anywhere |
| `is_valid_email()` | `utils/validators.py` Line 23 | Never called anywhere |
| `format_date()` | `utils/helpers.py` Line 13 | Never called anywhere |
| `sort_by_age` lambda | `utils/helpers.py` Line 46 | Never called anywhere |
| `filter_adults` lambda | `utils/helpers.py` Line 47 | Never called anywhere |

**Solution:**
Option A — Delete them if they will never be needed.
Option B — If `Doctor` will be used in the future, leave it but add a comment:
```python
# Doctor model — not yet wired into the system
```

For now, the safest choice is to delete all of them to keep the codebase clean.

---

### ISSUE 11 — encode_backup Is Misleadingly Named
- [ ] Fixed

**File:** `hospital/services/report_service.py` — Lines 115 to 121

**Problem:**
The function is named `encode_backup` and writes to a `.bin` file.
This makes it look like the data is encrypted or encoded securely.
In reality, it just writes JSON as UTF-8 bytes — no real encoding happens.
Anyone can open the `.bin` file and read it directly. It provides no security.

**Current Code:**
```python
def encode_backup(data):
    with open(BACKUP_FILE, "wb") as f:
        f.write(json.dumps(data).encode("utf-8"))
```

**Solution:**
Rename it to `save_backup` to accurately describe what it does.
Change `BACKUP_FILE` extension from `.bin` to `.json` to avoid confusion.

**Fixed Code:**
```python
BACKUP_FILE = os.path.join(BASE_DIR, "data", "backup.json")

def save_backup(data):
    try:
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
        with open(BACKUP_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise FileOperationError("Backup failed")
```

---

### ISSUE 12 — No Input Stripping (Whitespace in Names)
- [ ] Fixed

**File:** `hospital/main.py` — Lines 49 to 52

**Problem:**
If a user accidentally types `" John "` (with spaces), it is saved as `" John "`.
This is a different patient than `"John"`.
Search, update, and delete will not match because the names differ.
The name validator also rejects leading/trailing spaces.

**Current Code:**
```python
name = input("Name: ")
age = int(input("Age: "))
bg = input("Blood Group: ").upper()
contact = input("Contact: ")
```

**Solution:**
Call `.strip()` on all text inputs to remove accidental whitespace.

**Fixed Code:**
```python
name = input("Name: ").strip()
age = int(input("Age: ").strip())
bg = input("Blood Group: ").strip().upper()
contact = input("Contact: ").strip()
```

---

## Checklist Summary

Once you fix each issue, mark it done by changing `[ ]` to `[x]` in this file.

| # | Issue | Priority | File |
|---|---|---|---|
| 1 | ID collision after delete | CRITICAL | utils/helpers.py |
| 2 | Indentation crash in statistics | CRITICAL | main.py |
| 3 | from_dict loses prescriptions and date | CRITICAL | models/patient.py |
| 4 | Recursive search hits recursion limit | CRITICAL | utils/helpers.py |
| 5 | Update skips falsy values | LOGIC | services/patient_service.py |
| 6 | total_patients counter is unreliable | LOGIC | models/patient.py |
| 7 | Duplicate contact numbers allowed | LOGIC | services/patient_service.py |
| 8 | search_patient returns dict not object | LOGIC | services/patient_service.py |
| 9 | DEBUG prints leak to users | QUALITY | services/*.py |
| 10 | Dead code never used | QUALITY | multiple files |
| 11 | encode_backup is misleadingly named | QUALITY | services/report_service.py |
| 12 | No input stripping on user inputs | QUALITY | main.py |

---

Good luck. Fix CRITICAL issues first, then LOGIC, then QUALITY.
Ask your reviewer after fixing each section.
