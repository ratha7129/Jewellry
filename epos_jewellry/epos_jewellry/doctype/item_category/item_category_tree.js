
frappe.treeview_settings['Item Category'] = {
    breadcrumb: 'Item Category',
    title: 'Item Category',
    fields: [
        {
            fieldtype:'Data', 
            fieldname:'item_category_name_en', 
            label:__('Item Category Name EN'),
            reqd:true
        },
        {
            fieldtype:'Data', 
            fieldname:'item_category_name_kh', 
            label:__('Item Category Name KH')
        },
        {
            fieldtype:'Data', 
            fieldname:'item_code_prefix', 
            label:__('Item Code Prefix')
        },
        {
            fieldtype:'Data', 
            fieldname:'item_code_digit', 
            label:__('Item Code Digit')
        },
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group')
        },
    ],
    extend_toolbar: true
}
