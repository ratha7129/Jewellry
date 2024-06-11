# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_item_current_qty,get_material_current_qty

class BuyIn(Document):
	def on_submit(self):
		doc = frappe.get_doc("Sale Invoice",self.sale_invoice)
		doc.status = "Buy Back"
		doc.buy_in_no = self.name
		doc.save()

		add_item_stock_ledger_entry(self)
		for a in self.buy_in_material:
			add_material_stock_ledger_entry(self,a)

	def on_cancel(self):
		doc = frappe.get_doc("Sale Invoice",self.sale_invoice)
		set_status(doc)

		add_item_stock_ledger_entry(self)
		for a in self.buy_in_material:
			add_material_stock_ledger_entry(self,a)
	
	@frappe.whitelist()
	def get_sale_invoice_for_buy_in(doc):
		sale_invoice = frappe.get_doc("Sale Invoice",doc.sale_invoice)
		return sale_invoice

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

def add_item_stock_ledger_entry(self):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Buy In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': self.item,
					'unit':self.unit,
					'price':self.price,
					'cost':self.cost,
					'current_qty': get_item_current_qty(self.item),
					'qty_change':1,
					'qty_after_transaction': get_item_current_qty(self.item)+1,
					'note':"New Buy In {}".format(self.name)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Buy In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': self.item,
					'unit':self.unit,
					'price':self.price,
					'cost':self.cost,
					'current_qty': get_item_current_qty(self.item),
					'qty_change':-1,
					'qty_after_transaction': get_item_current_qty(self.item)-1,
					'note':"Cancelled Buy In {}".format(self.name)
				})


def add_material_stock_ledger_entry(self,material):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Buy In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': material.material_code,
					'unit': material.unit,
					'price': material.price,
					'cost': material.cost,
					'current_qty': get_material_current_qty(material.material_code),
					'qty_change':1,
					'qty_after_transaction': get_material_current_qty(material.material_code)+1,
					'note':"New Buy In {}".format(self.name)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Buy In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': material.material_code,
					'unit':material.unit,
					'price':material.price,
					'cost':material.cost,
					'current_qty': get_material_current_qty(material.material_code),
					'qty_change':-1,
					'qty_after_transaction': get_material_current_qty(material.material_code)-1,
					'note':"Cancelled Buy In {}".format(self.name)
				})