import frappe
from frappe import _
from frappe.utils import nowdate
 
def get_context(context):
    user = frappe.session.user
    frappe.log_error(user, "DEBUG User")
 
    student = frappe.get_all("Student", filters={"user": user}, fields=["name", "student_name"])
    frappe.log_error(student, "DEBUG Student Query")
 
    context.no_student_record = True
    if not student:
        return context
    ...
 
 
def get_context(context):
    user = frappe.session.user
 
    # Redirect guests and admin to login
    if user in ("Guest", "Administrator"):
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?redirect-to=/student-portal"
        return {}
 
    # Fetch roles
    roles = frappe.get_roles(user)
 
    # Route based on role
    if "Student" in roles:
        return student_dashboard(context, user)
    elif "Parent" in roles:
        return parent_dashboard(context, user)
    elif "Teacher" in roles:
        return teacher_dashboard(context, user)
    else:
        frappe.log_error(f"User '{user}' has unsupported role for this portal.", "Invalid Role Access")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login"
        return {}
def student_dashboard(context, user):
    context.no_student_record = True
    student = frappe.get_all("Student", filters={"user": user}, fields=["name", "student_name"])
 
    if not student:
        frappe.log_error(f"No student record found for user: {user}", "Student Portal Access")
        return context
 
    student = student[0]
    context.student = student
    context.no_student_record = False
 
    program = frappe.get_all("Program Enrollment", filters={"student": student.name}, fields=["program", "academic_year"])
    context.program_info = program[0] if program else {}
 
    fees = frappe.get_all("Fees", filters={"student": student.name}, fields=["outstanding_amount", "posting_date"])
    if fees:
        context.fee_status = {
            "total_due": fees[0].outstanding_amount,
            "last_payment_date": fees[0].posting_date
        }
 
    student_groups = frappe.get_all("Student Group Student", filters={"student": student.name}, fields=["parent"])
    group_names = [g.parent for g in student_groups]
    courses = frappe.get_all("Student Group", filters={"name": ["in", group_names]}, fields=["course"])
    context.courses = courses
 
    if group_names:
        today = nowdate()
        schedule = frappe.get_all("Course Schedule", filters={
            "student_group": ["in", group_names],
            "schedule_date": today
        }, fields=["course", "from_time", "to_time", "room", "instructor"], order_by="from_time asc")
        context.today_schedule = schedule
 
        homework = frappe.get_all("Assessment Plan", filters={
            "assessment_group": ["in", group_names],
            "schedule_date": [">=", frappe.utils.nowdate()]
        }, fields=["assessment_name", "schedule_date", "course"], order_by="schedule_date asc", limit=5)
        context.homework = homework
 
    return context
 
def parent_dashboard(context, user):
    context.dashboard_type = "Parent"
    context.notice = "Parent dashboard coming soon."
    return context
 
def teacher_dashboard(context, user):
    context.dashboard_type = "Teacher"
    context.notice = "Teacher dashboard coming soon."
    return context
