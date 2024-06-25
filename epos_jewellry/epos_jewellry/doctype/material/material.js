// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Material", {
    onload_post_render: function(frm) {
        frm.set_value('material_stock_location', []);
        frm.refresh_field('material_stock_location');
        frm.call({
            method: 'get_stock_location_material',
            doc:frm.doc,
            callback:function(r){
                total_qty = 0
                if(r.message){
                    r.message.forEach(p => {
                        total_qty += p.qty
                        frm.add_child('material_stock_location', {
                            stock_location : p.stock_location,
                            unit : p.unit,
                            price : p.price,
                            cost : p.cost,
                            qty : p.qty,
                            stock_location_item : p.name
                        });
                    });
                    frm.refresh_field('material_stock_location')
                }
                frm.set_value("qty",total_qty)
            },
            async: true,
        });
    },
	refresh(frm) {
        frm.set_query('material_category', () => {
            return {
                filters: [
                    ["Material Category", "is_group", "=", 0]
                ]
            }
        });
        frm.add_custom_button(__('Generate Stock Location Item'), function(){
            frappe.call({
                method: "generate_stock_location_material",
                doc: frm.doc,
                callback: function (r) {
                    frm.reload_doc()
                    frm.refresh_field('item_stock_location')
                 },
            });
        }, __("Action"));
        frm.get_field("material_stock_location").grid.cannot_add_rows = true;
        frm.fields_dict["material_stock_location"].grid.wrapper.find(".grid-remove-rows").hide();
	},
});
frappe.ui.form.on("Material Stock Location", {
    qty(frm,cdt,cdn){
        total_qty = 0
        frm.doc.material_stock_location.forEach(r => {
            total_qty += r.qty
        });
        frm.set_value("qty",total_qty)
    }
})