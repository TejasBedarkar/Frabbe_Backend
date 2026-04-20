import frappe
from frappe import _


# ======================
# GET EMPLOYEE LIST
# ======================
@frappe.whitelist(allow_guest=True)
def get_employee_list(limit=20, offset=0, search=None):

    filters = {}

    if search:
        filters["full_name"] = ["like", f"%{search}%"]

    employees = frappe.get_all(
        "Employee",
        filters=filters,
        fields=[
            "name",
            "employee_id",
            "full_name",
            "first_name",
            "last_name",
            "company_email",
            "department",
            "designation",
            "employment_status"
        ],
        limit_start=int(offset),
        limit_page_length=int(limit),
        order_by="modified desc"
    )

    return employees


# ======================
# GET SINGLE EMPLOYEE
# ======================
@frappe.whitelist(allow_guest=True)
def get_employee(id):

    if not frappe.db.exists("Employee", id):
        frappe.throw(_("Employee not found"))

    return frappe.get_doc("Employee", id)


# ======================
# CREATE EMPLOYEE
# ======================
@frappe.whitelist(allow_guest=True)
def create_employee(**data):

    doc = frappe.get_doc({
        "doctype": "Employee",
        **data
    })

    doc.insert(ignore_permissions=True)
    return doc


# ======================
# UPDATE EMPLOYEE
# ======================
@frappe.whitelist(allow_guest=True)
def update_employee(name, **data):

    if not frappe.db.exists("Employee", name):
        frappe.throw(_("Employee not found"))

    doc = frappe.get_doc("Employee", name)

    for key, value in data.items():
        doc.set(key, value)

    doc.save(ignore_permissions=True)

    return doc


# ======================
# DELETE EMPLOYEE
# ======================
@frappe.whitelist(allow_guest=True)
def delete_employee(name):

    if not frappe.db.exists("Employee", name):
        frappe.throw(_("Employee not found"))

    frappe.delete_doc("Employee", name, ignore_permissions=True)

    return {"message": "Employee deleted successfully"}
