import frappe
from frappe.utils.password import update_password

def create_initial_data():
    # Store name of each created Trip Company
    company_name_map = {}

    for label in ["Uber", "Ola"]:
        # Try to fetch existing company
        company = frappe.db.get_value("Trip Company", {"trip_company_name": label}, "name")
        if not company:
            # Insert new Trip Company and get its name
            company_doc = frappe.get_doc({
                "doctype": "Trip Company",
                "trip_company_name": label,
            }).insert()
            company_name_map[label] = company_doc.name
        else:
            company_name_map[label] = company

    frappe.db.commit()  # Ensure Trip Companies are visible

    # User definitions
    user_list = [
        {
            "email": "olacoordinator@gmail.com",
            "first_name": "Ola Coordinator",
            "roles": ["Trip Coordinator"],
            "company_label": "Ola"
        },
        {
            "email": "olamanager@gmail.com",
            "first_name": "Ola Manager",
            "roles": ["Trip Manager"],
            "company_label": "Ola"
        },
        {
            "email": "ubercoordinator@gmail.com",
            "first_name": "Uber Coordinator",
            "roles": ["Trip Coordinator"],
            "company_label": "Uber"
        },
        {
            "email": "ubermanager@gmail.com",
            "first_name": "Uber Manager",
            "roles": ["Trip Manager"],
            "company_label": "Uber"
        },
    ]

    for user in user_list:
        if not frappe.db.exists("User", {"name": user['email']}):
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": user['email'],
                "first_name": user['first_name'],
                "roles": [{"role": role_name} for role_name in user["roles"]],
                "send_welcome_email": 0
            })
            user_doc.insert(ignore_permissions=True)
            update_password(user_doc.name, user.get("password", "Orange123*"))

        trip_company_name = company_name_map.get(user["company_label"])

        # Create User Permission
        if not frappe.db.exists("User Permission", {
            "user": user["email"],
            "allow": "Trip Company",
            "for_value": trip_company_name
        }):
            frappe.get_doc({
                "doctype": "User Permission",
                "user": user["email"],
                "allow": "Trip Company",
                "for_value": trip_company_name
            }).insert(ignore_permissions=True)

        # Create Trip Company User Mapping
        if not frappe.db.exists("Trip Company User Mapping", {
            "trip_company": trip_company_name,
            "user": user["email"]
        }):
            frappe.get_doc({
                "doctype": "Trip Company User Mapping",
                "trip_company": trip_company_name,
                "user": user["email"]
            }).insert(ignore_permissions=True)