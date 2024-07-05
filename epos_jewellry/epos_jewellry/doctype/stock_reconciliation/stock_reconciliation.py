# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_info_by_type

class StockReconciliation(Document):
	def validate(self):
		self.total_qty_change = sum(a.qty - a.current_qty for a in self.stock_reconciliation_item)
		self.total_amount_change = sum((a.cost * a.qty) - (a.current_cost * a.current_qty) for a in self.stock_reconciliation_item)

	def on_submit(self):
		if self.type == "Item":
			for a in self.stock_reconciliation_item:
				add_item_stock_ledger_entry(self,a)
		else:
			for a in self.stock_reconciliation_item:
				add_material_stock_ledger_entry(self,a)

	def on_cancel(self):
		if self.type == "Item":
			for a in self.stock_reconciliation_item:
				add_item_stock_ledger_entry(self,a)
		else:
			for a in self.stock_reconciliation_item:
				add_material_stock_ledger_entry(self,a)

def add_item_stock_ledger_entry(self,item):
		current = get_info_by_type("Item",item.item_code,self.stock_location)
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock Reconciliation",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': current.qty,
					'qty_change': item.qty - current.qty,
					'qty_after_transaction': item.qty,
					'stock_location': self.stock_location,
					'note':"New Stock Reconciliation {0}".format(self.name)
				})

def add_material_stock_ledger_entry(self,item):
		current = get_info_by_type("Material",item.item_code,self.stock_location)
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock Reconciliation",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.item_code,
					'unit': item.unit,
					'price': item.price,
					'cost': item.cost,
					'current_qty': current.qty,
					'qty_change': item.qty - current.qty,
					'qty_after_transaction': item.qty,
					'stock_location': self.stock_location,
					'note':"New Stock Reconciliation {0}".format(self.name)
				})