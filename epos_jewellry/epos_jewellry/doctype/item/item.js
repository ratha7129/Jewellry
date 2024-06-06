// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item", {
	refresh(frm) {
        frm.set_query('item_category', () => {
            return {
                filters: [
                    ["Item Category", "is_group", "=", 0]
                ]
            }
        });
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

function update_item_material(doc,frm){
    doc.total_amount = doc.qty * doc.price
    doc.total_cost = doc.qty * doc.cost
    frm.refresh_field('item_material');
}