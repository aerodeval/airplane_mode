import frappe
from frappe.utils import getdate, add_months, formatdate, today, get_month
from datetime import date

def monthly():
    monthly_shop_check()
    create_receipt()

def daily():
    remind_upcoming_shop_rent()
    check_expired()
    

def create_receipt():
    billing_day=frappe.db.get_single_value("Shop Management Settings", "default_date")
    rents = frappe.get_all(
        "Rent Payment",
        fields=["name", "contract", "tenant", "payment_date", "amount_paid"]
        )

    for rent in rents:

        rent_date = getdate(rent.payment_date)
        next_payment_date = add_months(rent_date, 1).replace(day=billing_day )

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


def check_expired():
    current_date = getdate(today())
 
    expired_shops = frappe.get_all(
        "Shop Details",
            filters={
            "contract_expiry_date": ["<", current_date]
            },
            fields=["name", "shop_name", "contract_expiry_date"] 
    )

    for shop in expired_shops:
        frappe.delete_doc("Shop Details", shop.shop_name, force=True)
        frappe.delete_doc("Contract Details", shop.name, force=True)
        send_email(shop , reminder_type="expiry")



def monthly_shop_check():
    rent_reminder_setting=frappe.db.get_single_value("Shop Management Settings", "rent_reminder")
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

    if rent_reminder_setting:
        shops = frappe.get_all("Shop Details", 
        fields=["shop_name", "shop_contact", "rent_end_date"],
        )


        for shop in shops:
            overdue_shop = frappe.get_all(
                "Rent Payment",
                filters={
                    "contract": shop.shop_name,
                    "payment_status": "Pending",
                },
                fields=["name", "payment_date", "amount", "tenant_contact"]
            )
            print(overdue_shop)

            # Check if previous month rent is unpaid
            for rent in overdue_shop:
                rent_date = getdate(rent['payment_date'])
                if rent_date.month == prev_month and rent_date.year == prev_year:
                        send_email(shop, rent, reminder_type="due")

def remind_upcoming_shop_rent():
    rent_reminder_setting=frappe.db.get_single_value("Shop Management Settings", "rent_reminder")
    remind_before=frappe.db.get_single_value("Shop Management Settings", "remind_before")

    if rent_reminder_setting:
        current_date = getdate(today())
        shops = frappe.get_all(
            "Shop Details",
            fields=["shop_name", "shop_contact"]
        )

        for shop in shops:
            upcoming_rents = frappe.get_all(
                "Rent Payment",
                filters={
                    "contract": shop.shop_name,
                    "payment_status": "Pending",
                },
                fields=["name", "payment_date", "amount", "tenant_contact"]
            )

            for rent in upcoming_rents:
                rent_date = getdate(rent["payment_date"])
                days_left = (rent_date - current_date).days

                if days_left == remind_before:
                    send_email(shop, rent, reminder_type="upcoming")





def send_email(shop, rent, reminder_type):

    match reminder_type:
        case "upcoming":
            frappe.sendmail(
                recipients=[shop.shop_contact],
                subject=f"Upcoming Rent – {shop.shop_name}",
                message=f"""
                Hello,

                The rent for the shop {shop.shop_name} is upcoming please pay the rent to avoid further inconvinience.
                """
            )

        case "due":
            frappe.sendmail(
                            recipients=[shop.shop_contact],
                            subject=f"Rent Due – {shop.shop_name}",
                            message=f"""
                            Hello,

                            The rent for the shop {shop.shop_name} for the month of {get_month(rent['payment_date'])} is still  unpaid.
                            to avoid further action please pay the rent
                    """
                        )

        case "expired":
                      frappe.sendmail(
                            recipients=[shop.shop_contact],
                            subject=f"Rent Expired – {shop.shop_name}",
                            message=f"""
                            Hello,

                            The contract for the shop {shop.shop_name} is expired due to missed payments in rents.
                            Please contact support"""
                        )

                
            



