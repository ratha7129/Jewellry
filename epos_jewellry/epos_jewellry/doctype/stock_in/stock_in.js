// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock In", {
	refresh(frm) {

	},
    type(frm){
        frm.doc.stock_in_item = []
        frm.doc.stock_in_item.forEach(r => {
            r.type = frm.doc.type
        });
        frm.refresh_field("stock_in_item")
    },
});
frappe.ui.form.on("Stock In Item", {
    stock_in_item_add(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.type = frm.doc.type
        frm.refresh_field("stock_in_item")
    },
    qty(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty * doc.cost
        update_total(frm)
    },
    cost(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty * doc.cost
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
                doc.unit = r.message.unit
                frappe.call({
                    method: "epos_jewellry.epos_jewellry.doctype.stock_in.stock_in.get_name_by_type",
                    args: {
                        type:frm.doc.type,
                        name: doc.item_code
                    },
                    callback: function (r) {
                        doc.item_name = r.message
                        doc.total_cost = doc.qty * doc.cost
                        update_total(frm)
                    }
                });
            }
        });
    }
});

function update_total(frm){
    frm.set_value("total_qty",frm.doc.stock_in_item.reduce((a, i) => a + i.qty, 0))
    frm.set_value("total_amount",frm.doc.stock_in_item.reduce((a, i) => a + i.total_cost, 0))
    frm.refresh_field("stock_in_item")
}