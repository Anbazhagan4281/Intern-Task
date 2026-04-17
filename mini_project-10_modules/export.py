import csv
import os
from file_handler import load_data
from utils import calculate_age, calculate_avg, get_status, get_grade
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

CSV_FILE = "students.csv"


def export_to_csv():
    data = load_data()

    if not data:
        print("No data to export")
        return

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID", "Name", "DOB", "Age", "Phone", "Email",
                "Marks", "Average", "Status", "Grade"
            ])


            for s in data:
                dob = s.get("date_of_birth") or s.get("date of birth") or "N/A"
                age = s.get("age") or calculate_age(dob)

                avg = calculate_avg(s["marks"])
                status = get_status(avg)
                grade = get_grade(avg)

                writer.writerow([
                    s["id"],
                    s["name"],
                    dob,
                    age,
                    s.get("phone", ""),
                    s["email"],
                    " ".join(map(str, s["marks"])),
                    round(avg, 2),
                    status,
                    grade
                ])

        print("CSV file created successfully!")

    except Exception as e:
        print("Error exporting CSV:", e)

def generate_report_card_pdf(student):
    filename = f"report_card_{student['id']}.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    dob = student.get("date_of_birth") or student.get("date of birth") or "N/A"
    age = student.get("age") or calculate_age(dob)

    content.append(Paragraph("STUDENT REPORT CARD", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"ID: {student['id']}", styles["Normal"]))
    content.append(Paragraph(f"Name: {student['name']}", styles["Normal"]))
    content.append(Paragraph(f"DOB: {dob}", styles["Normal"]))
    content.append(Paragraph(f"Age: {age}", styles["Normal"]))
    content.append(Paragraph(f"Phone: {student.get('phone','N/A')}", styles["Normal"]))
    content.append(Paragraph(f"Email: {student['email']}", styles["Normal"]))

    content.append(Spacer(1, 10))

    marks = student["marks"]
    avg = calculate_avg(marks)
    status = get_status(avg)
    grade = get_grade(avg)

    content.append(Paragraph("Marks:", styles["Heading3"]))

    for i, m in enumerate(marks, 1):
        content.append(Paragraph(f"Subject {i}: {m}", styles["Normal"]))

    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Average: {avg:.2f}", styles["Normal"]))
    content.append(Paragraph(f"Status: {status}", styles["Normal"]))
    content.append(Paragraph(f"Grade: {grade}", styles["Normal"]))

    doc.build(content)

    print(f"PDF Generated: {filename}")