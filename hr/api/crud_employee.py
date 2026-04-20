import frappe
from frappe import _


# ==============================
# HELPER FUNCTION
# ==============================
def get_full_name(data):
    return " ".join(filter(None, [
        data.get("first_name"),
        data.get("middle_name"),
        data.get("last_name")
    ]))


def parse_request_data(data):
    """
    Handles multiple input formats:
    1. {"data": {...}}
    2. direct fields
    3. string JSON
    """
    if not data:
        data = frappe.form_dict

    if isinstance(data, str):
        data = frappe.parse_json(data)

    # If wrapped inside "data"
    if isinstance(data, dict) and data.get("data"):
        data = data.get("data")

    return data


# ==============================
# CREATE EMPLOYEE
# ==============================
@frappe.whitelist(allow_guest=True)
def create_employee(data=None):
    data = parse_request_data(data)

    # ✅ Required fields
    if not data.get("employee_id"):
        frappe.throw(_("Employee ID is required"))

    if not data.get("first_name"):
        frappe.throw(_("First Name is required"))

    # ✅ Full Name
    data["full_name"] = get_full_name(data)

    # ✅ Default values
    data.setdefault("employment_status", "Active")
    data.setdefault("employment_type", "Full Time")
    data.setdefault("is_probation_completed", 0)
    data.setdefault("is_notice_period_active", 0)
    data.setdefault("bonus_eligibility", 0)

    try:
        doc = frappe.get_doc({
            "doctype": "Employee",
            **data
        })

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Employee created successfully",
            "data": doc
        }

    except Exception as e:
        frappe.db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }


# ==============================
# GET ALL EMPLOYEES
# ==============================
@frappe.whitelist(allow_guest=True)
def get_employee_list(limit=20, offset=0):
    try:
        employees = frappe.get_all(
            "Employee",
            fields=["*"],
            limit=int(limit),
            start=int(offset)
        )

        return {
            "status": "success",
            "count": len(employees),
            "data": employees
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ==============================
# GET SINGLE EMPLOYEE
# ==============================
@frappe.whitelist(allow_guest=True)
def get_employee(name=None):
    try:
        if not name:
            name = frappe.form_dict.get("name")

        if not name:
            frappe.throw(_("Employee name is required"))

        doc = frappe.get_doc("Employee", name)

        return {
            "status": "success",
            "data": doc
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ==============================
# UPDATE EMPLOYEE
# ==============================
@frappe.whitelist(allow_guest=True)
def update_employee(name=None, data=None):
    try:
        if not name:
            name = frappe.form_dict.get("name")

        if not name:
            frappe.throw(_("Employee name is required"))

        data = parse_request_data(data)

        doc = frappe.get_doc("Employee", name)

        for key, value in data.items():
            doc.set(key, value)

        # ✅ Update full name
        doc.full_name = get_full_name(doc)

        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Employee updated successfully",
            "data": doc
        }

    except Exception as e:
        frappe.db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }


# ==============================
# DELETE EMPLOYEE
# ==============================
@frappe.whitelist(allow_guest=True)
def delete_employee(name=None):
    try:
        if not name:
            name = frappe.form_dict.get("name")

        if not name:
            frappe.throw(_("Employee name is required"))

        frappe.delete_doc("Employee", name, ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Employee deleted successfully"
        }

    except Exception as e:
        frappe.db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }