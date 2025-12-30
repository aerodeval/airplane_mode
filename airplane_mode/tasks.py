import frappe
from frappe.utils import getdate, add_months, formatdate, today
from datetime import date

def monthly():
    monthly_shop_check()
    create_receipt()

def daily():
    monthly_shop_check()
    create_receipt()


def create_receipt():
    rents = frappe.get_all(
        "Rent Payment",
        fields=["name", "contract", "tenant", "payment_date", "amount_paid"]
        )

    for rent in rents:

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


def monthly_shop_check():
    current_date = getdate(today())
    current_month = current_date.month
    current_year = current_date.year

    # previous month calculation
    if current_month == 1:
        prev_month = 12
        prev_year = current_year - 1
    else:
        prev_month = current_month - 1
        prev_year = current_year

    shops = frappe.get_all("Shop Details", fields=["shop_name", "shop_contact"])

    for shop in shops:
        overdue_shop = frappe.get_all(
            "Rent Payment",
            filters={
                "contract": shop.shop_name,
                "payment_status": "Pending",
            },
            fields=["name", "payment_date", "amount", "tenant_contact"]
        )

        # Check if previous month rent is unpaid
        for rent in overdue_shop:
            rent_date = getdate(rent['payment_date'])
            if rent_date.month == prev_month and rent_date.year == prev_year:
                send_rent_email(shop, rent)
                

def send_rent_email(shop, rent):
    frappe.sendmail(
        recipients=[rent['tenant_contact']],
        subject=f"Rent Due – {shop.shop_name}",
                    message=f"""
                                Hello,

                                The rent for the shop {shop.shop_name} dated {rent['payment_date']} is unpaid. 

                                Please make the payment as soon as possible.

                                Thanks.
                            """
                )