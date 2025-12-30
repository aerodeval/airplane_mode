# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):

	def on_change(self):
		
		print("lol what is this")
		frappe.enqueue(
			method="airplane_mode.tasks.update_ticket_gate_numbers",
			queue="long",
			flight_name=self.name,
			new_gate=self.gate
		)

	def on_submit(self):
		self.status = "Completed"




	