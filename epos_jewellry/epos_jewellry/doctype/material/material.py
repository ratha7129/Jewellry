# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import generate_stock_location_material,get_info_by_type
from datetime import datetime
import json

class Material(Document):

	def on_update(self):
		add_stock_reconciliation(self)

	def before_insert(self):
		if self.material_code == "" or self.material_code == None:
			material_category = frappe.get_doc("Material Category",self.material_category)
			if material_category.material_code_prefix and material_category.material_code_digit:
				material_category.current_number += 1
				self.material_code = str(material_category.material_code_prefix) + str(material_category.current_number).zfill(len(material_category.material_code_digit))
				material_category.save()

	def after_insert(self):
		docs = frappe.db.sql("select name,material_name,unit,price,cost from `tabMaterial` where name = '{0}'".format(self.name),as_dict=1)
		generate_stock_location_material(json.dumps(docs[0]))
		self.reload()

	@frappe.whitelist()
	def get_stock_location_material(item):
		doc = frappe.db.sql("SELECT material_code,stock_location,unit,qty,cost,price,name FROM `tabStock Location Material` WHERE material_code = '{0}' order by stock_location".format(item.name),as_dict=1)
		if doc:
			return doc
		
def add_stock_reconciliation(self):
	for item in self.material_stock_location:
		current_qty = get_info_by_type("Material",self.name,item.stock_location).qty
		current_cost = get_info_by_type("Material",self.name,item.stock_location).cost
		current_price = get_info_by_type("Material",self.name,item.stock_location).price
		if current_qty != item.qty or current_cost != item.cost or current_price != item.price:
			parent = frappe.new_doc("Stock Reconciliation")
			parent.posting_date = datetime.today().strftime('%Y-%m-%d')
			parent.type = "Material"
			parent.stock_location = item.stock_location
			parent.append("stock_reconciliation_item",{
			'item_code' : self.name,
			'item_name' : self.material_name,
			'stock_location' : item.stock_location,
			'unit' : item.unit,
			'price' : item.price,
			'cost' : item.cost,
			'qty' : item.qty,
			'current_qty': get_info_by_type("Material",self.name,item.stock_location).qty,
			'current_cost' : get_info_by_type("Material",self.name,item.stock_location).cost})
			parent.docstatus=1
			parent.save()