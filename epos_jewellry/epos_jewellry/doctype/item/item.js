// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item", {
    onload: function(frm) {
        if (frm.is_new() && frm.doc.item_code != ""){
            frm.doc.item_code = ""
        }
        if(!frm.is_new()){
            frm.set_value('item_stock_location', []);
            frm.refresh_field('item_stock_location');
            frm.call({
                method: 'get_stock_location_item',
                doc:frm.doc,
                callback:function(r){
                    total_qty = 0
                    if(r.message){
                        r.message.forEach(p => {
                            total_qty += p.qty
                            frm.add_child('item_stock_location', {
                                stock_location : p.stock_location,
                                unit : p.unit,
                                price : p.price,
                                cost : p.cost,
                                qty : p.qty,
                                stock_location_item : p.name
                            });
                        });
                        frm.refresh_field('item_stock_location')
                    }
                    frm.set_value("qty",total_qty)
                    if (!frm.is_new()){
                        frm.save()
                    }
                },
                async: true,
            });
        }
    },
	refresh(frm) {
        frm.set_query('item_category', () => {
            return {
                filters: [
                    ["Item Category", "is_group", "=", 0]
                ]
            }
        });
        frm.add_custom_button(__('Generate Stock Location Item'), function(){
            frappe.call({
                method: "epos_jewellry.epos_jewellry.doctype.api.generate_stock_location_item",
                args: {
                    item: frm.doc
                },
                callback: function (r) {
                    frm.refresh_field('item_stock_location')
                },
                error: function (r) {
                    frappe.throw(_("Load data fail."))
                },
            });
        }, __("Action"));
        frm.get_field("item_stock_location").grid.cannot_add_rows = true;
        frm.fields_dict["item_stock_location"].grid.wrapper.find(".grid-remove-rows").hide();
	},
});
frappe.ui.form.on('Item Material', {
    qty(frm, cdt, cdn) {
		let doc = locals[cdt][cdn];
        update_item_material(doc,frm)
       
	},
    price(frm, cdt, cdn) {
		let doc = locals[cdt][cdn];
        update_item_material(doc,frm)
	},
    material_code(frm, cdt, cdn) {
		let doc = locals[cdt][cdn];
        update_item_material(doc,frm)
	}
})
frappe.ui.form.on("Item Stock Location", {
    qty(frm,cdt,cdn){
        total_qty = 0
        frm.doc.item_stock_location.forEach(r => {
            total_qty += r.qty
        });
        frm.set_value("qty",total_qty)
    }
})
function update_item_material(doc,frm){
    doc.total_amount = doc.qty * doc.price
    doc.total_cost = doc.qty * doc.cost
    frm.refresh_field('item_material');
}