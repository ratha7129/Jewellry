# Copyright (c) 2024, ESTC and contributors
# For license information, please see license.txt
from frappe.model.naming import NamingSeries
from frappe.model import no_value_fields
import frappe
from frappe.model.document import Document
from datetime import datetime
import shlex, subprocess
from frappe.model.document import Document
from frappe.utils import cstr
import asyncio
from datetime import datetime

class Company(Document):
	def on_update(self):
		for df in self.meta.get("fields"):
			if df.fieldtype not in no_value_fields and self.has_value_changed(df.fieldname):
				frappe.db.set_default(df.fieldname, self.get(df.fieldname))
	
	@frappe.whitelist()
	def reset_database(self):
		run_backup_command()
		frappe.db.sql('delete from `tabJeweller Payment Process`')
		frappe.db.sql('delete from `tabJeweller Payment`')
		frappe.db.sql('delete from `tabProcessing Item`')
		frappe.db.sql('delete from `tabProcessing Leftover Material`')
		frappe.db.sql('delete from `tabProcessing Out Material`')
		frappe.db.sql('delete from `tabJewellry Processing`')
		frappe.db.sql('delete from `tabJeweller`')
		frappe.db.sql('delete from `tabStock Reconciliation Item`')
		frappe.db.sql('delete from `tabStock Reconciliation`')
		frappe.db.sql('delete from `tabSupplier`')
		frappe.db.sql('delete from `tabStock Entry Item`')
		frappe.db.sql('delete from `tabStock Entry`')
		frappe.db.sql('delete from `tabMaterial Stock Location`')
		frappe.db.sql('delete from `tabStock Location Material`')
		frappe.db.sql('delete from `tabItem Stock Location`')
		frappe.db.sql('delete from `tabStock Location Item`')
		frappe.db.sql('delete from `tabStock Location`')
		frappe.db.sql('delete from `tabBuy In Material`')
		frappe.db.sql('delete from `tabBuy In`')
		frappe.db.sql('delete from `tabStock Ledger Entry`')
		frappe.db.sql('delete from `tabSale Invoice Payment`')
		frappe.db.sql('delete from `tabCurrency Exchange Rate`')
		frappe.db.sql('delete from `tabSale Invoice Item Material`')
		frappe.db.sql('delete from `tabEmployee Group`')
		frappe.db.sql('delete from `tabEmployee`')
		frappe.db.sql('delete from `tabSale Invoice`')
		frappe.db.sql('delete from `tabCustomer`')
		frappe.db.sql('delete from `tabCustomer Group`')
		frappe.db.sql('delete from `tabItem Material`')
		frappe.db.sql('delete from `tabItem`')
		frappe.db.sql('delete from `tabItem Category`')
		frappe.db.sql('delete from `tabMaterial`')
		frappe.db.sql('delete from `tabMaterial Category`')
		frappe.db.sql('delete from `tabUOM`')
		frappe.db.sql('delete from `tabUOM Category`')
            
		naming_series = NamingSeries("SIP.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("SUP.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("SRE.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("BI.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("STE.-.YYYY.####")
		naming_series.update_counter(0)

		naming_series = NamingSeries("JPR.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("JW.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("SINV.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("SLE.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("JPA.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("SINV.YYYY.-.####")
		naming_series.update_counter(0)


		a = frappe.new_doc("Jeweller")
		a.jeweller_name_en = "General"
		a.jeweller_name_kh= "General"
		a.insert()

		b = frappe.new_doc("Supplier")
		b.supplier_name = "General"
		b.insert()

		c = frappe.new_doc("Stock Location")
		c.stock_location_name = "Main Stock Location"
		c.insert()

		d = frappe.new_doc("Currency Exchange Rate")
		d.posting_date = datetime.today().strftime('%Y-%m-%d')
		d.from_currency = frappe.get_single("Company").currency
		d.to_currency = "KHR"
		d.exchange_rate = 4000
		d.docstatus = 1
		d.insert()
		d = None
		d = frappe.new_doc("Currency Exchange Rate")
		d.posting_date = datetime.today().strftime('%Y-%m-%d')
		d.from_currency = "KHR"
		d.to_currency = "KHR"
		d.exchange_rate = 1
		d.docstatus = 1
		d.insert()
		d = None
		d = frappe.new_doc("Currency Exchange Rate")
		d.posting_date = datetime.today().strftime('%Y-%m-%d')
		d.from_currency = frappe.get_single("Company").currency
		d.to_currency = frappe.get_single("Company").currency
		d.exchange_rate = 1
		d.docstatus = 1
		d.insert()

		e = frappe.new_doc("Employee Group")
		e.employee_group_name_en = "All Group"
		e.employee_group_name_kh = "All Group"
		e.is_group = 1
		e.insert()
		e = None
		e = frappe.new_doc("Employee Group")
		e.parent_employee_group = "All Group"
		e.employee_group_name_en = "General"
		e.employee_group_name_kh = "General"
		e.employee_code_prefix = "G"
		e.employee_code_digit = "0000"
		e.current_number = 0
		e.insert()

		f = frappe.new_doc("Customer Group")
		f.customer_group_name_en = "All Group"
		f.customer_group_name_kh = "All Group"
		f.is_group = 1
		f.insert()
		f= None
		f = frappe.new_doc("Customer Group")
		f.parent_customer_group = "All Group"
		f.customer_group_name_en = "General"
		f.customer_group_name_kh = "General"
		f.customer_code_prefix = "G"
		f.customer_code_digit = "0000"
		f.current_number = 0
		f.insert()

		g = frappe.new_doc("Item Category")
		g.item_category_name_en = "All Category"
		g.item_category_name_kh = "All Category"
		g.is_group = 1
		g.insert()
		g = None
		g = frappe.new_doc("Item Category")
		g.parent_item_category = "All Category"
		g.item_category_name_en = "General"
		g.item_category_name_kh = "General"
		g.item_code_prefix = "G"
		g.item_code_digit = "0000"
		g.current_number = 0
		g.insert()
        
		h = frappe.new_doc("Material Category")
		h.material_category_name_en = "All Category"
		h.material_category_name_kh = "All Category"
		h.is_group = 1
		h.insert()
		h = None
		h = frappe.new_doc("Material Category")
		h.parent_material_category = "All Category"
		h.material_category_name_en = "General"
		h.material_category_name_kh = "General"
		h.material_code_prefix = "G"
		h.material_code_digit = "0000"
		h.current_number = 0
		h.insert()

		i = frappe.new_doc("UOM Category")
		i.uom_category_name_en = "General"
		i.uom_category_name_kh = "General"
		i.insert()

		j = frappe.new_doc("UOM")
		j.uom_category = "General"
		j.uom_name = "Unit"
		j.insert()

		k = frappe.new_doc("Customer")
		k.customer_group = "General"
		k.customer_name_en = "General"
		k.customer_name_kh = "General"
		k.insert()

		k = frappe.new_doc("Employee")
		k.employee_group = "General"
		k.employee_name_en = "General"
		k.employee_name_kh = "General"
		k.insert()

	
	@frappe.whitelist()
	def delete_transactions(self):
		run_backup_command()
		frappe.db.sql('delete from `tabJeweller Payment Process`')
		frappe.db.sql('delete from `tabJeweller Payment`')
		frappe.db.sql('delete from `tabProcessing Item`')
		frappe.db.sql('delete from `tabProcessing Leftover Material`')
		frappe.db.sql('delete from `tabProcessing Out Material`')
		frappe.db.sql('delete from `tabJewellry Processing`')
		frappe.db.sql('delete from `tabStock Reconciliation Item`')
		frappe.db.sql('delete from `tabStock Reconciliation`')
		frappe.db.sql('delete from `tabStock Entry Item`')
		frappe.db.sql('delete from `tabStock Entry`')
		frappe.db.sql('delete from `tabBuy In Material`')
		frappe.db.sql('delete from `tabBuy In`')
		frappe.db.sql('delete from `tabStock Ledger Entry`')
		frappe.db.sql('delete from `tabSale Invoice Payment`')
		frappe.db.sql('delete from `tabSale Invoice Item Material`')
		frappe.db.sql('delete from `tabSale Invoice`')
            
		naming_series = NamingSeries("SIP.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("SRE.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("BI.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("STE.YYYY.####")
		naming_series.update_counter(0)

		naming_series = NamingSeries("JPR.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("SINV.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("SLE.YYYY.-.####")
		naming_series.update_counter(0)
        
		naming_series = NamingSeries("JPA.YYYY.-.####")
		naming_series.update_counter(0)
            
		naming_series = NamingSeries("SINV.YYYY.-.####")
		naming_series.update_counter(0)


@frappe.whitelist()
def run_backup_command():
    site_name = cstr(frappe.local.site)
    command = "bench --site " + site_name + " backup --with-files"
    asyncio.run(run_bench_command(command))

async def run_bench_command(command, kwargs=None):
    site = {"site": frappe.local.site}
    cmd_input = None
    if kwargs:
        cmd_input = kwargs.get("cmd_input", None)
        if cmd_input:
            if not isinstance(cmd_input, bytes):
                raise Exception(f"The input should be of type bytes, not {type(cmd_input).__name__}")
            del kwargs["cmd_input"]
        kwargs.update(site)
    else:
        kwargs = site
    command = " ".join(command.split()).format(**kwargs)
    command = shlex.split(command)
    subprocess.run(command, input=cmd_input, capture_output=True)