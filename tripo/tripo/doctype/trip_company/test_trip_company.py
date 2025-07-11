# Copyright (c) 2025, 22Logic and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestTripCompany(FrappeTestCase):
	def test_create_trip_company(self):
		"""Test creating a new trip company"""
		company = frappe.get_doc({
			"doctype": "Trip Company",
			"trip_company_name": "Test Taxi Company 1"
		})
		company.insert()

		# Verify company was created
		self.assertTrue(company.name)
		self.assertEqual(company.trip_company_name, "Test Taxi Company 1")

	def test_duplicate_company_name(self):
		"""Test creating companies with duplicate names"""
		# Create first company
		company1 = frappe.get_doc({
			"doctype": "Trip Company",
			"trip_company_name": "Duplicate Company"
		})
		company1.insert()

		# Try to create second company with same name
		company2 = frappe.get_doc({
			"doctype": "Trip Company",
			"trip_company_name": "Duplicate Company"
		})
		
		# This should succeed (no unique constraint in current setup)
		company2.insert()
		self.assertTrue(company2.name)
		self.assertNotEqual(company1.name, company2.name)

	def test_required_fields(self):
		"""Test that required fields are validated"""
		# Try to create company without name (should fail)
		with self.assertRaises(frappe.exceptions.MandatoryError):
			company = frappe.get_doc({
				"doctype": "Trip Company"
			})
			company.insert()

	def test_company_name_formatting(self):
		"""Test company name formatting and storage"""
		company = frappe.get_doc({
			"doctype": "Trip Company",
			"trip_company_name": "  Test Company With Spaces  "
		})
		company.insert()

		# Company name should be stored as-is (Frappe handles trimming)
		self.assertEqual(company.trip_company_name, "  Test Company With Spaces  ")

	def tearDown(self):
		"""Clean up test data"""
		# Clean up test companies
		frappe.db.delete("Trip Company", {"trip_company_name": "Test Taxi Company 1"})
		frappe.db.delete("Trip Company", {"trip_company_name": "Duplicate Company"})
		frappe.db.delete("Trip Company", {"trip_company_name": "  Test Company With Spaces  "})
		
		frappe.db.commit()
