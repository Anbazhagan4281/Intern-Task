import json
import csv

file_name = "students1.json"

def load_students():
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_students(students):
    with open(file_name, "w") as file:
        json.dump(students, file, indent=4)

def add_student():
    name = input("Enter name: ")
    age = input("Enter age: ")
    grade = input("Enter grade: ")

    students = load_students()
    students.append({"name": name, "age": age, "grade": grade})

    save_students(students)
    print("Student added successfully")

def view_students():
    students = load_students()

    if students:
        for student in students:
            print(f"Name: {student['name']}, Age: {student['age']}, Grade: {student['grade']}")
    else:
        print("No students found")

def export_to_csv():
    students = load_students()

    if students:
        with open("students.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "age", "grade"])
            writer.writeheader()
            writer.writerows(students)
        print("Exported to students.csv")
    else:
        print("No students to export")

def main():
    while True:
        print("\n1. Add Student 2. View Students 3. Export to CSV 4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            export_to_csv()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

main()
