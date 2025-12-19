// Copyright (c) 2025, Sydney and contributors
// For license information, please see license.txt

frappe.ui.form.on("Flight Passenger", {
    setup(frm) {
        frm.doc.full_name = frm.doc.first_name + " " +  frm.doc.last_name;
        }
});
