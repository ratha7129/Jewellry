// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Location", {
	refresh(frm) {
        frm.add_custom_button(__('Generate Stock Location Item'), function(){
            frappe.call({
                method: "generate_stock_location_material_and_item",
                doc:frm.doc,
                callback: function (r) {
                    
                },
                error: function (r) {
                    frappe.throw(_("Load data fail."))
                },
            });
        }, __("Action"));
	},
});
