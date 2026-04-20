import frappe
from frappe.model.document import Document
from frappe import _


# ======================
# DOC TYPE CONTROLLER
# ======================
class Employee(Document):

    def before_save(self):
        self.set_full_name()
        self.validate_fields()

    def set_full_name(self):
        """Auto generate full name"""
        names = [self.first_name, self.middle_name, self.last_name]
        self.full_name = " ".join([n for n in names if n])

    def validate_fields(self):
        """Basic validations"""

        if self.personal_email and "@" not in self.personal_email:
            frappe.throw(_("Invalid Personal Email"))

        if self.personal_phone and len(self.personal_phone) != 10:
            frappe.throw(_("Phone number must be 10 digits"))

        if self.pan_number and len(self.pan_number) != 10:
            frappe.throw(_("PAN must be 10 characters"))


# ======================
# API SECTION (FOR REACT)
# ======================

# ✅ 1. GET LIST (with pagination + search)
@frappe.whitelist()
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


# ✅ 2. GET SINGLE EMPLOYEE
@frappe.whitelist()
def get_employee(name):

    if not frappe.db.exists("Employee", name):
        frappe.throw(_("Employee not found"))

    return frappe.get_doc("Employee", name)


# ✅ 3. CREATE EMPLOYEE
@frappe.whitelist()
def create_employee(data):

    if isinstance(data, str):
        import json
        data = json.loads(data)

    doc = frappe.get_doc({
        "doctype": "Employee",
        **data
    })

    doc.insert(ignore_permissions=True)
    return doc


# ✅ 4. UPDATE EMPLOYEE
@frappe.whitelist()
def update_employee(name, data):

    if isinstance(data, str):
        import json
        data = json.loads(data)

    doc = frappe.get_doc("Employee", name)

    for key, value in data.items():
        doc.set(key, value)

    doc.save(ignore_permissions=True)
    return doc


# ✅ 5. DELETE EMPLOYEE
@frappe.whitelist()
def delete_employee(name):

    if not frappe.db.exists("Employee", name):
        frappe.throw(_("Employee not found"))

    frappe.delete_doc("Employee", name, ignore_permissions=True)

    return {"message": "Employee deleted successfully"}


# ✅ 6. ADVANCED FILTER API
@frappe.whitelist()
def filter_employees(filters=None):

    if isinstance(filters, str):
        import json
        filters = json.loads(filters)

    return frappe.get_all(
        "Employee",
        filters=filters or {},
        fields=["*"],
        order_by="modified desc"
    )