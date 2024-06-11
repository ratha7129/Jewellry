// Copyright (c) 2024, ESTC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale Invoice", {
	onload(frm) {
        frm.get_field("sale_invoice_item_material").grid.cannot_add_rows = true;
        frm.fields_dict["sale_invoice_item_material"].grid.wrapper.find(".grid-remove-rows").hide();
        frm.doc.sale_invoice_item_material.forEach(p=>{
            frm.fields_dict['sale_invoice_item_material'].grid.wrapper.find('.btn-open-row').hide();
        })
	},
    refresh(frm){
        frm.page.btn_secondary.show()
        allow_discount(frm)
        if(frm.doc.status == "Buy Back"){
            frm.page.btn_secondary.hide()
            frm.add_custom_button(__('Go To Buy In'), function(){
                frappe.set_route('Form', "Buy In", frm.doc.buy_in_no);
            }, __("Action"));
        }
    },
    discount_amount(frm) {
        update_totals(frm)
    },
    discount_percent(frm) {
        update_totals(frm)
    },
    discount_type(frm){
        allow_discount(frm)
    },
    item(frm){
        frm.doc.sale_invoice_item_material=[]
        frappe.call({
            method: "epos_jewellry.epos_jewellry.doctype.api.get_item_material",
            args: {
                item_code: frm.doc.item
            },
            callback: function (r) {
               r.message.forEach(m => {
                    doc = frm.add_child("sale_invoice_item_material");
                    doc.material_code = m.material_code
                    doc.material_name = m.material_name
                    doc.unit = m.unit
                    doc.price = m.price
                    doc.cost = m.cost
                    doc.qty = m.qty
                    doc.total_amount = m.qty * m.price
                    doc.total_cost = m.qty * m.cost
               });
               frm.refresh_field("sale_invoice_item_material")
            },
            error: function (r) {
                frappe.throw(_("Load data fail."))
            },
        });
        update_totals(frm);
    }
});

function update_totals(frm){
    if (frm.doc.allow_discount == 0){
        frm.set_df_property("discount_type", "read_only", 1);
        frm.set_df_property("discount_percent", "read_only", 1);
        frm.set_df_property("discount_amount", "read_only", 1);
    }
    frm.set_value("sub_total",frm.doc.price)
    frm.set_value("total_cost",frm.doc.cost)
    if (frm.doc.discount_type == "Percent"){
        frm.set_value("discount_amount",frm.doc.sub_total * (frm.doc.discount_percent/100)) 
    }
    else{
        frm.set_value("discount_percent",(frm.doc.discount_amount/frm.doc.sub_total)*100) 
    }
    frm.set_value("total_amount",frm.doc.price - frm.doc.discount_amount)
    frm.set_value("total_profit",frm.doc.total_amount - frm.doc.cost)
}

function allow_discount(frm){
    if(frm.doc.discount_type == "Not Set"){
        frm.set_df_property("discount_percent", "read_only", 1);
        frm.set_df_property("discount_amount", "read_only", 1);
    }
    else if(frm.doc.discount_type == "Percent"){
        frm.set_df_property("discount_percent", "read_only", 0);
        frm.set_df_property("discount_amount", "read_only", 1);
    }
    else{
        frm.set_df_property("discount_percent", "read_only", 1);
        frm.set_df_property("discount_amount", "read_only", 0);
    }
}