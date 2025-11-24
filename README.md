# Intelligent IaC Generator - Full Prototype

This repository contains a runnable prototype that generates Terraform configurations for AWS
based on a parameterized JSON input. It includes a rule engine that decides which modules
to include (VPC, EC2, S3, ALB, RDS, IAM) and a validation flow using Terraform CLI.

See `main.py` for the runtime entry point:
`python main.py --config examples/input_aws.json --out output`

Requirements:
- Python 3.8+
- Jinja2 (`pip install Jinja2`)
- Terraform installed for validation
