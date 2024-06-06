# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SaleInvoicePayment(Document):
	def on_submit(self):
		doc = frappe.get_doc("Sale Invoice",self.sale_invoice)
		doc.paid_amount = doc.paid_amount + self.payment_amount
		doc.balance = doc.balance - self.payment_amount
		doc.save()
		set_status(doc)

	def on_cancel(self):
		doc = frappe.get_doc("Sale Invoice",self.sale_invoice)
		doc.paid_amount = doc.paid_amount - self.payment_amount
		doc.balance = doc.balance + self.payment_amount
		doc.save()
		set_status(doc)

def set_status(doc):
	if doc.docstatus == 2:
		doc.status = "Cancelled"
	elif doc.docstatus == 1:
		if 0 < doc.balance < doc.total_amount:
			doc.status = "Partly Paid"
		elif doc.balance == doc.total_amount:
			doc.status = "Unpaid"
		elif doc.balance <= 0:
			doc.status = "Paid"
		else:
			doc.status = "Submitted"
	else:
		doc.status = "Draft"
	doc.save()