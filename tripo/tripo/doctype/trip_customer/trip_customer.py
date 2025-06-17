# Copyright (c) 2025, 22Logic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re

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

		# validate customer_phone
		phone = self.customer_phone
		if phone:
			phone = phone.strip()

            # Add +91 if no country code is present
			if not phone.startswith('+'):
				phone = f'+91 {phone}'

            # Normalize dash to space
			phone = re.sub(r'-', ' ', phone)

            # Validate the phone format (international)
			if not re.match(r'^\+\d{1,4}\s?\d{6,15}$', phone):
				frappe.throw(_("Customer Phone must be a valid number, e.g., +91 9876543210"))

            # Save back the normalized phone
			self.customer_phone = phone
