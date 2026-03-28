import unittest
from script_gen import ScriptGenerator

class TestScriptGen(unittest.TestCase):
    def setUp(self):
        self.gen = ScriptGenerator()

    def test_script_has_all_parts(self):
        result = self.gen.generate_viral_script("Coffee")
        # Ensure the AI didn't forget any part of the viral structure
        self.assertIn('hook', result)
        self.assertIn('mystery', result)
        self.assertIn('reveal', result)
        self.assertIn('cta', result)

if __name__ == "__main__":
    unittest.main()