import unittest
import os
import json
from utilities.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    """ Unit tests for AI-driven error logging and debugging """

    @classmethod
    def setUpClass(cls):
        """ Initialize ErrorHandler and setup test logs """
        cls.error_handler = ErrorHandler()
        cls.test_log_file = cls.error_handler.error_log_file

        # Ensure test log file is reset
        if os.path.exists(cls.test_log_file):
            os.remove(cls.test_log_file)

    def test_log_error(self):
        """ Ensure AI correctly logs an error """
        self.error_handler.log_error("Test Error Message", error_type="TestError", source="TestModule")

        # Verify log file was created
        self.assertTrue(os.path.exists(self.test_log_file), "Error log file should be created")

        # Verify error was logged
        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertGreater(len(logs), 0, "Error log should not be empty")
        self.assertEqual(logs[-1]["type"], "TestError", "Error type should match logged type")
        self.assertEqual(logs[-1]["source"], "TestModule", "Error source should match logged source")

    def test_handle_exception(self):
        """ Ensure AI logs exceptions with traceback details """
        try:
            raise ValueError("Test Exception")
        except Exception as e:
            self.error_handler.handle_exception(e, source="TestModule")

        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertGreater(len(logs), 1, "Exception should be logged")
        self.assertIn("Exception", logs[-1]["type"], "Exception should be categorized correctly")

    def test_retrieve_recent_errors(self):
        """ Validate AI fetches recent error logs correctly """
        recent_errors = self.error_handler.get_recent_errors(limit=2)

        self.assertIsInstance(recent_errors, list, "Recent errors should return a list")
        self.assertLessEqual(len(recent_errors), 2, "Returned errors should not exceed requested limit")

if __name__ == "__main__":
    unittest.main()
