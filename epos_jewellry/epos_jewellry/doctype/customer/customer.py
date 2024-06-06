# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Customer(Document):
	def before_insert(self):
		if self.customer_code == "" or self.customer_code == None:
			customer_group = frappe.get_doc("Customer Group",self.customer_group)
			customer_group.current_number += 1
			self.customer_code = str(customer_group.customer_code_prefix) + str(customer_group.current_number).zfill(len(customer_group.customer_code_digit))
			customer_group.save()
