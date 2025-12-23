# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airplane(Document):
	# def before_insert(self):
	# 	airplane_brand= frappe.db.get_value("Airplane Ticket", self.flight, "airplane")
	# 	capacity = frappe.db.get_value("Airplane", airplane_brand, "capacity")
	# 	ticket_count = frappe.db.count(
	# 		"Airplane Ticket",
	# 		{
	# 			"airplane_flight": self.airplane_flight
	# 		}
	# 	)

	# 	if ticket_count >=capacity:
	# 		frappe.throw("The number of tickets for that flight have exceeded, we're sorry.")
	pass
