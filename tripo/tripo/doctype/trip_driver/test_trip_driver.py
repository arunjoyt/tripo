# Copyright (c) 2025, 22Logic and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestTripDriver(FrappeTestCase):
	def setUp(self):
		"""Set up test data"""
		# Create test Trip Company
		self.trip_company = frappe.get_doc({
			"doctype": "Trip Company",
			"trip_company_name": "Test Driver Company"
		})
		if not frappe.db.exists("Trip Company", {"trip_company_name": "Test Driver Company"}):
			self.trip_company.insert()
		else:
			self.trip_company = frappe.get_doc("Trip Company", {"trip_company_name": "Test Driver Company"})

	def test_create_driver(self):
		"""Test creating a new driver"""
		driver = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "Test Driver 1",
			"phone_1": "+91-9876543210",
			"phone_2": "+91-9876543211",
			"trip_company": self.trip_company.name
		})
		driver.insert()

		# Verify driver was created
		self.assertTrue(driver.name)
		self.assertEqual(driver.driver_name, "Test Driver 1")
		self.assertEqual(driver.trip_company_name, "Test Driver Company")

	def test_driver_phone_validation(self):
		"""Test driver phone number validation"""
		driver = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "Test Driver 2",
			"phone_1": "+91-9876543220",
			"trip_company": self.trip_company.name
		})
		driver.insert()

		# Verify phone number is stored correctly
		self.assertEqual(driver.phone_1, "+91-9876543220")

	def test_driver_company_association(self):
		"""Test driver-company association"""
		driver = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "Test Driver 3",
			"phone_1": "+91-9876543230",
			"trip_company": self.trip_company.name
		})
		driver.insert()

		# Verify company name is fetched correctly
		self.assertEqual(driver.trip_company, self.trip_company.name)
		self.assertEqual(driver.trip_company_name, "Test Driver Company")

	def test_driver_without_company(self):
		"""Test creating driver without company"""
		driver = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "Independent Driver",
			"phone_1": "+91-9876543240"
		})
		driver.insert()

		# Verify driver can be created without company
		self.assertTrue(driver.name)
		self.assertEqual(driver.driver_name, "Independent Driver")

	def test_duplicate_driver_name(self):
		"""Test handling of duplicate driver names"""
		# Create first driver
		driver1 = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "Duplicate Name",
			"phone_1": "+91-9876543250",
			"trip_company": self.trip_company.name
		})
		driver1.insert()

		# Create second driver with same name but different phone
		driver2 = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "Duplicate Name",
			"phone_1": "+91-9876543251",
			"trip_company": self.trip_company.name
		})
		driver2.insert()

		# Both should be created successfully (no unique constraint on name)
		self.assertTrue(driver1.name)
		self.assertTrue(driver2.name)
		self.assertNotEqual(driver1.name, driver2.name)

	def tearDown(self):
		"""Clean up test data"""
		# Clean up drivers
		frappe.db.delete("Trip Driver", {"trip_company": self.trip_company.name})
		frappe.db.delete("Trip Driver", {"driver_name": "Independent Driver"})
		frappe.db.delete("Trip Driver", {"driver_name": "Duplicate Name"})
		
		# Clean up company
		frappe.db.delete("Trip Company", {"trip_company_name": "Test Driver Company"})
		
		frappe.db.commit()
