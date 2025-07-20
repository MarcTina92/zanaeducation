import frappe
from datetime import datetime

# Get the latest program enrollments for a student
def get_enrolled_program_for_student(student):
    enrolled_programs = frappe.get_all("Program Enrollment",
    filters={
        "student": student.name,
        "docstatus": 1
    },
    fields = [
            "program",
            "academic_year",
            "academic_term"
        ]
    )
    if isinstance(enrolled_programs, list):
        return enrolled_programs
    return []



# get list of groups names which student is part of.
def get_student_group(student):
    student_groups = frappe.get_all("Student Group Student",
        filters={"student": student.name},
        fields=["parent"]  # parent = Student Group
    )
    return [sg.parent for sg in student_groups]

