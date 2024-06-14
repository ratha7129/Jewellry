# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_info_by_type

class SaleInvoice(Document):
	def on_update(self):
		self.sub_total = self.price
		self.total_amount = self.sub_total - self.discount_amount
		self.total_cost = self.cost
		self.total_profit = self.total_amount - self.total_cost
		self.balance = self.total_amount - self.paid_amount
		self.set_status()

	def on_submit(self):
		self.set_status()
		add_item_stock_ledger_entry(self)
		for a in self.sale_invoice_item_material:
			add_material_stock_ledger_entry(self,a)

	def on_cancel(self):
		self.set_status()
		add_item_stock_ledger_entry(self)
		for a in self.sale_invoice_item_material:
			add_material_stock_ledger_entry(self,a)
		
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


def add_item_stock_ledger_entry(self):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Sale Invoice",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': self.item,
					'unit':self.unit,
					'price':self.price,
					'cost':self.cost,
					'current_qty': get_info_by_type("Item",self.item,self.stock_location).qty,
					'qty_change':-1,
					'qty_after_transaction': get_info_by_type("Item",self.item,self.stock_location).qty-1,
					'stock_location':self.stock_location,
					'note':"New Sale Invoice {}".format(self.name)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Sale Invoice",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': self.item,
					'unit':self.unit,
					'price':self.price,
					'cost':self.cost,
					'current_qty': get_info_by_type("Item",self.item,self.stock_location).qty,
					'qty_change':1,
					'qty_after_transaction': get_info_by_type("Item",self.item,self.stock_location).qty+1,
					'stock_location':self.stock_location,
					'note':"Cancelled Sale Invoice {}".format(self.name)
				})


def add_material_stock_ledger_entry(self,material):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Sale Invoice",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': material.material_code,
					'unit': material.unit,
					'price': material.price,
					'cost': material.cost,
					'current_qty': get_info_by_type("Material",material.material_code,self.stock_location).qty,
					'qty_change':-1,
					'qty_after_transaction': get_info_by_type("Material",material.material_code,self.stock_location).qty-1,
					'stock_location':self.stock_location,
					'note':"New Sale Invoice {}".format(self.name)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Sale Invoice",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': material.material_code,
					'unit':material.unit,
					'price':material.price,
					'cost':material.cost,
					'current_qty': get_info_by_type("Material",material.material_code,self.stock_location).qty,
					'qty_change':1,
					'qty_after_transaction': get_info_by_type("Material",material.material_code,self.stock_location).qty+1,
					'stock_location':self.stock_location,
					'note':"Cancelled Sale Invoice {}".format(self.name)
				})