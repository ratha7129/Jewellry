# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import generate_stock_location_material,generate_stock_location_item
import json

class StockLocation(Document):
	def after_insert(self):
		self.generate_stock_location_material_and_item(self)
	
	@frappe.whitelist(allow_guest=1)
	def generate_stock_location_material_and_item(self,a=None):
		items = frappe.db.sql("select count(name) count from `tabItem` where disabled = 0",as_dict=1)
		if items[0].count >= 100:
			frappe.enqueue("epos_jewellry.epos_jewellry.doctype.stock_location.stock_location.queue_generate_stock_location_item")
		else:
			queue_generate_stock_location_item()
		
		materials = frappe.db.sql("select count(name) count from `tabMaterial` where disabled = 0",as_dict=1)
		if materials[0].count >= 100:
			frappe.enqueue("epos_jewellry.epos_jewellry.doctype.stock_location.stock_location.queue_generate_stock_location_material")
			frappe.msgprint("Update In Background")
		else:
			queue_generate_stock_location_material()

@frappe.whitelist(allow_guest=1)
def queue_generate_stock_location_item():
	docs = frappe.db.sql("select name,item_name_en,unit,price,cost from `tabItem` where disabled = 0",as_dict=1)
	for a in docs:
		generate_stock_location_item(json.dumps(a))

@frappe.whitelist(allow_guest=1)
def queue_generate_stock_location_material():
	docs = frappe.db.sql("select name,material_name,unit,price,cost from `tabMaterial` where disabled = 0",as_dict=1)
	for a in docs:
		generate_stock_location_material(json.dumps(a))