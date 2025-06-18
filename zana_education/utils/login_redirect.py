# import frappe
# from frappe.utils.redirect import get_url

# def login_redirect(login_manager):
#     user = frappe.get_doc("User", frappe.session.user)
#     roles = frappe.get_roles(user.name)

#     if "Student" in roles:
#         frappe.local.response["home_page"] = "/student-dashboard"
#     elif "Guardian" in roles:
#         frappe.local.response["home_page"] = "/guardian-dashboard"
#     elif "Instructor" in roles:
#         frappe.local.response["home_page"] = "/teacher-dashboard"
