// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	refresh(frm) {
        frm.set_query('employee_group', () => {
            return {
                filters: [
                    ["Employee Group", "is_group", "=", 0]
                ]
            }
        });
	},
});
