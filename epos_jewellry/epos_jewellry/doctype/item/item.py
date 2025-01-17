# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import generate_stock_location_item,get_info_by_type
from datetime import datetime
import json

class Item(Document):
	def on_update(self):
		add_stock_reconciliation(self)

	def before_save(self):
		if self.cost == 0:
			self.cost = sum(item.total_cost or 0 for item in self.item_material)
		if self.price == 0:
			self.price = sum(item.total_amount or 0 for item in self.item_material)
	
	def before_insert(self):
		if self.item_code == "" or self.item_code == None:
			item_category = frappe.get_doc("Item Category",self.item_category)
			if item_category.item_code_prefix and item_category.item_code_digit:
				item_category.current_number += 1
				self.item_code = str(item_category.item_code_prefix) + str(item_category.current_number).zfill(len(item_category.item_code_digit))
				item_category.save()
				
	def after_insert(self):
		docs = frappe.db.sql("select name,item_name_en,unit,price,cost from `tabItem` where name = '{0}'".format(self.name),as_dict=1)
		generate_stock_location_item(json.dumps(docs[0]))
		self.reload()
	
	def validate(self):
		if self.no_material == 0 and len(self.item_material) == 0:
			frappe.throw("Item require at least 1 material")
	
	@frappe.whitelist()
	def get_stock_location_item(item):
		doc = frappe.db.sql("SELECT item_code,stock_location,unit,qty,cost,price,name FROM `tabStock Location Item` WHERE item_code = '{0}' order by stock_location".format(item.name),as_dict=1)
		if doc:
			return doc

def add_stock_reconciliation(self):
	for item in self.item_stock_location:
		current = get_info_by_type("Item",self.name,item.stock_location)
		if current.qty != item.qty or current.cost != item.cost or current.price != item.price:
			parent = frappe.new_doc("Stock Reconciliation")
			parent.posting_date = datetime.today().strftime('%Y-%m-%d')
			parent.type = "Item"
			parent.stock_location = item.stock_location
			parent.append("stock_reconciliation_item",{
			'item_code' : self.name,
			'item_name' : self.item_name_en,
			'stock_location' : item.stock_location,
			'unit' : item.unit,
			'price' : item.price,
			'cost' : item.cost,
			'qty' : item.qty,
			'current_qty': current.qty,
			'current_cost' : current.cost})
			parent.docstatus = 1
			parent.save()