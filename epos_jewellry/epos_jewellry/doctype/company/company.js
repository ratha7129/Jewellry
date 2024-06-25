// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Company", {
	refresh(frm) {
        if (frappe.user.has_role('System Manager')) {
            if (frm.has_perm('write')) {
                frm.add_custom_button(__('Reset Database'), function() {
                    frappe.verify_password(function(){
                        frappe.call({
                            method: "epos_jewellry.epos_jewellry.doctype.company.company.reset_database",
                            freeze: true,
                            callback: function(r, rt) {
                                if(!r.exc)
                                    frappe.msgprint(__("Successfully Reset Database"));
                            },
                        });
                    });
                }, __('Action'));
            }
        }
        if (frappe.user.has_role('System Manager')) {
            if (frm.has_perm('write')) {
                frm.add_custom_button(__('Delete Transactions'), function() {
                    frappe.verify_password(function() {
                        frappe.call({
                            method: "epos_jewellry.epos_jewellry.doctype.company.company.delete_transactions",
                            freeze: true,
                            callback: function(r, rt) {
                                if(!r.exc)
                                    frappe.msgprint(__("Successfully Feleted All Transactions"));
                            },
                        });
                    });
                }, __('Action'));
            }
        }
	}
})
