// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mode Of Payment", {
	currency(frm) {
        frappe.call({
            method: "get_currency_exchange_rate",
            doc: frm.doc,
            callback: function (r) {
              frm.set_value("exchange_rate",r.message)
            },
        });
	},
});
