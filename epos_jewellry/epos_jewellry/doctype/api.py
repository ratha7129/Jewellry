import frappe
from frappe.model.document import Document
import json

@frappe.whitelist()
def get_item_material(item_code):
    item_material = frappe.db.sql("select material_code,material_name,unit,price,cost,qty from `tabItem Material` where parent = '{}'".format(item_code),as_dict=1)
    return item_material

@frappe.whitelist()
def stock_ledger_entry(data):
    doc = frappe.get_doc(data)
    doc.insert()

@frappe.whitelist()
def get_info_by_type(type,name,stock_location):
    if type == "Item":
        doc = frappe.db.sql("select cost,qty,price,unit from `tabStock Location Item` where item_code = '{0}' and stock_location = '{1}'".format(name,stock_location),as_dict=1)
        if not doc:
            doc = frappe.get_doc("Item",name)
            generate_stock_location_item(doc)
            doc = frappe.db.sql("select cost,qty,price,unit from `tabStock Location Item` where item_code = '{0}' and stock_location = '{1}'".format(name,stock_location),as_dict=1)
    else:
        doc = frappe.db.sql("select cost,qty,price,unit from `tabStock Location Material` where material_code = '{0}' and stock_location = '{1}'".format(name,stock_location),as_dict=1)
        if not doc:
            doc = frappe.get_doc("Material",name)
            generate_stock_location_material(doc)
            doc = frappe.db.sql("select cost,qty,price,unit from `tabStock Location Material` where material_code = '{0}' and stock_location = '{1}'".format(name,stock_location),as_dict=1)
    return doc[0] or ""

@frappe.whitelist()	
def generate_stock_location_item(item,is_bulk=0):
    item = json.loads(item)
    current_stock_location_item = frappe.db.sql("select stock_location from `tabStock Location Item` where item_code='{}'".format(item["name"]),as_dict=1)
    stock_location = frappe.db.sql("select name from `tabStock Location`",as_dict=1)
    if len(current_stock_location_item) == len(stock_location) and is_bulk == 0:
        frappe.msgprint("Item {0} Stock Location Item Already Created".format(item["name"]))
    elif len(current_stock_location_item)<len(stock_location) and len(current_stock_location_item)>0:
        for a in stock_location:
            if not any(a.name in x.stock_location  for x in current_stock_location_item):
                doc = frappe.new_doc("Stock Location Item")
                doc.item_code = item["name"]
                doc.item_name = item["item_name_en"]
                doc.stock_location = a.name
                doc.unit = item["unit"]
                doc.price = item["price"]
                doc.cost = item["cost"]
                doc.qty = 0
                doc.save()
        if is_bulk == 0:
            frappe.msgprint("New Stock Location Item Created")
    else:
        for a in stock_location:
            doc = frappe.new_doc("Stock Location Item")
            doc.item_code = item["name"]
            doc.item_name = item["item_name_en"]
            doc.stock_location = a.name
            doc.unit = item["unit"]
            doc.price = item["price"]
            doc.cost = item["cost"]
            doc.qty = 0
            doc.save()
        if is_bulk == 0:
            frappe.msgprint("New Stock Location Item Created")

@frappe.whitelist()
def generate_stock_location_material(item,is_bulk=0):
    item = json.loads(item)
    current_stock_location_material = frappe.db.sql("select stock_location from `tabStock Location Material` where material_code='{}'".format(item["name"]),as_dict=1)
    stock_location = frappe.db.sql("select name from `tabStock Location`",as_dict=1)
    if len(current_stock_location_material) == len(stock_location) and is_bulk == 0:
        frappe.msgprint("Material {0} Stock Location Material Already Created".format(item["name"]))
    elif len(current_stock_location_material)<len(stock_location):
        for a in stock_location:
            if not any(a.name in x.stock_location  for x in current_stock_location_material):
                doc = frappe.new_doc("Stock Location Material")
                doc.material_code = item["name"]
                doc.material_name = item["material_name"]
                doc.stock_location = a.name
                doc.unit = item["unit"]
                doc.price = item["price"]
                doc.cost = item["cost"]
                doc.qty = 0
                doc.save()
        if is_bulk == 0:
            frappe.msgprint("New Stock Location Material Created")
    else:
        for a in stock_location:
            doc = frappe.new_doc("Stock Location Material")
            doc.material_code = item["name"]
            doc.material_name = item["material_name"]
            doc.stock_location = a.name
            doc.unit = item["unit"]
            doc.price = item["price"]
            doc.cost = item["cost"]
            doc.qty = 0
            doc.save()
        if is_bulk == 0:
                frappe.msgprint("New Stock Location Material Created")