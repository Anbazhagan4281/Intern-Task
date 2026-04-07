contact = {}

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")
    contact[name] = {"phone": phone, "email": email}
    print("Contact added")

def search_contact():
    name = input("Enter name to search: ")
    if name in contact:
        print("\nName:", name)
        print("Phone:", contact[name]["phone"])
        print("Email:", contact[name]["email"])
    else:
        print("Not found")

def update_contact():
    name = input("Enter name to update: ")
    if name in contact:
        phone = input("Enter new phone: ")
        email = input("Enter new email: ")
        contact[name] = {"phone": phone, "email": email}
        print("Updated")
    else:
        print("Not found")

def delete_contact():
    name = input("Enter name to delete: ")
    if name in contact:
        del contact[name]
        print("Deleted")
    else:
        print("Not found")

def show_all():
    if contact:
        for name, details in contact.items():
            print("\nName:", name)
            print("Phone:", details["phone"])
            print("Email:", details["email"])
    else:
        
        print("No contact")

while True:
    print("\n1.Add 2.Search 3.Update 4.Delete 5.Show 6.Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        search_contact()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        show_all()
    elif choice == "6":
        print("exit")
        break
    else:
        print("Invalid ")
        