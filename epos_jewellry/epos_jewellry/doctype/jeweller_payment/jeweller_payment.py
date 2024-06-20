# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JewellerPayment(Document):

	def validate(self):
		for a in self.jeweller_payment_process:
			p = frappe.get_doc("Jewellry Processing",a.processing)
			a.total_fee =  p.balance
			a.balance = a.total_fee - a.total_payment
			if p.balance <= 0:
				frappe.throw("Process {0} already paid".format(p.name))
			if a.total_payment > p.balance:
				a.input_amount =  p.balance * self.exchange_rate
				a.total_payment =  p.balance
				a.balance = 0


	def on_submit(self):
		doc = frappe.get_doc("Jeweller",self.jeweller)
		doc.total_paid = doc.total_paid + self.total_payment
		doc.balance = doc.total_fee - doc.total_paid
		doc.save()

		for a in self.jeweller_payment_process:
			p = frappe.get_doc("Jewellry Processing",a.processing)
			p.total_payment = p.total_payment + a.total_payment
			p.balance = p.total_fee - p.total_payment
			p.save()

	def on_cancel(self):
		doc = frappe.get_doc("Jeweller",self.jeweller)
		doc.total_paid = doc.total_paid - self.total_payment
		doc.balance = doc.balance + self.total_payment
		doc.save()

		for a in self.jeweller_payment_process:
			p = frappe.get_doc("Jewellry Processing",a.processing)
			p.total_payment = p.total_payment - a.total_payment
			p.balance = p.balance + a.total_payment
			p.save()

	@frappe.whitelist()
	def get_jeweller_processing(self):
		docs = frappe.db.sql("select name,total_fee,balance,total_payment from `tabJewellry Processing` where jeweller = '{0}' and docstatus=1 and balance > 0".format(self.jeweller),as_dict=1)
		if docs:
			return docs
		else:
			frappe.throw("No record")
		return docs
	
@frappe.whitelist()
def get_jeweller_processing_by_name(name):
	doc = frappe.get_doc("Jewellry Processing",name)
	return doc
