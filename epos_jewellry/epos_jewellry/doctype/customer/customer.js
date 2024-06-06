// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
	refresh(frm) {
        frm.set_query('customer_group', () => {
            return {
                filters: [
                    ["Customer Group", "is_group", "=", 0]
                ]
            }
        });
	},
});
