import frappe

def redirect_based_on_role(login_manager):
    user = frappe.get_doc("User", frappe.session.user)
    roles = [role.role for role in user.roles]

    # Define the redirect route for each role
    role_redirect_map = {
        "Guardian": "/parent-portal",
        "Student": "/student-portal",
        "Instructor": "/teacher-portal"
    }

    # Redirect based on first matched role
    for role, route in role_redirect_map.items():
        if role in roles:
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = route
            break
