import frappe



def after_install():
    shop_types = ["Santa", "Christmas"]   #shoptypes to be added

    for shop_type_name in shop_types:
        if not frappe.db.exists("Shop Type", shop_type_name):
            doc = frappe.get_doc({
                "doctype": "Shop Type",
                "name": shop_type_name, 
                "enabled": 1
            })
            doc.insert(ignore_permissions=True)