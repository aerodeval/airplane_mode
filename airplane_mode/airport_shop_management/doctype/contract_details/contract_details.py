# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ContractDetails(Document):
	def before_insert(self):
		settings = frappe.get_single("Shop Management Settings")
		if self.rent_amount < settings.default_rent_amount:
			frappe.throw(f"Cannot be less than default amount set by user. Must be higher than {settings.default_rent_amount}")