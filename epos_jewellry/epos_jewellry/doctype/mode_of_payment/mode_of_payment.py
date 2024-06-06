# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ModeOfPayment(Document):
	@frappe.whitelist()
	def get_currency_exchange_rate(self):
		main_currency = frappe.get_doc("Company").currency
		exchange_rate = frappe.db.sql("select * from `tabCurrency Exchange Rate` where from_currency = '{0}' and to_currency='{1}'".format(main_currency,self.currency),as_dict=1)
		return exchange_rate[0].exchange_rate
