# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Material(Document):
	def before_insert(self):
		if self.material_code == "" or self.material_code == None:
			material_category = frappe.get_doc("Material Category",self.material_category)
			if material_category.material_code_prefix and material_category.material_code_digit:
				material_category.current_number += 1
				self.material_code = str(material_category.material_code_prefix) + str(material_category.current_number).zfill(len(material_category.material_code_digit))
				material_category.save()
