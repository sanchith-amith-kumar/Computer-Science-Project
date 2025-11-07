import os
import unittest

class TestValidationScripts(unittest.TestCase):
    def test_validation_scripts_exist(self):
        self.assertTrue(os.path.exists("validation/validate.sh"))
        self.assertTrue(os.path.exists("validation/lint_rules.yaml"))
        self.assertTrue(os.path.exists("validation/checkov_policy.json"))

if __name__ == "__main__":
    unittest.main()
