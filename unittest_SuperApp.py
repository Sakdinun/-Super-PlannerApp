import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch

# Import the Bl and Ui classes from the module where they are defined
from SuperApp import Bl, Ui

class TestBlClass(unittest.TestCase):

    def setUp(self):
        """Set up the Bl object for testing"""
        self.bl = Bl()

    def test_add_event_valid(self):
        """Test adding a valid event"""
        event_name = "Meeting"
        start_time = "12-12-2024 10:00"
        end_time = "12-12-2024 11:00"
        result = self.bl.add_bl(event_name, start_time, end_time)
        self.assertEqual(result, f"Added event '{event_name}' from {datetime.strptime(start_time, '%d-%m-%Y %H:%M'):%Y-%m-%d %H:%M:%S} to {datetime.strptime(end_time, '%d-%m-%Y %H:%M'):%Y-%m-%d %H:%M:%S}.")
        self.assertEqual(len(self.bl.events), 1)

    def test_add_event_invalid_time(self):
        """Test adding an event with invalid time (start time after end time)"""
        event_name = "Meeting"
        start_time = "12-12-2024 10:00"
        end_time = "12-12-2024 09:00"
        result = self.bl.add_bl(event_name, start_time, end_time)
        self.assertEqual(result, "End time must be after start time. Please try again.")
        self.assertEqual(len(self.bl.events), 0)

    def test_add_event_invalid_format(self):
        """Test adding an event with invalid date format"""
        event_name = "Meeting"
        start_time = "12-12-2024 10:00"
        end_time = "12-12-2024 25:00"  # Invalid hour
        result = self.bl.add_bl(event_name, start_time, end_time)
        self.assertEqual(result, "Invalid date format. Please try again.")
        self.assertEqual(len(self.bl.events), 0)

    def test_remove_event_valid(self):
        """Test removing a valid event"""
        event_name = "Meeting"
        start_time = "12-12-2024 10:00"
        end_time = "12-12-2024 11:00"
        self.bl.add_bl(event_name, start_time, end_time)
        result = self.bl.remove_bl(1)
        self.assertEqual(result, f"Removed event: {event_name}")
        self.assertEqual(len(self.bl.events), 0)

    def test_remove_event_invalid(self):
        """Test removing an event with an invalid index"""
        result = self.bl.remove_bl(1)
        self.assertEqual(result, "Invalid selection. Please try again.")


class TestUiClass(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "user1", "password", "password"])
    def test_register_user(self, mock_input):
        """Test the registration functionality"""
        ui = Ui(self.bl)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ui.register()
            output = mock_stdout.getvalue()
        self.assertIn("You have successfully registered!", output)

    @patch("builtins.input", side_effect=["1", "user1", "password", "password"])
    def test_login_user(self, mock_input):
        """Test the login functionality"""
        ui = Ui(self.bl)
        ui.userData = [{"user1": "password"}]  # Mock user data
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ui.login()
            output = mock_stdout.getvalue()
        self.assertIn("Welcome user1!!", output)

    @patch("builtins.input", side_effect=["2", "user1", "password", "password", "1", "event1", "12-12-2024 10:00", "12-12-2024 11:00"])
    def test_add_event(self, mock_input):
        """Test adding an event through the UI"""
        ui = Ui(self.bl)
        ui.userData = [{"user1": "password"}]  # Mock user data
        ui.login()  # Log in user first
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ui.add()  # Adding event
            output = mock_stdout.getvalue()
        self.assertIn("You have entered the event: event1", output)
        self.assertEqual(len(self.bl.events), 1)

    @patch("builtins.input", side_effect=["3", "1"])
    def test_remove_event(self, mock_input):
        """Test removing an event through the UI"""
        ui = Ui(self.bl)
        ui.userData = [{"user1": "password"}]  # Mock user data
        ui.login()  # Log in user first
        ui.add()  # Add an event first
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ui.remove()  # Remove event
            output = mock_stdout.getvalue()
        self.assertIn("Removed event:", output)
        self.assertEqual(len(self.bl.events), 0)

    @patch("builtins.input", side_effect=["3", "y"])
    def test_exit(self, mock_input):
        """Test the exit functionality"""
        ui = Ui(self.bl)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ui.exit()
            output = mock_stdout.getvalue()
        self.assertIn("Thank you for using our Planner App!!", output)


if __name__ == "__main__":
    unittest.main()
