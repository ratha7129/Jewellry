// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Buy In", {
    refresh(frm) {
        frm.set_query('sale_invoice', () => {
            return {
                filters: [
                    ["Sale Invoice", "status", "not in", ["Cancelled","Buy Back"]]
                ]
            }
        });
	},
	sale_invoice(frm) {
        frappe.call({
            method: "get_sale_invoice_for_buy_in",
            doc:frm.doc,
            callback: function (r) {
                frm.set_value("customer",r.message.customer)
                frm.set_value("item",r.message.item)
                r.message.sale_invoice_item_material.forEach(m => {
                        doc = frm.add_child("buy_in_material");
                        doc.material_code = m.material_code
                        doc.material_name = m.material_name
                        doc.unit = m.unit
                        doc.price = m.price
                        doc.cost = m.cost
                        doc.qty = m.qty
                        doc.total_amount = m.qty * m.price
                        doc.total_cost = m.qty * m.cost
                });
               frm.refresh_field("buy_in_material")
            },
            error: function (r) {
                frappe.throw(_("Load data fail."))
            },
        });
	},
});
