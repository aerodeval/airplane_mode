// Copyright (c) 2025, Sydney and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Type", {
    setup(frm) {
        frm.set_query('shop_type',
        () => {
            return {
                filters: {
                    enabled: 1
                }
            };
        });
    }
});
