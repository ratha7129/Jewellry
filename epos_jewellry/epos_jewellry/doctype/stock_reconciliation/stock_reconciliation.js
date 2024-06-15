// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Reconciliation", {
	refresh(frm) {
        if (frm.doc.docstatus == 1){
            frm.page.btn_secondary.hide()
        }
	},
});
frappe.ui.form.on("Stock Reconciliation Item", {
    stock_reconciliation_item_add(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.type = frm.doc.type
        frm.refresh_field("stock_reconciliation_item")
    },
    qty(frm,cdt,cdn){
        update_total(frm)
    },
    cost(frm,cdt,cdn){
        update_total(frm)
    },
    item_code(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.api.get_info_by_type",
            args: {
                type: frm.doc.type,
                name: doc.item_code,
                stock_location: frm.doc.stock_location
            },
            callback: function (r) {
                doc.cost = r.message.cost
                doc.price = r.message.price
                doc.qty = r.message.qty
                doc.current_cost = r.message.cost
                doc.current_qty = r.message.qty
                doc.unit = r.message.unit
                frappe.call({
                    method: "epos_jewellry.epos_jewellry.doctype.stock_entry.stock_entry.get_name_by_type",
                    args: {
                        type:frm.doc.type,
                        name: doc.item_code
                    },
                    callback: function (r) {
                        doc.item_name = r.message
                        update_total(frm)
                    }
                });
            }
        });
    }
});

function update_total(frm){
    frm.set_value("total_qty_change",frm.doc.stock_reconciliation_item.reduce((a, i) => a + (i.qty - i.current_qty), 0))
    frm.set_value("total_amount_change",frm.doc.stock_reconciliation_item.reduce((a, i) => a + ((i.cost * i.qty) - (i.current_cost * i.current_qty)), 0))
    frm.refresh_field("stock_reconciliation_item")
}