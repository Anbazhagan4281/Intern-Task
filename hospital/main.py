# main.py

import sys

# Patient Service imports
from services.patient_service import (
    add_patient,
    view_all_patients,
    search_patient,
    update_patient,
    delete_patient,
    add_prescription,
    get_statistics
)

# Report Service imports
from services.report_service import (
    load_from_json,
    export_to_csv,
    generate_report
)

# Utils
from utils.helpers import session_tracker


def main():
    tracker = session_tracker()

    while True:
        print("\n PATIENT MANAGEMENT SYSTEM")

        
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Add Prescription")
        print("7. View Statistics")
        print("8. Generate Report")
        print("9. Export CSV")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                name = input("Name: ")
                age = int(input("Age: "))
                bg = input("Blood Group: ").upper()
                contact = input("Contact: ")

                p = add_patient(name, age, bg, contact)
                print(f" Added! ID: {p.patient_id}")
                tracker("Add Patient")

            elif choice == "2":
                view_all_patients()
                tracker("View All")

            elif choice == "3":
                pid = input("Enter ID: ")
                p = search_patient(pid)
                print(p)
                tracker("Search")

            elif choice == "4":
                pid = input("Enter ID: ")
                name = input("New Name: ")
                update_patient(pid, name=name)
                print("Updated!")
                tracker("Update")

            elif choice == "5":
                pid = input("Enter ID: ")
                delete_patient(pid)
                print("Deleted!")
                tracker("Delete")

            elif choice == "6":
                pid = input("ID: ")
                med = input("Medicine: ")
                dos = input("Dosage: ")
                days = int(input("Days: "))
                add_prescription(pid, med, dos, days)
                print("Prescription Added!")
                tracker("Prescription")

            elif choice == "7":
                stats = get_statistics()

                if not stats:
                 print("No data available")
                else:
                 print("\n Hospital Statistics")
                 print("=" * 30)

                 print(f"Total Patients     : {stats['total']}")
                 print(f"Average Age        : {stats['average']}")
                 print(f"Youngest           : {stats['youngest']}")
                 print(f"Oldest             : {stats['oldest']}")

                 print("\nBlood Group Counts:")
                for bg, count in stats["blood_counts"].items():
                    print(f"  {bg}  : {count} patients")

                print(f"\nUnique Blood Groups: {stats['unique']}")
                print("=" * 30)

                tracker("Stats")

            elif choice == "8":
                pid = input("Enter ID: ")
                p = search_patient(pid)
                path = generate_report(p)
                print(f"Report saved at {path}")
                tracker("Report")

            elif choice == "9":
                data = load_from_json()
                export_to_csv(data)
                print("CSV Exported!")
                tracker("CSV Export")

            elif choice == "0":
                print("Exiting...")
                sys.exit()

            else:
                print("Invalid choice")

        except Exception as e:
            print(f" Error: {e}")


if __name__ == "__main__":
    main()