# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):

	def before_insert(self):
		airplane_brand= frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		capacity = frappe.db.get_value("Airplane", airplane_brand, "capacity")
		ticket_count = frappe.db.count(
			"Airplane Ticket",
			{
				"flight": self.flight
			}
		)

		if ticket_count >=capacity:
			frappe.throw("The number of tickets for that flight have exceeded, we're sorry.")
				
	def on_submit(self):
		self.flight_status_check()


	def validate(self):
		self.total_amount = self.calc_total()
		self.unique_add_on_check()
		print(f"this is the status {self.status}")



		#validation for not allowing same seat booking
		if frappe.db.exists(

			"Airplane Ticket",
			{
				"flight": self.flight,
				"seat":self.seat

			}
			):
			frappe.throw(
                f"Seat {self.seat} has already been booked for this flight"
			)	

	
	# def generate_seat(self):
	# 	number = random.randint(1, 100)
	# 	letter = random.choice(['A', 'B', 'C', 'D', 'E'])
	# 	self.seat = f"{number}{letter}"


	def calc_total(self):
		total_add_on=0;
		print(f"this is {self.add_ons}")
		for add_on in self.add_ons:
			total_add_on+=add_on.amount or 0
		print(total_add_on)
		total_amount= self.flight_price + total_add_on
		return total_amount

	
	def unique_add_on_check(self):
		seen_items = set()
		for row in self.add_ons:
			if row.item in seen_items:
					frappe.throw(
					f"Add-on '{row.item}' has been added more than once. "
					"Please update in the earlier add on"
					)
			seen_items.add(row.item)

	def flight_status_check(self):
		if self.status != "Boarded":
			frappe.throw(
				"Ticket must be Boarded before submission"
			)


	pass
