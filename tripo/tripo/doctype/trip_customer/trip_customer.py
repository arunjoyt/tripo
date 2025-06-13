# Copyright (c) 2025, 22Logic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class TripCustomer(Document):
	def validate(self):
		if not self.trip_company:
			trip_company = frappe.get_value(
				"Trip Company User Mapping",
				{"user": frappe.session.user},
				"trip_company"
			)

			if not trip_company:
				frappe.throw(_("No Trip Company mapping found for the logged-in user ({0})").format(frappe.session.user))

			self.trip_company = trip_company
