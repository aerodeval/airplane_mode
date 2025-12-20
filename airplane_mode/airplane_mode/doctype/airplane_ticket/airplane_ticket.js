// Copyright (c) 2025, Sydney and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button('Assign Seat', () => {
            let d = new frappe.ui.Dialog({
                title: 'Select Seat',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data'
                    },
                ],
                size: 'small', 
                primary_action_label: 'Assign',
                primary_action(values) {
                    d.hide();
                }
            });
            
            d.show();
            
            
            

        }, 'Actions')
	},
});
