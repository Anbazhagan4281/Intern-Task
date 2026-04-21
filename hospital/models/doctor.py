# models/doctor.py

class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.patients_treated = []

    def __str__(self):
        return f"Dr.{self.name} ({self.specialization})"

    def __repr__(self):
        return f"Doctor({self.doctor_id}, {self.name})"

    def assign_patient(self, patient_id):
        self.patients_treated.append(patient_id)

    def get_patient_count(self):
        return len(self.patients_treated)