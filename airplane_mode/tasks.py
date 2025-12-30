import frappe
from frappe.utils import getdate, add_months, formatdate


def monthly():
    create_receipt()

def daily():
    create_receipt()

def create_receipt():
    paid_rents = frappe.get_all(
        "Rent Payment",
        filters={"payment_status": "Paid"},
        fields=["name", "contract", "tenant", "payment_date", "amount_paid"]
        )

    for rent in paid_rents:

        rent_date = getdate(rent.payment_date)
        next_payment_date = add_months(rent_date, 1).replace(day=5)

        existing = frappe.db.exists(
            "Rent Payment",
            {
                "contract": rent.contract,
                "payment_date": next_payment_date
            }
        )

        if existing:
            continue  


        rent_doc = frappe.new_doc("Rent Payment")


        next_payment_date_str = formatdate(next_payment_date)
        rent_doc.name = f"{rent.contract}-{next_payment_date_str}"
        rent_doc.contract = rent.contract
        rent_doc.tenant = rent.tenant
        rent_doc.payment_date = next_payment_date
        rent_doc.amount_paid = rent.amount_paid
        rent_doc.payment_status = "Pending"

        rent_doc.insert(ignore_permissions=True)

def update_ticket_gate_numbers(flight_name, new_gate):
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight_name},
        pluck="name"
    )

    for ticket in tickets:
        frappe.db.set_value(
            "Airplane Ticket",
            ticket,
            "gate",
            new_gate
        )

    frappe.db.commit()

