# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import get_item_current_qty


class StockLedgerEntry(Document):
	def validate(self):
		config=frappe.get_doc('Company')
		if config.allow_negative_stock:
			update_qty(self)
		else:
			if get_item_current_qty(self.item_code)<=0:
				frappe.throw("Item <b>{0}</b> require <b>{1} {2}</b> to complete this transaction".format(self.item_code,abs(self.qty_change),self.unit))
			else:
				update_qty(self)
def update_qty(self):
	if self.ledger_type == 'Item':
		doc = frappe.get_doc('Item',self.item_code)
		doc.qty = doc.qty + self.qty_change
		doc.save()
	elif self.ledger_type == 'Material' :
		doc = frappe.get_doc('Material',self.item_code)
		doc.qty = doc.qty + self.qty_change
		doc.save()
	else:
		pass