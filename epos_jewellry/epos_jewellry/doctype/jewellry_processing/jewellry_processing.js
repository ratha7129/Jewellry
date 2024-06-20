// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Jewellry Processing", {
	refresh(frm) {

	},
});

frappe.ui.form.on("Processing Out Material", {
	qty(frm,cdt,cdn) {
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty*doc.cost
        doc.total_amount = doc.qty*doc.price
        update_totals(frm)
	},
    material_code(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.api.get_info_by_type",
            args: {
                type: "Material",
                name: doc.material_code,
                stock_location: frm.doc.stock_location
            },
            callback: function (r) {
                doc.cost = r.message.cost
                doc.price = r.message.price
                doc.unit = r.message.unit
                doc.total_cost = doc.qty*doc.cost
                doc.total_amount = doc.qty*doc.price
                frm.refresh_field("processing_out_material")
                update_totals(frm)
            }
        });
        
    }
});

frappe.ui.form.on("Processing Leftover Material", {
    processing_leftover_material_remove(frm,cdt,cdn){
        update_totals(frm)
    },
	qty(frm,cdt,cdn) {
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty*doc.cost
        doc.total_amount = doc.qty*doc.price
        update_totals(frm)
	},
    material_code(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.api.get_info_by_type",
            args: {
                type: "Material",
                name: doc.material_code,
                stock_location: frm.doc.stock_location
            },
            callback: function (r) {
                doc.cost = r.message.cost
                doc.price = r.message.price
                doc.unit = r.message.unit
                doc.total_cost = doc.qty*doc.cost
                doc.total_amount = doc.qty*doc.price
                frm.refresh_field("processing_leftover_material")
                update_totals(frm)
            }
        });
        
    }
});

frappe.ui.form.on("Processing Item", {
    processing_item_remove(frm,cdt,cdn){
        update_totals(frm)
    },
	qty(frm,cdt,cdn) {
        let doc = locals[cdt][cdn];
        doc.total_cost = doc.qty*doc.cost
        doc.total_amount = doc.qty*doc.price
        doc.total_fee = doc.fee * doc.qty
        update_totals(frm)
	},
    item_code(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.api.get_info_by_type",
            args: {
                type: "Item",
                name: doc.item_code,
                stock_location: frm.doc.stock_location
            },
            callback: function (r) {
                doc.cost = r.message.cost
                doc.price = r.message.price
                doc.unit = r.message.unit
                doc.total_cost = doc.qty*doc.cost
                doc.total_amount = doc.qty*doc.price
                frm.refresh_field("processing_item")
                update_totals(frm)
            }
        });
    },
    fee(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.total_fee = doc.fee * doc.qty
        frm.refresh_field("processing_item")
        update_totals(frm)
    }
});

function update_totals(frm){
    if(frm.doc.processing_out_material){
        frm.set_value("t_total_qty",frm.doc.processing_out_material.reduce((a, i) => a + i.qty, 0)) 
        frm.set_value("t_total_cost",frm.doc.processing_out_material.reduce((a, i) => a + i.total_cost, 0)) 
        frm.set_value("t_total_amount",frm.doc.processing_out_material.reduce((a, i) => a + i.total_amount, 0)) 
        frm.refresh_field("processing_out_material")
    }

    if(frm.doc.processing_leftover_material){
        frm.set_value("l_total_qty",frm.doc.processing_leftover_material.reduce((a, i) => a + i.qty, 0)) 
        frm.set_value("l_total_cost",frm.doc.processing_leftover_material.reduce((a, i) => a + i.total_cost, 0)) 
        frm.set_value("l_total_amount",frm.doc.processing_leftover_material.reduce((a, i) => a + i.total_amount, 0)) 
        frm.refresh_field("processing_leftover_material")
    }

    if(frm.doc.processing_item){
        frm.set_value("i_total_qty",frm.doc.processing_item.reduce((a, i) => a + i.qty, 0)) 
        frm.set_value("i_total_cost",frm.doc.processing_item.reduce((a, i) => a + i.total_cost, 0)) 
        frm.set_value("i_total_amount",frm.doc.processing_item.reduce((a, i) => a + i.total_amount, 0)) 
        frm.set_value("total_fee",frm.doc.processing_item.reduce((a, i) => a + i.total_fee, 0)) 
        frm.set_value("balance",frm.doc.processing_item.reduce((a, i) => a + i.total_fee, 0)) 
        frm.refresh_field("processing_item")
    }
}