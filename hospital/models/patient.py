# models/patient.py

from datetime import datetime


class Patient:
    total_patients = 0  # class variable

    def __init__(self, patient_id, name, age, blood_group, contact):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.blood_group = blood_group
        self.contact = contact
        self.prescriptions = []
        self.admitted_on = datetime.now()

        Patient.total_patients += 1

    def __str__(self):
        return f"{self.patient_id} - {self.name} ({self.age})"

    def __repr__(self):
        return f"Patient({self.patient_id}, {self.name})"

    def __eq__(self, other):
        return self.patient_id == other.patient_id

    def add_prescription(self, prescription):
        self.prescriptions.append(prescription)

    def get_summary(self):
        return {
            "id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "blood_group": self.blood_group
        }

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "blood_group": self.blood_group,
            "contact": self.contact,
            "prescriptions": [p.to_dict() for p in self.prescriptions],
            "admitted_on": self.admitted_on.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        patient = cls(
            data["patient_id"],
            data["name"],
            data["age"],
            data["blood_group"],
            data["contact"]
        )
        return patient

    @staticmethod
    def validate_blood_group(bg):
        valid = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        return bg in valid