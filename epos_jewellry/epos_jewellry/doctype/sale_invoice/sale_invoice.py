# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SaleInvoice(Document):
	def on_update(self):
		self.sub_total = self.price
		self.total_amount = self.sub_total - self.discount_amount
		self.total_cost = self.cost
		self.total_profit = self.total_amount - self.total_cost
		self.balance = self.total_amount - self.paid_amount
		self.set_status()
	def before_submit(self):
		self.set_status()
	def after_cancel(self):
		self.set_status()

	def set_status(self, update=False, status=None, update_modified=True):
		if self.docstatus == 2:
			self.status = "Cancelled"
		elif self.docstatus == 1:
			if 0 < self.balance < self.total_amount:
				self.status = "Partly Paid"
			elif self.balance == self.total_amount:
				self.status = "Unpaid"
			elif self.balance <= 0:
				self.status = "Paid"
			else:
				self.status = "Submitted"
		else:
			self.status = "Draft"
		self.db_set("status", self.status, update_modified=update_modified)