import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_item_material(item_code):
    item_material = frappe.db.sql("select material_code,material_name,unit,price,cost,qty from `tabItem Material` where parent = '{}'".format(item_code),as_dict=1)
    return item_material

def stock_ledger_entry(data):
    doc = frappe.get_doc(data)
    doc.insert()

def get_item_current_qty(item_code,stock_location):
    doc = frappe.db.sql("select qty from `tabStock Location Item` where item_code = '{0}' and stock_location = '{1}'".format(item_code,stock_location),as_dict=1)
    return doc[0].qty or 0

def get_material_current_qty(material_code,stock_location):
    doc = frappe.db.sql("select qty from `tabStock Location Material` where material_code = '{0}' and stock_location = '{1}'".format(material_code,stock_location),as_dict=1)
    return doc[0].qty or 0