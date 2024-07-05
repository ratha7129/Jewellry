# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_info_by_type

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
	current = get_info_by_type("Item",self.item,self.stock_location)
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
					'current_qty':current.qty,
					'qty_change':1,
					'qty_after_transaction': current.qty + 1,
					'stock_location': self.stock_location,
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
					'current_qty': current.qty,
					'qty_change':-1,
					'qty_after_transaction': current.qty - 1,
					'stock_location': self.stock_location,
					'note':"Cancelled Buy In {}".format(self.name)
				})


def add_material_stock_ledger_entry(self,material):
	current = get_info_by_type("Material",self.item,self.stock_location)
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
					'current_qty': current.qty,
					'qty_change':material.qty,
					'qty_after_transaction': current.qty + material.qty,
					'stock_location': self.stock_location,
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
					'current_qty': current.qty,
					'qty_change':material.qty*-1,
					'qty_after_transaction': current.qty + (material.qty*-1),
					'stock_location': self.stock_location,
					'note':"Cancelled Buy In {}".format(self.name)
				})