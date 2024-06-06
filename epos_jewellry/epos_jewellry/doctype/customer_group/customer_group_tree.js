
frappe.treeview_settings['Customer Group'] = {
    breadcrumb: 'Customer Group',
    title: 'Customer Group',
    fields: [
        {
            fieldtype:'Data', 
            fieldname:'customer_group_name_en', 
            label:__('Customer Group Name EN'),
            reqd:true
        },
        {
            fieldtype:'Data', 
            fieldname:'customer_group_name_kh', 
            label:__('Customer Group Name KH')
        },
        {
            fieldtype:'Data', 
            fieldname:'customer_code_prefix', 
            label:__('Customer Code Prefix')
        },
        {
            fieldtype:'Data', 
            fieldname:'customer_code_digit', 
            label:__('Customer Code Digit')
        },
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group')
        },
    ],
    extend_toolbar: true
}
