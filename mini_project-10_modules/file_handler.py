import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "data.json")


def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_data(data):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print("Error saving data:", e)