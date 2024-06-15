// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry", {
	refresh(frm) {

	},
    type(frm){
        frm.doc.stock_entry_item = []
        frm.doc.stock_entry_item.forEach(r => {
            r.type = frm.doc.type
        });
        frm.refresh_field("stock_entry_item")
    },
});
frappe.ui.form.on("Stock Entry Item", {
    stock_entry_item_add(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.type = frm.doc.type
        frm.refresh_field("stock_entry_item")
    },
    qty(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty * doc.cost
        doc.total_amount = doc.qty * doc.price
        update_total(frm)
    },
    cost(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty * doc.cost
        doc.total_amount = doc.qty * doc.price
        update_total(frm)
    },
    item_code(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.api.get_info_by_type",
            args: {
                type: frm.doc.type,
                name: doc.item_code,
                stock_location: frm.doc.from_stock_location
            },
            callback: function (r) {
                doc.cost = r.message.cost
                doc.price = r.message.price
                doc.unit = r.message.unit
                frappe.call({
                    method: "epos_jewellry.epos_jewellry.doctype.stock_entry.stock_entry.get_name_by_type",
                    args: {
                        type:frm.doc.type,
                        name: doc.item_code
                    },
                    callback: function (r) {
                        doc.item_name = r.message
                        doc.total_cost = doc.qty * doc.cost
                        doc.total_amount = doc.qty * doc.price
                        update_total(frm)
                    }
                });
            }
        });
    }
});

function update_total(frm){
    frm.set_value("total_qty",frm.doc.stock_entry_item.reduce((a, i) => a + i.qty, 0))
    frm.set_value("total_amount",frm.doc.stock_entry_item.reduce((a, i) => a + i.total_amount, 0))
    frm.set_value("total_cost",frm.doc.stock_entry_item.reduce((a, i) => a + i.total_cost, 0))
    frm.set_value("total_item",frm.doc.stock_entry_item.length)
    frm.refresh_field("stock_entry_item")
}