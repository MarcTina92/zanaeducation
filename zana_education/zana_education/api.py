# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
# from zana_education.zana_education.utils.student_utils import get_enrolled_program_for_student
from zana_education.zana_education.utils.student_utils import get_enrolled_program_for_student, get_student_group

# from frappe import _
# from frappe.email.doctype.email_group.email_group import add_subscribers
# from frappe.model.mapper import get_mapped_doc
# from frappe.utils import cstr, flt, getdate
# from frappe.utils.dateutils import get_dates_from_timegrain
@frappe.whitelist()
def get_zana_student_info():
    student_name = frappe.form_dict.get("student_name")
    email = frappe.session.user
    if email == "Administrator":
        return
    student_info = frappe.get_all(
        "Student",
        fields=["*"],
        filters={"name": student_name},
        ignore_permissions=True 
    )
    # if not student_info:
    #     frappe.throw("Student not found")
    
    student_info = student_info[0]
    current_program = get_current_enrollment(student_info.name)
    
    if current_program:
        student_groups = get_student_groups(student_info.name, current_program.program)
        student_info["student_groups"] = student_groups
        student_info["current_program"] = current_program
    
    return student_info

@frappe.whitelist()
def get_current_enrollment(student, academic_year=None):
    current_academic_year = academic_year or frappe.defaults.get_defaults().academic_year
    if not current_academic_year:
        frappe.throw(_("Please set default Academic Year in Education Settings"))
    program_enrollment_list = frappe.db.sql(
        """
        select
            name as program_enrollment, student_name, program, student_batch_name as student_batch,
            student_category, academic_term, academic_year
        from
            `tabProgram Enrollment`
        where
            student = %s and academic_year = %s
        order by creation""",
        (student, current_academic_year),
        as_dict=1,
    )

    if program_enrollment_list:
        return program_enrollment_list[0]
    else:
        return None

def get_student_groups(student, program_name):

    student_group = frappe.qb.DocType("Student Group")
    student_group_students = frappe.qb.DocType("Student Group Student")

    student_group_query = (
        frappe.qb.from_(student_group)
        .inner_join(student_group_students)
        .on(student_group.name == student_group_students.parent)
        .select((student_group_students.parent).as_("label"))
        .where(student_group_students.student == student)
        .where(student_group.program == program_name)
        .run(as_dict=1)
    )

    return student_group_query


def get_guardian_doc(email):
    guardian = frappe.get_all("Guardian", filters={"user": email}, fields=["name", "guardian_name"])
    if guardian:
        return frappe.get_doc("Guardian", guardian[0].name)
    else:
        return None

def get_student_docs_for_guardian(guardian):
    if guardian is None:
        return []
    parent_doc = frappe.get_all(
        "Student Guardian",
        filters={"guardian": guardian.name},
        fields=["parent"]
    )
    students = []
    for s in parent_doc:
        student_doc = frappe.get_doc("Student", s.parent)
        students.append({
            "name": student_doc.name,
            "student_name": student_doc.student_name,
            "email": student_doc.student_email_id,
            "birth_date": student_doc.date_of_birth or "Not set",
            "image": student_doc.image or "/assets/zana_education/images/default_student.png",
        })
    return students

@frappe.whitelist()
def get_guardian_info():
    user = frappe.session.user
    roles = frappe.get_roles(user)
    user = frappe.get_doc("User", frappe.session.user)
    if "Guardian" not in roles:
        return
    guardian = get_guardian_doc(user.email)
    students = get_student_docs_for_guardian(guardian)
    return {
        "guardian": guardian,
        "students": students
    }


@frappe.whitelist()
def get_course_schedule_for_zana_student():
    student_name = frappe.form_dict.get("student_name")
    student_doc = frappe.get_doc("Student", student_name)
    enrolled_programs = get_enrolled_program_for_student(student_doc)
    unique_enrolled_programs = list(set(item['program'] for item in enrolled_programs))
    student_groups = get_student_group(student_doc)
    schedule = frappe.db.get_list(
        "Course Schedule",
        fields=[
            "schedule_date",
            "room",
            "class_schedule_color",
            "course",
            "from_time",
            "to_time",
            "instructor",
            "title",
            "name",
        ],
        filters={"program": ["in", unique_enrolled_programs], "student_group": ["in", student_groups]},
        ignore_permissions=True,
        order_by="schedule_date asc",
    )
    return schedule


def combine_datetime(date, time):
    if isinstance(date, datetime) and time:
        return date.replace(hour=time.seconds // 3600, minute=(time.seconds // 60) % 60)
    elif date and time:
        return datetime.combine(date, (datetime.min + time).time())
    return ""


@frappe.whitelist()
def get_enrolled_courses_for_student():
    student_name = frappe.form_dict.get("student_name")
    enrolled_courses = frappe.get_all("Course Enrollment",
    filters={
        "student": student_name,
    },
    fields = [
            "course",
        ]
    )
    if isinstance(enrolled_courses, list):
        return enrolled_courses
    return []

