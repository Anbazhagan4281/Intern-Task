import sys

# Patient Service imports
from services.patient_service import (
    add_patient,
    view_all_patients,
    search_patient,
    update_patient,
    delete_patient,
    add_prescription,
    view_prescriptions,
    get_statistics,
    show_graph
)

# Report Service imports
from services.report_service import (
    load_from_json,
    export_to_csv,
    generate_report,
    generate_department_report
)

# Utils
from utils.helpers import session_tracker


# ==============================
# LOGIN SYSTEM
# ==============================
def login():
    USERNAME = "admin"
    PASSWORD = "1234"

    print("\nLOGIN REQUIRED")
    print("=" * 25)

    for attempt in range(3):
        user = input("Username: ")
        pwd = input("Password: ")

        if user == USERNAME and pwd == PASSWORD:
            print("Login Successful\n")
            return True
        else:
            print("Invalid credentials\n")

    print("Too many attempts. Exiting...")
    return False


# ==============================
# MAIN PROGRAM
# ==============================
def main():

    if not login():
        return

    tracker = session_tracker()

    while True:
        print("\nPATIENT MANAGEMENT SYSTEM")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Add Prescription")
        print("7. View Prescriptions")
        print("8. View Statistics")
        print("9. Generate Report")
        print("10. Export CSV")
        print("11. Show Graph")
        print("12. Doctor & Department Report")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            # ==============================
            # ADD PATIENT
            # ==============================
            if choice == "1":
                name = input("Name: ")
                age = int(input("Age: "))
                bg = input("Blood Group: ").upper()
                contact = input("Contact: ")

                p = add_patient(name, age, bg, contact)

                print("\nAdded Successfully!")
                print(f"ID          : {p['patient_id']}")
                print(f"Risk Level  : {p.get('risk_level')}")

                tracker("Add Patient")

            # ==============================
            # VIEW ALL
            # ==============================
            elif choice == "2":
                view_all_patients()
                tracker("View All")

            # ==============================
            # SEARCH
            # ==============================
            elif choice == "3":
                pid = input("Enter Patient ID: ")

                try:
                    p = search_patient(pid)

                    print("\n--- PATIENT DETAILS ---")
                    print(f"ID        : {p['patient_id']}")
                    print(f"Name      : {p['name']}")
                    print(f"Age       : {p['age']}")
                    print(f"Blood     : {p['blood_group']}")
                    print(f"Contact   : {p['contact']}")
                    print(f"Risk      : {p.get('risk_level','-')}")

                except Exception:
                    print("Patient not found")

                tracker("Search")

            # ==============================
            # UPDATE
            # ==============================
            elif choice == "4":
                pid = input("Enter Patient ID: ")
                name = input("New Name (leave blank to skip): ")

                update_patient(pid, name=name)

                print("Updated Successfully!")
                tracker("Update")

            # ==============================
            # DELETE
            # ==============================
            elif choice == "5":
                pid = input("Enter Patient ID: ")

                delete_patient(pid)

                print("Deleted Successfully!")
                tracker("Delete")

            # ==============================
            # ADD PRESCRIPTION
            # ==============================
            elif choice == "6":
                pid = input("Patient ID: ")
                med = input("Medicine: ")
                dos = input("Dosage: ")
                days = int(input("Days: "))

                add_prescription(pid, med, dos, days)

                print("Prescription Added!")
                tracker("Prescription")

            # ==============================
            # VIEW PRESCRIPTIONS
            # ==============================
            elif choice == "7":
                pid = input("Enter Patient ID: ")
                view_prescriptions(pid)
                tracker("View Prescription")

            # ==============================
            # STATISTICS
            # ==============================
            elif choice == "8":
                stats = get_statistics()

                if not stats:
                    print("No data available")
                else:
                    print("\nHOSPITAL STATISTICS")
                    print("=" * 35)

                    print(f"Total Patients     : {stats['total']}")
                    print(f"Average Age        : {stats['average']}")
                    print(f"Youngest           : {stats['youngest']}")
                    print(f"Oldest             : {stats['oldest']}")

                    print("\nBlood Group Counts:")
                    for bg, count in stats["blood_counts"].items():
                        print(f"  {bg} : {count} patients")

                    print(f"\nUnique Blood Groups: {set(stats['blood_counts'].keys())}")
                    print("=" * 35)

                tracker("Stats")

            # ==============================
            # GENERATE REPORT
            # ==============================
            elif choice == "9":
                pid = input("Enter Patient ID: ")
                p = search_patient(pid)

                path = generate_report(p)

                print(f"Report saved at: {path}")
                tracker("Report")

            # ==============================
            # EXPORT CSV
            # ==============================
            elif choice == "10":
                data = load_from_json()
                export_to_csv(data)

                print("CSV Exported Successfully!")
                tracker("CSV Export")

            # ==============================
            # GRAPH
            # ==============================
            elif choice == "11":
                show_graph()
                tracker("Graph")

            # ==============================
            # DOCTOR & DEPARTMENT REPORT
            # ==============================
            elif choice == "12":
                generate_department_report()
                tracker("Department Report")

            # ==============================
            # EXIT
            # ==============================
            elif choice == "0":
                print("👋 Exiting... Bye da!")
                sys.exit()

            else:
                print("Invalid choice")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()