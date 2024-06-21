# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_info_by_type

class JewellryProcessing(Document):
	def on_submit(self):
		for a in self.processing_out_material:
			add_material_stock_ledger_entry(self,a,"Stock Take",self.stock_location)
		for a in self.processing_leftover_material:
			add_material_stock_ledger_entry(self,a,"Stock In",self.stock_location)
		for a in self.processing_item:
			add_item_stock_ledger_entry(self,a,"Stock In",self.stock_location)
			if self.stock_in_material == 1:
						doc = frappe.db.sql("select material_code item_code,unit,price,cost,qty from `tabItem Material` where parent = '{0}'".format(a.item_code),as_dict=1)
						for b in doc:
							b.qty = b.qty * a.qty
							add_material_stock_ledger_entry(self,b,"Stock In",self.stock_location)
		
		doc = frappe.get_doc("Jeweller",self.jeweller)
		doc.total_fee = doc.total_fee + self.total_fee
		doc.balance = doc.total_fee - doc.total_paid
		doc.save()


	def on_cancel(self):
		for a in self.processing_out_material:
			add_material_stock_ledger_entry(self,a,"Stock Take",self.stock_location)
		for a in self.processing_leftover_material:
			add_material_stock_ledger_entry(self,a,"Stock In",self.stock_location)
		for a in self.processing_item:
			add_item_stock_ledger_entry(self,a,"Stock In",self.stock_location)

		doc = frappe.get_doc("Jeweller",self.jeweller)
		doc.total_fee = doc.total_fee - self.total_fee
		doc.balance = doc.total_fee + doc.total_paid
		doc.save()


def add_item_stock_ledger_entry(self,item,stock_entry_type,stock_location):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Jewellry Processing",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Item",item.item_code,stock_location).qty,
					'qty_change': item.qty if stock_entry_type == "Stock In" else item.qty * -1,
					'qty_after_transaction': get_info_by_type("Item",item.item_code,stock_location).qty + (item.qty if stock_entry_type == "Stock In" else item.qty * -1),
					'stock_location': stock_location,
					'note':"New Stock Entry {0} Type {1}".format(self.name,stock_entry_type)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Jewellry Processing",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Item',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Item",item.item_code,stock_location).qty,
					'qty_change':item.qty*-1 if stock_entry_type == "Stock In" else item.qty,
					'qty_after_transaction': get_info_by_type("Item",item.item_code,stock_location).qty + (item.qty*-1 if stock_entry_type == "Stock In" else item.qty),
					'stock_location': stock_location,
					'note':"Cancelled Stock Entry {0} Type {1}".format(self.name,stock_entry_type)
				})


def add_material_stock_ledger_entry(self,item,stock_entry_type,stock_location):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Jewellry Processing",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.material_code,
					'unit': item.unit,
					'price': item.price,
					'cost': item.cost,
					'current_qty': get_info_by_type("Material",item.material_code,stock_location).qty,
					'qty_change': item.qty if stock_entry_type == "Stock In" else item.qty*-1,
					'qty_after_transaction': get_info_by_type("Material",item.material_code,stock_location).qty + (item.qty if stock_entry_type == "Stock In" else item.qty*-1),
					'stock_location': stock_location,
					'note':"New Stock Entry {0} Type {1}".format(self.name,stock_entry_type)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Jewellry Processing",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.material_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Material",item.material_code,stock_location).qty,
					'qty_change': item.qty*-1 if stock_entry_type == "Stock In" else item.qty,
					'qty_after_transaction': get_info_by_type("Material",item.material_code,stock_location).qty + (item.qty*-1 if stock_entry_type == "Stock In" else item.qty),
					'stock_location': stock_location,
					'note':"Cancelled Stock Entry {0} Type {1}".format(self.name,stock_entry_type)
				})

