#!/bin/bash
# Validation script for Terraform templates using Checkov and TFLint

echo "[INFO] Running validation checks..."

# Lint Terraform code
if command -v tflint &> /dev/null; then
  echo "[INFO] Running tflint..."
  tflint examples/output_terraform/
else
  echo "[WARN] tflint not installed. Skipping Terraform lint."
fi

# Run Checkov security policy checks
if command -v checkov &> /dev/null; then
  echo "[INFO] Running Checkov policy checks..."
  checkov -d examples/output_terraform/ -c validation/checkov_policy.json
else
  echo "[WARN] checkov not installed. Skipping security checks."
fi

echo "[INFO] Validation completed."
