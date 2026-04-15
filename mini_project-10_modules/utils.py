import re

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_email(email):
    pattern = r"\w+@\w+\.\w+"
    return bool(re.fullmatch(pattern, email))

def calculate_avg(marks):
    return sum(marks) / len(marks) if marks else 0

def get_status(avg):
    return "Pass" if avg >= 40 else "Fail"

def get_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "D"