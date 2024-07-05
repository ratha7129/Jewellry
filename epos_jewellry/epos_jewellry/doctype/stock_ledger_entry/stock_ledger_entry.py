# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import get_info_by_type


class StockLedgerEntry(Document):
	def validate(self):
		config=frappe.get_doc('Company')
		if config.allow_negative_stock:
			update_qty(self)
			update_cost_and_price(self)
		else:
			if get_info_by_type(self.ledger_type,self.item_code,self.stock_location).qty<=0:
				frappe.throw("Item <b>{0}</b> require <b>{1} {2}</b> to complete this transaction".format(self.item_code,abs(self.qty_change),self.unit))
			else:
				update_qty(self)
				update_cost_and_price(self)
def update_qty(self):
	if self.ledger_type == 'Item':
		frappe.db.sql("update `tabStock Location Item` set qty = qty + {0} where item_code = '{1}' and stock_location = '{2}'".format(self.qty_change,self.item_code,self.stock_location))
	elif self.ledger_type == 'Material' :
		frappe.db.sql("update `tabStock Location Material` set qty = qty + {0} where material_code = '{1}' and stock_location = '{2}'".format(self.qty_change,self.item_code,self.stock_location))
	else:
		pass

def update_cost_and_price(self):
	if self.ledger_type == 'Item':
		doc = frappe.db.sql("select cost,price from `tabStock Location Item` where item_code = '{0}' and stock_location = '{1}'".format(self.item_code,self.stock_location),as_dict=1)
		if doc:
			if doc[0].cost != self.cost or doc[0].price != self.price:
				frappe.db.sql("update `tabStock Location Item` set cost = {0}, price = {1} where item_code = '{2}' and stock_location = '{3}'".format(self.cost,self.price,self.item_code,self.stock_location))
	elif self.ledger_type == 'Material' :
		doc = frappe.db.sql("select cost,price from `tabStock Location Material` where material_code = '{0}' and stock_location = '{1}'".format(self.item_code,self.stock_location),as_dict=1)
		if doc:
			if doc[0].cost != self.cost or doc[0].price != self.price:
				frappe.db.sql("update `tabStock Location Material` set cost = {0}, price = {1} where material_code = '{2}' and stock_location = '{3}'".format(self.cost,self.price,self.item_code,self.stock_location))
	else:
		pass