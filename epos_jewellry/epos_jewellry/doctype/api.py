import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_item_material(item_code):
    item_material = frappe.db.sql("select material_code,material_name,unit,price,cost,qty from `tabItem Material` where parent = '{}'".format(item_code),as_dict=1)
    return item_material

def stock_ledger_entry(data):
    doc = frappe.get_doc(data)
    doc.insert()

def get_item_current_qty(item_code):
    doc = frappe.get_doc('Item',item_code)
    return doc.qty or 0

def get_material_current_qty(material_code):
    doc = frappe.get_doc('Material',material_code)
    return doc.qty or 0