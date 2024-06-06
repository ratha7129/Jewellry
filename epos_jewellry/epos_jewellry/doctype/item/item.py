# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Item(Document):
	def before_save(self):
		if self.cost == 0:
			self.cost = sum(item.total_cost for item in self.item_material)
		if self.price == 0:
			self.price = sum(item.total_amount for item in self.item_material)
	
	def before_insert(self):
		if self.item_code == "" or self.item_code == None:
			item_category = frappe.get_doc("Item Category",self.item_category)
			item_category.current_number += 1
			self.item_code = str(item_category.item_code_prefix) + str(item_category.current_number).zfill(len(item_category.item_code_digit))
			item_category.save()

