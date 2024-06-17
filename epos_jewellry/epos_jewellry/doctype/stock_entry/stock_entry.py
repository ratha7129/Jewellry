# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epos_jewellry.epos_jewellry.doctype.api import stock_ledger_entry,get_info_by_type

class StockEntry(Document):
	def validate(self):
		for a in self.stock_entry_item:
			if a.qty <= 0:
				frappe.throw("Item {} quantity can not be zero or smaller than zero".format(a.item_code))


	def on_submit(self):
		if self.stock_entry_type in ["Stock In","Stock Take"]:
			if self.type == "Item":
				for a in self.stock_entry_item:
					add_item_stock_ledger_entry(self,a,self.stock_entry_type,self.from_stock_location)
					if self.stock_in_material == 1:
						doc = frappe.db.sql("select material_code item_code,unit,price,cost,qty from `tabItem Material` where parent = '{0}'".format(a.item_code),as_dict=1)
						for b in doc:
							b.qty = b.qty * a.qty
							add_material_stock_ledger_entry(self,b,self.stock_entry_type,self.from_stock_location)
			else:
				for a in self.stock_entry_item:
					add_material_stock_ledger_entry(self,a,self.stock_entry_type,self.from_stock_location)
		else:
			if self.type == "Item":
				for a in self.stock_entry_item:
					add_item_stock_ledger_entry(self,a,"Stock Take",self.from_stock_location)
					add_item_stock_ledger_entry(self,a,"Stock In",self.to_stock_location)
			else:
				for a in self.stock_entry_item:
					add_material_stock_ledger_entry(self,a,"Stock Take",self.from_stock_location)
					add_material_stock_ledger_entry(self,a,"Stock In",self.to_stock_location)



	def on_cancel(self):
		if self.stock_entry_type in ["Stock In","Stock Take"]:
			if self.type == "Item":
				for a in self.stock_entry_item:
					add_item_stock_ledger_entry(self,a,self.stock_entry_type,self.from_stock_location)
			else:
				for a in self.stock_entry_item:
					add_material_stock_ledger_entry(self,a,self.stock_entry_type,self.from_stock_location)
		else:
			if self.type == "Item":
				for a in self.stock_entry_item:
					add_item_stock_ledger_entry(self,a,"Stock Take",self.from_stock_location)
					add_item_stock_ledger_entry(self,a,"Stock In",self.to_stock_location)
			else:
				for a in self.stock_entry_item:
					add_material_stock_ledger_entry(self,a,"Stock Take",self.from_stock_location)
					add_material_stock_ledger_entry(self,a,"Stock In",self.to_stock_location)

@frappe.whitelist()
def get_name_by_type(type,name):
	if type == "Item":
		doc = frappe.get_doc("Item",name)
		return doc.item_name_en or ""
	else:
		doc = frappe.get_doc("Material",name)
		return doc.material_name or ""


def add_item_stock_ledger_entry(self,item,stock_entry_type,stock_location):
	if self.docstatus == 1:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock Entry",
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
					'voucher_type':"Stock Entry",
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
					'voucher_type':"Stock Entry",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.item_code,
					'unit': item.unit,
					'price': item.price,
					'cost': item.cost,
					'current_qty': get_info_by_type("Material",item.item_code,stock_location).qty,
					'qty_change': item.qty if stock_entry_type == "Stock In" else item.qty*-1,
					'qty_after_transaction': get_info_by_type("Material",item.item_code,stock_location).qty + (item.qty if stock_entry_type == "Stock In" else item.qty*-1),
					'stock_location': stock_location,
					'note':"New Stock Entry {0} Type {1}".format(self.name,stock_entry_type)
				})
	else:
		stock_ledger_entry({
					'doctype': 'Stock Ledger Entry',
					'voucher_type':"Stock Entry",
					'voucher_no':self.name,
					'posting_date':self.posting_date,
					'ledger_type':'Material',
					'item_code': item.item_code,
					'unit':item.unit,
					'price':item.price,
					'cost':item.cost,
					'current_qty': get_info_by_type("Material",item.item_code,stock_location).qty,
					'qty_change': item.qty*-1 if stock_entry_type == "Stock In" else item.qty,
					'qty_after_transaction': get_info_by_type("Material",item.item_code,stock_location).qty + (item.qty*-1 if stock_entry_type == "Stock In" else item.qty),
					'stock_location': stock_location,
					'note':"Cancelled Stock Entry {0} Type {1}".format(self.name,stock_entry_type)
				})