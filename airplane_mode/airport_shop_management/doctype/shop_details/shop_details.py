# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopDetails(Document):

  def validate(self):
        airport = frappe.get_doc('Airport', self.airport)
        current_shops = frappe.get_all(
            "Shop Details",
            filters={"airport": airport.name},
            fields=["name"]
        )

        shop_capacity = airport.shop_capacity
        available_shops = int(shop_capacity) - len(current_shops)

        if available_shops <= 0:
            frappe.throw(
                f"Cannot add shop: Airport '{airport.name}' has reached its full capacity of {shop_capacity} shops."
            )
		# Update airport availability
        frappe.db.set_value("Airport", airport.name, "shop_availibility", max(available_shops - 1, 0))