# Copyright (c) 2025, 22Logic and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestTrip(FrappeTestCase):
	def setUp(self):
		"""Set up test data"""
		# Create test Trip Company
		self.trip_company = frappe.get_doc({
			"doctype": "Trip Company",
			"trip_company_name": "Test Taxi Company"
		})
		if not frappe.db.exists("Trip Company", {"trip_company_name": "Test Taxi Company"}):
			self.trip_company.insert()
		else:
			self.trip_company = frappe.get_doc("Trip Company", {"trip_company_name": "Test Taxi Company"})

		# Create test Trip Driver
		self.trip_driver = frappe.get_doc({
			"doctype": "Trip Driver",
			"driver_name": "John Driver",
			"phone_1": "+91-9876543210",
			"phone_2": "+91-9876543211",
			"trip_company": self.trip_company.name
		})
		if not frappe.db.exists("Trip Driver", {"driver_name": "John Driver"}):
			self.trip_driver.insert()
		else:
			self.trip_driver = frappe.get_doc("Trip Driver", {"driver_name": "John Driver"})

		# Create test Trip Customer
		self.trip_customer = frappe.get_doc({
			"doctype": "Trip Customer",
			"customer_name": "Jane Customer",
			"customer_phone": "+91-9876543200",
			"customer_address": "123 Test Street, Test City"
		})
		if not frappe.db.exists("Trip Customer", {"customer_name": "Jane Customer"}):
			self.trip_customer.insert()
		else:
			self.trip_customer = frappe.get_doc("Trip Customer", {"customer_name": "Jane Customer"})

	def test_create_trip(self):
		"""Test creating a new trip"""
		trip = frappe.get_doc({
			"doctype": "Trip",
			"customer": self.trip_customer.name,
			"pickup_location": "Airport",
			"destination": "Hotel Downtown",
			"trip_date": "2025-07-15",
			"trip_time": "10:00 AM",
			"round_trip__one_way": "One Way",
			"trip_status": "Booked",
			"trip_driver": self.trip_driver.name,
			"trip_company": self.trip_company.name,
			"trip_charge": 500.00,
			"trip_distance_km": 25.5
		})
		trip.insert()

		# Verify trip was created
		self.assertTrue(trip.name)
		self.assertEqual(trip.customer_name, "Jane Customer")
		self.assertEqual(trip.trip_driver_name, "John Driver")
		self.assertEqual(trip.trip_company_name, "Test Taxi Company")

	def test_trip_status_validation(self):
		"""Test trip status changes"""
		trip = frappe.get_doc({
			"doctype": "Trip",
			"customer": self.trip_customer.name,
			"pickup_location": "Station",
			"destination": "Office",
			"trip_date": "2025-07-16",
			"trip_time": "09:00 AM",
			"trip_status": "Booked",
			"trip_driver": self.trip_driver.name,
			"trip_company": self.trip_company.name
		})
		trip.insert()

		# Test status change to Completed
		trip.trip_status = "Completed"
		trip.save()
		self.assertEqual(trip.trip_status, "Completed")

		# Test status change to Cancelled
		trip.trip_status = "Cancelled"
		trip.save()
		self.assertEqual(trip.trip_status, "Cancelled")

	def test_payment_calculation(self):
		"""Test payment amount calculations"""
		trip = frappe.get_doc({
			"doctype": "Trip",
			"customer": self.trip_customer.name,
			"pickup_location": "Home",
			"destination": "Shopping Mall",
			"trip_date": "2025-07-17",
			"trip_time": "02:00 PM",
			"trip_status": "Booked",
			"trip_driver": self.trip_driver.name,
			"trip_company": self.trip_company.name,
			"trip_charge": 1000.00,
			"paid_amount": 300.00
		})
		trip.insert()

		# Check if to_be_paid is calculated correctly
		expected_to_be_paid = 1000.00 - 300.00
		self.assertEqual(trip.to_be_paid, expected_to_be_paid)

	def test_trip_with_full_payment(self):
		"""Test trip with full payment"""
		trip = frappe.get_doc({
			"doctype": "Trip",
			"customer": self.trip_customer.name,
			"pickup_location": "Office",
			"destination": "Home",
			"trip_date": "2025-07-18",
			"trip_time": "06:00 PM",
			"trip_status": "Completed",
			"trip_driver": self.trip_driver.name,
			"trip_company": self.trip_company.name,
			"trip_charge": 500.00,
			"paid_amount": 500.00,
			"paid_date": "2025-07-18",
			"mode_of_payment": "UPI"
		})
		trip.insert()

		# Check if to_be_paid is 0 when fully paid
		self.assertEqual(trip.to_be_paid, 0.00)

	def test_round_trip_creation(self):
		"""Test creating a round trip"""
		trip = frappe.get_doc({
			"doctype": "Trip",
			"customer": self.trip_customer.name,
			"pickup_location": "City Center",
			"destination": "Airport",
			"trip_date": "2025-07-19",
			"trip_time": "08:00 AM",
			"round_trip__one_way": "Round Trip",
			"trip_status": "Booked",
			"trip_driver": self.trip_driver.name,
			"trip_company": self.trip_company.name,
			"trip_charge": 1200.00,
			"trip_distance_km": 50.0
		})
		trip.insert()

		self.assertEqual(trip.round_trip__one_way, "Round Trip")
		self.assertEqual(trip.trip_distance_km, 50.0)

	def test_trip_company_auto_assignment(self):
		"""Test automatic trip company assignment based on user mapping"""
		# Create a user mapping for testing
		user_mapping = frappe.get_doc({
			"doctype": "Trip Company User Mapping",
			"user": "test@example.com",
			"trip_company": self.trip_company.name
		})
		if not frappe.db.exists("Trip Company User Mapping", {"user": "test@example.com"}):
			user_mapping.insert()

		# Create trip without specifying trip_company
		trip = frappe.get_doc({
			"doctype": "Trip",
			"customer": self.trip_customer.name,
			"pickup_location": "Test Location",
			"destination": "Test Destination",
			"trip_date": "2025-07-20",
			"trip_time": "11:00 AM",
			"trip_status": "Booked",
			"trip_driver": self.trip_driver.name
		})
		
		# Mock the session user for testing
		frappe.local.session.user = "test@example.com"
		trip.insert()

		# Verify trip_company was auto-assigned
		self.assertEqual(trip.trip_company, self.trip_company.name)

	def tearDown(self):
		"""Clean up test data"""
		# Clean up trips
		frappe.db.delete("Trip", {"customer": self.trip_customer.name})
		
		# Clean up test records
		frappe.db.delete("Trip Company User Mapping", {"user": "test@example.com"})
		frappe.db.delete("Trip Customer", {"customer_name": "Jane Customer"})
		frappe.db.delete("Trip Driver", {"driver_name": "John Driver"})
		frappe.db.delete("Trip Company", {"trip_company_name": "Test Taxi Company"})
		
		frappe.db.commit()
