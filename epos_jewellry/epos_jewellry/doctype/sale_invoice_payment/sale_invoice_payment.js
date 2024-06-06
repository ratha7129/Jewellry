// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale Invoice Payment", {
	sale_invoice(frm) {
        frm.set_value("input_amount",frm.doc.balance*frm.doc.exchange_rate)
        frm.set_value("payment_amount",frm.doc.input_amount/frm.doc.exchange_rate)
        frm.set_value("sale_invoice_balance",frm.doc.balance-frm.doc.payment_amount)
	},
    mode_of_payment(frm){
        frm.set_value("input_amount",frm.doc.balance*frm.doc.exchange_rate)
        frm.set_value("payment_amount",frm.doc.input_amount/frm.doc.exchange_rate)
        frm.set_value("sale_invoice_balance",frm.doc.balance-frm.doc.payment_amount)
    },
    input_amount(frm){
        frm.set_value("payment_amount",frm.doc.input_amount/frm.doc.exchange_rate)
        frm.set_value("sale_invoice_balance",frm.doc.balance-frm.doc.payment_amount)
    }
});
