#!/bin/bash
set -e
if ! command -v terraform &> /dev/null
then
  echo "terraform could not be found, please install terraform to run validation."
  exit 2
fi
OUT_DIR="${1:-output}"
echo "Validating Terraform files in ${OUT_DIR}"
cd "${OUT_DIR}"
terraform fmt -check || terraform fmt
terraform init -backend=false
terraform validate
