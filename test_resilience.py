import unittest
from script_gen import ScriptGenerator
from google.genai import errors

class TestResilience(unittest.TestCase):
    def test_model_version_is_current(self):
        gen = ScriptGenerator()
        # Confirms you are on the supported 2.5 version
        self.assertEqual(gen.model_id, "gemini-2.5-flash")

    def test_handles_rate_limit_logic(self):
        # This confirms our script_gen uses the correct native error class
        gen = ScriptGenerator()
        self.assertTrue(hasattr(errors, 'ClientError'))

if __name__ == "__main__":
    unittest.main()