import frappe


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

