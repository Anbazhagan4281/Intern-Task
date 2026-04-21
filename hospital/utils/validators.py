# utils/validators.py

import re


# Name validation
def is_valid_name(name):
    try:
        return bool(re.fullmatch(r"[A-Za-z ]{2,50}", name))
    except:
        return False


# Contact validation
def is_valid_contact(contact):
    try:
        return bool(re.fullmatch(r"\d{10}", contact))
    except:
        return False


# Email validation
def is_valid_email(email):
    try:
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))
    except:
        return False


# Blood group validation
def is_valid_blood_group(bg):
    if not isinstance(bg, str):
        return False
    bg = bg.upper()
    valid = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    return bg in valid