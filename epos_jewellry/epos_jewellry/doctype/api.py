import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_item_material(item_code):
    item_material = frappe.db.sql("select material_code,material_name,unit,price,cost,qty from `tabItem Material` where parent = '{}'".format(item_code),as_dict=1)
    return item_material
