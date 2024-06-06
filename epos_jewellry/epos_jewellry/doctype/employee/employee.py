# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Employee(Document):
	def before_insert(self):
		if self.employee_code == "" or self.employee_code == None:
			employee_group = frappe.get_doc("Employee Group",self.employee_group)
			employee_group.current_number += 1
			self.employee_code = str(employee_group.employee_code_prefix) + str(employee_group.current_number).zfill(len(employee_group.employee_code_digit))
			employee_group.save()
