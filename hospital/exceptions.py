# exceptions.py

# Base Exception
class HospitalError(Exception):
    def __init__(self, message="Hospital Error"):
        super().__init__(message)


# Patient not found
class PatientNotFoundError(HospitalError):
    def __init__(self, patient_id):
        self.patient_id = patient_id
        super().__init__(f"Patient with ID {patient_id} not found.")


# Invalid data
class InvalidPatientDataError(HospitalError):
    def __init__(self, message="Invalid patient data"):
        super().__init__(message)


# Invalid age
class InvalidAgeError(HospitalError):
    def __init__(self, age):
        self.age = age
        super().__init__(f"Invalid age: {age}. Age must be between 1 and 120.")


# Invalid contact
class InvalidContactError(HospitalError):
    def __init__(self, contact):
        self.contact = contact
        super().__init__(f"Invalid contact number: {contact}. Must be 10 digits.")


# Duplicate patient
class DuplicatePatientError(HospitalError):
    def __init__(self, patient_id):
        self.patient_id = patient_id
        super().__init__(f"Patient with ID {patient_id} already exists.")


# File error
class FileOperationError(HospitalError):
    def __init__(self, message="File operation failed"):
        super().__init__(message)