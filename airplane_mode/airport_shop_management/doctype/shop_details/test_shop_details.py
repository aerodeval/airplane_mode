# Copyright (c) 2025, Sydney and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]

airport="Test International Airport"

def create_shop(shop_name, airport):
	return frappe.get_doc({
		"doctype": "Shop Details",
		"shop_name": shop_name,
		"airport": airport,
		"shop_contact": "email",
		"shop_type":"Stall"
	}).insert(ignore_links=True)


class IntegrationTestShopDetails(IntegrationTestCase):
	"""
	Integration tests for ShopDetails.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		print("setting up airport test")

	def test_create_airport(self):
			print("running test_create_airport")

			return frappe.get_doc({
				"doctype": "Airport",
				"name": "Test International Airport",
				"code": "TIA",
				"city": "Test City",
				"country": "Test Country",
				"shop_capacity": 3
			}).insert(ignore_permissions=True)


	def test_create_shop(self):
		create_shop("Shop A", airport)
		create_shop("Shop B", airport)
		create_shop("Shop C", airport)
		with self.assertRaises(frappe.exceptions.ValidationError) as exc:
			create_shop("Shop D", airport)

		self.assertIn(f"Cannot add shop: Airport '{airport}' has reached its full capacity of 3 shops.", str(exc.exception))
	


def tearDown(self):
    print("cleaning up airport test")
    frappe.set_user("Administrator")

    for name in frappe.get_all(
        "Shop",
        filters={"airport": self.airport.name},
        pluck="name"
    ):
        frappe.delete_doc("Shop Details", name, force=1)

    frappe.delete_doc("Airport", self.airport.name, force=1)
