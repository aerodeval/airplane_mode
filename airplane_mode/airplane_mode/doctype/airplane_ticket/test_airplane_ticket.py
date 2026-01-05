# Copyright (c) 2025, Sydney and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase
import frappe
import random
from frappe.utils import random_string
import frappe.defaults

from frappe.tests.utils import FrappeTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


FLIGHT = "Indigo-001-01-2026-00002"
PASSENGER = "Miles Morales"
ERROR_MSG="The number of tickets for that flight have exceeded, we're sorry."
OCC_MSG="Seat 1A has already been booked for this flight"


# def create_passenger():
# 	if not frappe.db.exists("Passenger", PASSENGER):
# 		frappe.get_doc({
# 			"doctype": "Flight Passenger",
# 			"first_name": "Miles",
# 			"last_name": "Tyson",
# 			"date_of_birth": "2026-01-01",
# 		}).insert(ignore_permissions=True)

def create_ticket(seat):
	print(frappe.session.user)
	frappe.set_user("Administrator")
	return frappe.get_doc({
		"doctype": "Airplane Ticket",
		"flight": FLIGHT,
		"passenger": PASSENGER,
		"status": "Booked",
		"seat": "1234567890",
		"gate": "1234567890",
		"source_airport_code": "1234567890",
		"destination_airport_code": "1234567890",
		"flight_price": 100,
		"total_amount": 100,
		"seat": seat,
		"departure_date": "2026-01-01",
		"departure_time": "12:00:00",
		"duration_of_flight": 120,
	}).insert(ignore_links=True)
	
def cleanup():
	frappe.set_user("Administrator")

	for name in frappe.get_all("Airplane Ticket", filters={"flight": FLIGHT}, pluck="name"):
		frappe.delete_doc("Airplane Ticket", name, force=1)


# def create_events():
# 	print("create events")
# 	if frappe.flags.test_events_created:
# 		return

# 	frappe.set_user("Administrator")
# 	doc = frappe.get_doc({
# 	"doctype": "City",
# 	"city_name":"_Test Event 1",
# 	"country": "India",
# 	})
# 	doc.insert()
# 	doc.save()
# 	frappe.flags.test_events_created = True

# def create_shops():
# 	print("Shops created")
# 	if frappe.flags.test_shops_created:
# 		return
# 	frappe.set_user("Administrator")
# 	doc = frappe.get_doc({
# 		"doctype": "Shop",
# 		"shop_name": "Test Shop",
# 	})
# 	doc.insert(ignore_links=True)
# 	doc.save()
# 	frappe.flags.test_shops_created = True	


# def create_tickets():
# 	print("Tickets created")
# 	if frappe.flags.test_events_created:
# 		return

# 	frappe.set_user("Administrator")
# 	doc = frappe.get_doc({
# 		"doctype": "Airplane Ticket",
# 		"flight": "Indigo-001-01-2026-00002",
# 		"passenger": "Miles",
# 		"status": "Booked",
# 		"seat": "1234567890",
# 		"gate": "1234567890",
# 		"source_airport_code": "1234567890",
# 		"destination_airport_code": "1234567890",
# 		"flight_price": 100,
# 		"total_amount": 100,
# 		"departure_date": "2026-01-01",
# 		"departure_time": "12:00:00",
# 		"duration_of_flight": 120,
# 	})
# 	doc.insert(ignore_links=True)
# 	frappe.db.commit()
# 	frappe.flags.test_events_created = True


class IntegrationTestAirplaneTicket(IntegrationTestCase):
	"""
	Integration tests for AirplaneTicket.
	Use this class for testing interactions between multiple components.
	"""
	def setUp(self):
		
		print("setting up new test")		
		# print(frappe.session.user)
		# frappe.set_user("Administrator")
		# create_passenger()

	def test_occupied_ticket(self):
		print("ran test occupied ticket")
		create_ticket("1A")
		with self.assertRaises(frappe.exceptions.ValidationError) as exc:
			create_ticket("1A")

		self.assertIn(OCC_MSG, str(exc.exception))



	def test_max_ticket_limit_on_flight(self):
		print("ran test ticket limit exceed")

		create_ticket("1A")
		create_ticket("1B")
		create_ticket("1C")
		
		with self.assertRaises(frappe.exceptions.ValidationError) as exc:
			create_ticket("1D")

		self.assertIn(ERROR_MSG, str(exc.exception))
	
	def tearDown(self):
		print("cleaning out data")
		cleanup()
		