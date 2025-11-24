import json
from typing import Dict

class ConfigParser:
    """
    Loads and validates example JSON configuration for IaC generation.
    Minimal validation included; extend as needed.
    """
    REQUIRED = ["provider", "region", "resources"]

    def load(self, path: str) -> Dict:
        with open(path, 'r') as f:
            data = json.load(f)
        for r in self.REQUIRED:
            if r not in data:
                raise ValueError(f"Missing required field: {r}")
        # Basic type checks
        if data['provider'].lower() != 'aws':
            raise ValueError('Prototype supports only provider = "aws"')
        return data
