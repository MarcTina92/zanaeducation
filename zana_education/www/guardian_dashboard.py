import frappe
from datetime import datetime

logger = frappe.logger("your_module_name", allow_site=True)

def combine_datetime(date, time):
    if isinstance(date, datetime) and time:
        return date.replace(hour=time.seconds // 3600, minute=(time.seconds // 60) % 60)
    elif date and time:
        return datetime.combine(date, (datetime.min + time).time())
    return ""

def get_guardian_doc(email):
    guardian = frappe.get_all("Guardian", filters={"user": email}, fields=["name", "guardian_name"])
    if guardian:
        return frappe.get_doc("Guardian", guardian[0].name)
    else:
        return None



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

def get_enrolled_courses_for_student(student):
    enrolled_courses = frappe.get_all("Course Enrollment",
    filters={
        "student": student.name,
    },
    fields = [
            "course",
        ]
    )
    if isinstance(enrolled_courses, list):
        return enrolled_courses
    return []


# Get Sales invoices for student
def get_sumitted_invoices_for_student(student):
    invoices = frappe.get_all("Sales Invoice",
    filters={
        "student": student.name,
        # docstatus: 1 means submited invoices
        "docstatus": 1
    },
    fields = [
            "outstanding_amount",
        ]
    )
    if isinstance(invoices, list):
        return invoices
    return []


# Get Sales invoices for student
def get_payment_history_for_student(student):
    payments = frappe.get_all(
        "Payment Entry",
        filters={"party_type": "Customer", "party": student.customer, "docstatus": 1},
        fields=[ "posting_date", "paid_amount"]
    )
    if isinstance(payments, list):
        return payments
    return []



def get_student_group(student):
    return frappe.get_all("Student Group Student",
        filters={"student": student.name},
        fields=["parent"]  # parent = Student Group
    )


def get_course_schedule(student):
    student_groups = get_student_group(student)
    group_ids = [sg.parent for sg in student_groups]

    if not group_ids:
        return []

    course_schedules = frappe.get_all("Course Schedule",
        filters={"student_group": ["in", group_ids]},
        fields=[
            "name", "course", "student_group", "from_time", "to_time", "room", "instructor", "schedule_date"
        ],
        order_by="from_time asc"
    )

    # Convert to calendar-friendly format
    courses = []
    for cs in course_schedules:
        start_dt = combine_datetime(cs.schedule_date, cs.from_time)
        end_dt = combine_datetime(cs.schedule_date, cs.to_time)
        courses.append({
            "title": f"{cs.course} ({cs.student_group})",
            "start": start_dt.isoformat() if start_dt else "",
            "end": end_dt.isoformat() if end_dt else "",
            "id": cs.name,
            "extendedProps": {
                "instructor": cs.instructor,
                "room": cs.room
            }
        })

    return courses


def get_context(context):
    # check if loggedin user is a Guardian
    user = frappe.session.user
    roles = frappe.get_roles(user)
    user = frappe.get_doc("User", frappe.session.user)
    if "Guardian" not in roles:
        return
    
    
    email = user.email
    # Load guardian data
    guardian = get_guardian_doc(email)
    context.guardian = guardian
    #  get students associated with the guardian
    parent_doc = frappe.get_all(
        "Student Guardian",
        filters={"guardian": guardian.name},
        fields=["parent"]
    )
    
    students = []
    for s in parent_doc:
        student_doc = frappe.get_doc("Student", s.parent)
        programs = get_enrolled_program_for_student(student_doc)
        courses = get_enrolled_courses_for_student(student_doc)
        invoices = get_sumitted_invoices_for_student(student_doc)
        payments = get_payment_history_for_student(student_doc)
        courses_calendar = get_course_schedule(student_doc)
        
        # attendance = frappe.db.get_value("Attendance", {"student": s.student}, ["count(name)"])
        # grades = frappe.db.get_value("Student Grade", {"student": s.student}, ["gpa"])
        students.append({
            "name": student_doc.student_name,
            "email": student_doc.student_email_id,
            "birth_date": student_doc.date_of_birth or "Not set",
            "image": student_doc.image or "/assets/zana_education/images/default_student.png",
            "programs": programs,
            "courses": courses,
            "outstanding_amount": sum([invoice.outstanding_amount for invoice in invoices]),
            "payments": payments,
            "courses_calendar": courses_calendar,
        })

    context.students = students
    print(f"Courses Calendar: {context.students[0]}")
    return context

