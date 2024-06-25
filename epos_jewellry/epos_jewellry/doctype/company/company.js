// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Company", {
	refresh(frm) {
        if (frappe.user.has_role('System Manager')) {
            if (frm.has_perm('write')) {
                frm.add_custom_button(__('Reset Database'), function() {
                    frm.trigger("reset_database");
                }, __('Action'));
            }
        }
        if (frappe.user.has_role('System Manager')) {
            if (frm.has_perm('write')) {
                frm.add_custom_button(__('Delete Transactions'), function() {
                    frm.trigger("delete_transactions");
                }, __('Action'));
            }
        }
	},
    reset_database: function(frm) {
		frappe.verify_password(function() {
        frappe.call({
            method: "reset_database",
            doc:frm.doc,
            freeze: true,
            callback: function(r, rt) {
                if(!r.exc)
                    frappe.msgprint(__("Successfully reset database"));
            },
        });
    })},
    delete_transactions: function(frm) {
		frappe.verify_password(function() {
        frappe.call({
            method: "delete_transactions",
            doc:frm.doc,
            freeze: true,
            callback: function(r, rt) {
                if(!r.exc)
                    frappe.msgprint(__("Successfully deleted all transactions"));
            },
        });
    })}
})
