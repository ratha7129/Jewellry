frappe.treeview_settings['Material Category'] = {
    breadcrumb: 'Material Category',
    title: 'Material Category',
    fields: [
        {
            fieldtype:'Data', 
            fieldname:'material_category_name_en', 
            label:__('Material Category Name EN'),
            reqd:true
        },
        {
            fieldtype:'Data', 
            fieldname:'material_category_name_kh', 
            label:__('Material Category Name KH')
        },
        {
            fieldtype:'Data', 
            fieldname:'material_code_prefix', 
            label:__('Material Code Prefix')
        },
        {
            fieldtype:'Data', 
            fieldname:'material_code_digit', 
            label:__('Material Code Digit')
        },
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group')
        }
    ],
    extend_toolbar: true
}
