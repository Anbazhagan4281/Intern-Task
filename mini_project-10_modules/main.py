from utils import is_valid_phone, is_valid_email, calculate_avg, get_status, get_grade
from file_handler import load_data, save_data
from export import export_to_csv

class InvalidAgeError(Exception):
    pass

class InvalidDOBError(Exception):
    pass

class InvalidPhoneError(Exception):
    pass

class InvalidEmailError(Exception):
    pass

class InvalidMarksError(Exception):
    pass

def generate_id(data):
    if not data:
        return 1
    return max(s["id"] for s in data) + 1


def get_dob(student):
    # Handles both old + new data keys
    return student.get("date_of_birth") or student.get("date of birth")


def add_student():
    print("\n--- Add Student ---")
    name = input("Enter Name: ")

    try:
        age = int(input("Enter Age: "))
        if age <= 0:
            raise InvalidAgeError("Error: Age must be greater than 0")
    except ValueError:
        print("Error: Age must be a number")
        return
    except InvalidAgeError as e:
        print(e)
        return

    try:
        dob = input("Enter DOB (DD/MM/YYYY): ")
        if len(dob.split("/")) != 3:
            raise InvalidDOBError("Error: ---Invalid DOB format---")
    except InvalidDOBError as e:
        print(e)
        return
    
    try:
        phone = input("Enter Phone Number: ")
        if not is_valid_phone(phone):
            raise InvalidPhoneError("Error: ---Invalid phone number---")
    except InvalidPhoneError as e:
        print(e)
        return

    try:
        email = input("Enter Email: ")
        if not is_valid_email(email):
            raise InvalidEmailError("Error: ---Invalid email---")
    except InvalidEmailError as e:
        print(e)
        return

    try:
        marks = list(map(int, input("Enter marks (space separated): ").split()))
        if any(m < 0 or m > 100 for m in marks):
            raise InvalidMarksError("Error: ---Marks must be between 0-100---")
    except ValueError:
        print("Error: ---Marks must be numbers---")
        return
    except InvalidMarksError as e:
        print(e)
        return

    data = load_data()

    student = {
        "id": generate_id(data),   
        "name": name,
        "date_of_birth": dob,      
        "age": age,
        "phone": phone,
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
        dob = get_dob(s)  
        avg = calculate_avg(s["marks"]) 
        status = get_status(avg)
        grade = get_grade(avg)


        print("=" * 30)
        print(f"ID: {s['id']}")
        print(f"Name: {s['name']}")
        print(f"Date of Birth: {dob}")
        print(f"Age: {s['age']}")
        print(f"Phone: {s.get('phone', 'N/A')}")
        print(f"Email: {s['email']}")
        print(f"Marks: {s['marks']}")
        print(f"Average: {avg:.2f}")
        print(f"Status: {status}")
        print(f"Grade: {grade}")

def search_student():
    print("\n--- Search Student ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Error: ---Invalid ID---")
        return
    
    data = load_data()

    for s in data:
        if s["id"] == sid:
         print("Student Found:")
         print("ID:", s["id"])
         print("Name:", s["name"])
         print("Age:", s["age"])
         print("Phone:", s.get("phone", "N/A"))
         print("Email:", s["email"])

         print("Marks:")
        for i, m in enumerate(s["marks"], 1):
           print(f"Subject {i}: {m}")
        return

    print("Student not found")


def update_marks():
    print("\n--- Update Marks ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Error: ---Invalid ID---")
        return

    data = load_data()

    for s in data:
        if s["id"] == sid:
            try:
                new_marks = list(map(int, input("Enter new marks: ").split()))

                if any(m < 0 or m > 100 for m in new_marks):
                    raise InvalidMarksError("Error: ---Marks must be between 0-100---")

                s["marks"] = new_marks
                save_data(data)

                print("Marks updated successfully")
                return

            except ValueError:
                print("Error: ---Marks must be numbers---")
                return
            except InvalidMarksError as e:
                print(e)
                return

    print("Student not found")

def edit_student():
    print("\n--- Edit Student ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid ID")
        return

    data = load_data()

    for s in data:
        if s["id"] == sid:
            print("Leave blank to keep old value")

            name = input("Enter new name: ")
            email = input("Enter new email: ")

            if name:
                s["name"] = name
            
            phone = input("Enter new phone: ")

            if phone:
             if not is_valid_phone(phone):
                print("Invalid phone number")
                return
            s["phone"] = phone

            if email:
                if not is_valid_email(email):
                    print("Invalid email")
                    return
                s["email"] = email

            save_data(data)
            print("Student updated successfully")
            return

    print("Student not found")


def delete_student():
    print("\n--- Delete Student ---")

    try:
        sid = int(input("Enter Student ID: "))
    except ValueError:
        print("Error: ---Invalid ID---")
        return

    data = load_data()

    new_data = [s for s in data if s["id"] != sid]

    if len(data) == len(new_data):
        print("Error: ---Student not found---")
    else:
        save_data(new_data)
        print("Student deleted successfully")

def show_topper():
    print("\n--- Topper ---")

    data = load_data()

    if not data:
        print("No records found")
        return

    topper = max(data, key=lambda s: calculate_avg(s["marks"]))

    avg = calculate_avg(topper["marks"])

    print("Topper Details:")
    print(f"Name: {topper['name']}")
    print(f"ID: {topper['id']}")
    print(f"Average: {avg:.2f}")


def main():
    while True:
        print("\n" + "=" * 35)
        print(" STUDENT MANAGEMENT SYSTEM ")
        print("=" * 35)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Marks")
        print("5. Edit Student")
        print("6. Delete Student")
        print("7. Show Topper")
        print("8. Export to CSV")
        print("9. Exit")

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
            edit_student()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            show_topper()
        elif choice == "8":
            export_to_csv()
        elif choice == "9":
            print("Exiting")
            break
        else:
            print("Error: ---Invalid choice---")


if __name__ == "__main__":
    main()