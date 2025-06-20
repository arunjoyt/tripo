import frappe
from frappe.utils.password import update_password
import logging
"""
How to run the script?
bench --site <site_name> execute tripo.install.create_initial_data
Make sure to run the script after initial account setup from Frappe UI
"""

def create_initial_data():
    logger = frappe.logger("tripo_setup")
    logger.setLevel(logging.INFO)

    def log(msg):
        logger.info(msg)
        print(msg)  # Still prints to console when run from bench

    # Store name of each created Trip Company
    company_name_map = {}

    for label in ["Uber", "Ola"]:
        company = frappe.db.get_value("Trip Company", {"trip_company_name": label}, "name")
        if not company:
            company_doc = frappe.get_doc({
                "doctype": "Trip Company",
                "trip_company_name": label,
            }).insert()
            company_name_map[label] = company_doc.name
            log(f"Trip Company created: {label}")
        else:
            company_name_map[label] = company
            log(f"Trip Company exists: {label}")

    frappe.db.commit()

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

    all_modules = frappe.get_all("Module Def", pluck="name")
    allowed_module = "Tripo"

    for user in user_list:
        user_created = False

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
            log(f"User created: {user['email']}")
            user_created = True
        else:
            log(f"User exists: {user['email']}")

        # Always update module access
        blocked = [m for m in all_modules if m != allowed_module]
        user_doc = frappe.get_doc("User", user['email'])
        user_doc.set("block_modules", [])

        for module in blocked:
            user_doc.append("block_modules", {
                "module": module
            })

        user_doc.save(ignore_permissions=True)
        log(f"Modules set for {user['email']} (only '{allowed_module}' allowed)")

        trip_company_name = company_name_map.get(user["company_label"])

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
            log(f"User Permission added: {user['email']} → {trip_company_name}")

        if not frappe.db.exists("Trip Company User Mapping", {
            "trip_company": trip_company_name,
            "user": user["email"]
        }):
            frappe.get_doc({
                "doctype": "Trip Company User Mapping",
                "trip_company": trip_company_name,
                "user": user["email"]
            }).insert(ignore_permissions=True)
            log(f"Trip Company Mapping created: {user['email']} → {trip_company_name}")