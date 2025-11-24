import os
import shutil
import unittest
from engine.parser import ConfigParser
from engine.rule_engine import RuleEngine
from engine.generator import TemplateGenerator
from engine.validator import Validator

class TestIaCGenerator(unittest.TestCase):

    def setUp(self):
        self.config_path = "examples/input_aws.json"
        self.output_dir = "tests/test_output"
        os.makedirs(self.output_dir, exist_ok=True)

        self.parser = ConfigParser()
        self.config = self.parser.load(self.config_path)
        self.engine = RuleEngine()

    def tearDown(self):
        # Clean up generated files
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_rule_engine_modules(self):
        """Check that correct modules are selected based on input"""
        plan = self.engine.process(self.config)
        expected_modules = ['vpc', 'ec2', 'iam', 's3', 'alb']  # as per input_aws.json defaults
        self.assertListEqual(sorted(plan['modules']), sorted(expected_modules))

    def test_template_generation(self):
        """Check that all template files are generated"""
        plan = self.engine.process(self.config)
        generator = TemplateGenerator(plan['template_path'])
        generator.generate(plan['modules'], plan['variables'], self.output_dir)

        generated_files = os.listdir(self.output_dir)
        expected_files = [f"{m}.tf" for m in plan['modules']] + ['variables.tf', 'outputs.tf', 'provider.tf']
        for f in expected_files:
            self.assertIn(f, generated_files)

    def test_validator_passes(self):
        """Check that generated Terraform passes basic validation"""
        plan = self.engine.process(self.config)
        generator = TemplateGenerator(plan['template_path'])
        generator.generate(plan['modules'], plan['variables'], self.output_dir)

        validator = Validator(self.output_dir)
        results = validator.validate()
        # Ensure the last command (validate) succeeded
        self.assertEqual(results[-1]['rc'], 0)

if __name__ == "__main__":
    unittest.main()
