import unittest
import os
from google import genai
from dotenv import load_dotenv

# This line loads the variables from your .env file into your system
load_dotenv()

class TestEnvironment(unittest.TestCase):
    def test_api_key_exists(self):
        # This will now find the key from your .env file
        self.assertIsNotNone(os.getenv("GOOGLE_API_KEY"), "API Key not found!")

    def test_sdk_installation(self):
        try:
            from google import genai
            self.assertTrue(True)
        except ImportError:
            self.fail("google-genai SDK not installed.")

if __name__ == "__main__":
    unittest.main()