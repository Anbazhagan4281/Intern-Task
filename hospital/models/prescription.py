# models/prescription.py

from datetime import datetime, timedelta


class Prescription:
    def __init__(self, medicine_name, dosage, days):
        self.medicine_name = medicine_name
        self.dosage = dosage
        self.days = days
        self.prescribed_on = datetime.now()

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage} ({self.days} days)"

    def __repr__(self):
        return f"Prescription({self.medicine_name})"

    def to_dict(self):
        return {
            "medicine_name": self.medicine_name,
            "dosage": self.dosage,
            "days": self.days,
            "prescribed_on": self.prescribed_on.isoformat()
        }

    def is_active(self):
        end_date = self.prescribed_on + timedelta(days=self.days)
        return datetime.now() <= end_date