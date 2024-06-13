# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Material(Document):

	def on_update(self):
		for a in self.material_stock_location:
			doc = frappe.get_doc("Stock Location Material",a.stock_location_item)
			doc.price = a.price
			doc.cost = a.cost
			doc.qty = a.qty
			doc.save()

	def before_insert(self):
		if self.material_code == "" or self.material_code == None:
			material_category = frappe.get_doc("Material Category",self.material_category)
			if material_category.material_code_prefix and material_category.material_code_digit:
				material_category.current_number += 1
				self.material_code = str(material_category.material_code_prefix) + str(material_category.current_number).zfill(len(material_category.material_code_digit))
				material_category.save()

	def after_insert(self):
		self.generate_stock_location_material(self)


	@frappe.whitelist()	
	def generate_stock_location_material(item,a=None):
		current_stock_location_material = frappe.db.sql("select stock_location from `tabStock Location Material` where material_code='{}'".format(item.name),as_dict=1)
		stock_location = frappe.db.sql("select name from `tabStock Location`",as_dict=1)
		if len(current_stock_location_material) == len(stock_location):
			frappe.throw("Stock Location Material Already Created")
		elif len(current_stock_location_material)<len(stock_location):
			for a in stock_location:
				if not any(a.name in x.stock_location  for x in current_stock_location_material):
					doc = frappe.new_doc("Stock Location Material")
					doc.material_code = item.name
					doc.material_name = item.material_name
					doc.stock_location = a.name
					doc.unit = item.unit
					doc.price = item.price
					doc.cost = item.cost
					doc.qty = 0
					doc.save()
		else:
			for a in stock_location:
				doc = frappe.new_doc("Stock Location Material")
				doc.material_code = item.name
				doc.material_name = item.material_name
				doc.stock_location = a.name
				doc.unit = item.unit
				doc.price = item.price
				doc.cost = item.cost
				doc.qty = 0
				doc.save()

	@frappe.whitelist()
	def get_stock_location_material(item):
		doc = frappe.db.sql("SELECT material_code,stock_location,unit,qty,cost,price,name FROM `tabStock Location Material` WHERE material_code = '{0}'".format(item.name),as_dict=1)
		if doc:
			return doc