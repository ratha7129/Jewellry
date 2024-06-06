
frappe.treeview_settings['Employee Group'] = {
    breadcrumb: 'Employee Group',
    title: 'Employee Group',
    fields: [
        {
            fieldtype:'Data', 
            fieldname:'employee_group_name_en', 
            label:__('Employee Group Name EN'),
            reqd:true
        },
        {
            fieldtype:'Data', 
            fieldname:'employee_group_name_kh', 
            label:__('Employee Group Name KH')
        },
        {
            fieldtype:'Data', 
            fieldname:'employee_code_prefix', 
            label:__('Employee Code Prefix')
        },
        {
            fieldtype:'Data', 
            fieldname:'employee_code_digit', 
            label:__('Employee Code Digit')
        },
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group')
        },
    ],
    extend_toolbar: true
}
