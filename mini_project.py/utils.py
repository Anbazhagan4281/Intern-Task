import re

def is_valid_email(email):
    pattern = r"\w+@\w+\.\w+"
    return bool(re.fullmatch(pattern, email))

def calculate_avg(*marks):
    return sum(marks) / len(marks) if marks else 0

def get_status(avg):
    return "Pass" if avg >= 40 else "Fail"