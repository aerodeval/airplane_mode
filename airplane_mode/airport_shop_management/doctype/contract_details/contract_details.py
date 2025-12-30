# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ContractDetails(Document):

	def before_insert(self):
		settings = frappe.get_single("Shop Management Settings")
		if self.rent_amount < settings.default_rent_amount:
			frappe.throw(f"Cannot be less than default amount set by user. Must be higher than {settings.default_rent_amount}")

	def after_insert(self):
		self.create_rent_payment()

	def create_rent_payment(self):
		print("rent reciept created")
		rent_doc=frappe.new_doc("Rent Payment")
		rent_doc.contract = self.shop_name
		rent_doc.tenant= self.tenant
		rent_doc.data_eite = self.shop_name
		rent_doc.payment_date = self.date_of_expiry
		rent_doc.amount_paid = self.rent_amount
		rent_doc.payment_status = "Pending"
		rent_doc.insert(ignore_permissions=True)

	