from unittest.mock import patch
import unittest
from SuperApp import Bl, Ui  # Import the classes from your SuperApp.py
from unittest.mock import patch


class TestMethods(unittest.TestCase):

    def setUp(self):
        """Set up test cases"""
        self.bl = Bl()

    def test_add_event_success(self):
        result = self.bl.add_bl("Test Event", "12-12-2024 09:00", "12-12-2024 10:00")
        self.assertEqual(result, "Added event 'Test Event' from 2024-12-12 09:00:00 to 2024-12-12 10:00:00.")
        self.assertEqual(len(self.bl.events), 1)
        self.assertEqual(self.bl.events[0]['EventName'], "Test Event")

    def test_add_event_invalid_date_format(self):
        result = self.bl.add_bl("Test Event", "12-12-2024 09:00", "2024-12-12 10:00")  # Incorrect format
        self.assertEqual(result, "Invalid date format. Please try again.")
        self.assertEqual(len(self.bl.events), 0)

    def test_end_time_before_start_time(self):
        result = self.bl.add_bl("Test Event", "12-12-2024 10:00", "12-12-2024 09:00")
        self.assertEqual(result, "End time must be after start time. Please try again.")
        self.assertEqual(len(self.bl.events), 0)

    def test_remove_event_success(self):
        self.bl.add_bl("Test Event", "12-12-2024 09:00", "12-12-2024 10:00")
        result = self.bl.remove_bl(1)
        self.assertEqual(result, "Removed event: Test Event")
        self.assertEqual(len(self.bl.events), 0)

    def test_remove_event_invalid_index(self):
        result = self.bl.remove_bl(1)
        self.assertEqual(result, "Invalid selection. Please try again.")

    def test_check_empty(self):
        result = self.bl.check_empty("", "password")
        self.assertEqual(result, ">> Please enter your username and password.")

    def test_check_password_mismatch(self):
        result = self.bl.bl_check_password("password", "differentpassword")
        self.assertEqual(result, ">> Passwords don't match. Please try again.")

    def test_calculate_duration(self):
        self.bl.add_bl("Test Event", "12-12-2024 09:00", "12-12-2024 10:15")
        duration = self.bl.calculate_duration(self.bl.events[0])
        self.assertEqual(duration, "1:15 hours")

if __name__ == "__main__":
    unittest.main()
