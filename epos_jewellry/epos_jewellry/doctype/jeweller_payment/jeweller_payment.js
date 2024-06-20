// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Jeweller Payment", {
    mode_of_payment(frm){
        if(frm.doc.jeweller_payment_process){
            frm.doc.jeweller_payment_process.forEach(doc => {
                doc.input_amount = doc.total_fee * frm.doc.exchange_rate
                doc.total_payment = doc.total_fee
                doc.balance = doc.total_fee - doc.total_payment
                update_total(frm)
            });
        }
    },
    refresh(frm) {
        frm.fields_dict['jeweller_payment_process'].grid.get_field('processing').get_query = function(doc, cdt, cdn) {
            return {    
                filters:[
                    ["Jewellry Processing", "docstatus", "in", ["1"]],
                    ["Jewellry Processing", "jeweller", "=", frm.doc.jeweller],
                    ["Jewellry Processing", "balance", ">", 0]
                ]
            }
        }
	},
    jeweller(frm){
        frm.doc.jeweller_payment_process = [    ]
        frappe.call({
            method: "get_jeweller_processing",
            doc:frm.doc,
            callback: function (r) {
                r.message.forEach(m => {
                        doc = frm.add_child("jeweller_payment_process");
                        doc.processing = m.name
                        doc.total_fee = m.balance
                        doc.input_amount = doc.total_fee * frm.doc.exchange_rate
                        doc.total_payment = doc.total_fee
                        doc.balance = doc.total_fee - doc.total_payment
                });
               frm.refresh_field("jeweller_payment_process")
               update_total(frm)
            },
            error: function (r) {
                frappe.throw(_("Load data fail."))
            },
        });
    }
});

frappe.ui.form.on("Jeweller Payment Process", {
    jeweller_payment_process_remove(frm,cdt,cdn){
        update_total(frm)
    },
	processing(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.jeweller_payment.jeweller_payment.get_jeweller_processing_by_name",
            args: {
                name:doc.processing
            },
            callback: function (r) {
                m = r.message
                doc.processing = m.name
                doc.total_fee = m.balance
                doc.input_amount = doc.total_fee * frm.doc.exchange_rate
                doc.total_payment = doc.total_fee
                doc.balance = doc.total_fee - doc.total_payment
                frm.refresh_field("jeweller_payment_process")
                update_total(frm)
            },
            error: function (r) {
                frappe.throw(_("Load data fail."))
            },
        });
        update_total(frm)
    },
    input_amount(frm,cdt,cdn){
        let doc = locals[cdt][cdn];
        doc.total_payment = doc.input_amount/frm.doc.exchange_rate
        if(doc.total_payment>doc.total_fee){
            doc.input_amount = doc.total_fee * frm.doc.exchange_rate
            doc.total_payment = doc.total_fee
            doc.balance = 0
        }
        doc.balance = doc.total_fee - doc.total_payment
        update_total(frm)
    }
});

function update_total(frm){
    frm.set_value("total_fee",frm.doc.jeweller_payment_process.reduce((a, i) => a + i.total_fee, 0)) 
    frm.set_value("total_payment",frm.doc.jeweller_payment_process.reduce((a, i) => a + i.total_payment, 0)) 
    frm.set_value("balance",frm.doc.jeweller_payment_process.reduce((a, i) => a + i.balance, 0)) 
    frm.refresh_field("jeweller_payment_process")
}