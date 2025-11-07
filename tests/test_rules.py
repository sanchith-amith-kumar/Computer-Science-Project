import unittest
from engine.rule_engine import apply_rules

class TestRuleEngine(unittest.TestCase):
    def test_aws_compute_mapping(self):
        config = {"resources": [{"name": "web", "type": "compute", "provider": "aws"}]}
        result = apply_rules(config)
        self.assertIn("web", result)
        self.assertTrue(result["web"]["template"].startswith("templates/aws/"))

if __name__ == "__main__":
    unittest.main()
