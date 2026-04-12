from utils import *
from file_handler import *

def generate_id(data):
    return max([s.get("id", 0) for s in data], default=0) + 1

def add_student():
    print("\n--- Add Student ---")
    name = input("Enter Name: ")
    try:
        age = int(input("Enter Age: "))
        if age <= 0:
            raise ValueError
    except ValueError:
        print("Invalid age")
        return

    email = input("Enter Email: ")
    if not is_valid_email(email):
        print("Invalid email")
        return

    try:
        marks = list(map(int, input("Enter marks (space separated): ").split()))
        if any(m < 0 or m > 100 for m in marks):
            print("Marks must be between 0-100")
            return
    except ValueError:
        print("Invalid marks")
        return

    data = load_data()

    student = {
        "id": generate_id(data),  
        "name": name,
        "age": age,
        "email": email,
        "marks": marks
    }

    data.append(student)
    save_data(data)

    print("Student added successfully!")

def view_students():
    print("\n--- Student List ---")
    data = load_data()

    if not data:
        print("No records found")
        return

    for s in data:
        avg = calculate_avg(*s["marks"])
        status = get_status(avg)

        print("="*30)
        print(f"ID: {s['id']}")
        print(f"Name: {s['name']}")
        print(f"Age: {s['age']}")
        print(f"Email: {s['email']}")
        print(f"Marks: {s['marks']}")
        print(f"Average: {avg:.2f}")
        print(f"Status: {status}")

def search_student():
    print("\n--- Search Student ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid ID")
        return
    
    data = load_data()

    for s in data:
        if s["id"] == sid:
            print("Student Found:")
            print(s)
            return

    print("Student not found")
def update_marks():
    print("\n--- Update Marks ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid ID")
        return

    data = load_data()

    for s in data:
        if s["id"] == sid:
            try:
                new_marks = list(map(int, input("Enter new marks: ").split()))
                s["marks"] = new_marks
                save_data(data)
                print("Marks updated")
                return
            except ValueError:
                print("Invalid marks")
                return

    print("Student not found")

def delete_student():
    print("\n--- Delete Student ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid ID")
        return

    data = load_data()

    new_data = [s for s in data if s["id"] != sid]

    if len(data) == len(new_data):
        print("Student not found")
    else:
        save_data(new_data)
        print("Student deleted")

def main():
    while True:
        print("\n" + "="*35)
        print(" STUDENT MANAGEMENT SYSTEM ")
        print("="*35)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Marks")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_marks()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()