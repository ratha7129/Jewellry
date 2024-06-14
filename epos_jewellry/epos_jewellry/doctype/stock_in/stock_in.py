# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_info_by_type

class StockIn(Document):
	def on_submit(self):
		if self.type == "Item":
			for a in self.stock_in_item:
				add_item_stock_ledger_entry(self,a)
		else:
			for a in self.stock_in_item:
				add_material_stock_ledger_entry(self,a)
	def on_cancel(self):
		if self.type == "Item":
			for a in self.stock_in_item:
				add_item_stock_ledger_entry(self,a)
		else:
			for a in self.stock_in_item:
				add_material_stock_ledger_entry(self,a)

@frappe.whitelist()
def get_name_by_type(type,name):
	if type == "Item":
		doc = frappe.get_doc("Item",name)
		return doc.item_name_en or ""
	else:
		doc = frappe.get_doc("Material",name)
		return doc.material_name or ""

def add_item_stock_ledger_entry(self,item):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Item",item.item_code,self.stock_location).qty,
					'qty_change':item.qty,
					'qty_after_transaction': get_info_by_type("Item",item.item_code,self.stock_location).qty + item.qty,
					'stock_location':self.stock_location,
					'note':"New Stock In {}".format(self.name)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Item",item.item_code,self.stock_location).qty,
					'qty_change':item.qty*-1,
					'qty_after_transaction': get_info_by_type("Item",item.item_code,self.stock_location).qty - item.qty,
					'stock_location':self.stock_location,
					'note':"Cancelled Stock In {}".format(self.name)
				})


def add_material_stock_ledger_entry(self,item):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.item_code,
					'unit': item.unit,
					'price': item.price,
					'cost': item.cost,
					'current_qty': get_info_by_type("Material",item.item_code,self.stock_location).qty,
					'qty_change':item.qty,
					'qty_after_transaction': get_info_by_type("Material",item.item_code,self.stock_location).qty + item.qty,
					'stock_location':self.stock_location,
					'note':"New Stock In {}".format(self.name)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock In",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Material",item.item_code,self.stock_location).qty,
					'qty_change':item.qty*-1,
					'qty_after_transaction': get_info_by_type("Material",item.item_code,self.stock_location).qty - item.qty,
					'stock_location':self.stock_location,
					'note':"Cancelled Stock In {}".format(self.name)
				})