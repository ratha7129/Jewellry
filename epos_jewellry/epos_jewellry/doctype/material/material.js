// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Material", {
	refresh(frm) {
        frm.set_query('material_category', () => {
            return {
                filters: [
                    ["Material Category", "is_group", "=", 0]
                ]
            }
        });
	},
});
