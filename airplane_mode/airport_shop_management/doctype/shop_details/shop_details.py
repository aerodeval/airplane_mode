# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopDetails(Document):

	def on_change(self):

		airport = frappe.get_doc('Airport', self.airport)
		current_shops = frappe.get_all(
			"Shop Details",
			filters={"Airport": airport.name},
			fields=["Tenant"]
		)

		shop_capacity=airport.shop_capacity

		# print(f'{current_shops} :current shop' )
		# print(f'{shop_capacity} :shop' )
		available_shops = int(shop_capacity) - len(current_shops)
		
		frappe.db.set_value("Airport", self.airport, "shop_availibility", available_shops)

