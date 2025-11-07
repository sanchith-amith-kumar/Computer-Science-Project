import json
import yaml

def parse_input(file_path: str) -> dict:
    """
    Parses a user-provided input configuration file in JSON or YAML format.
    Returns the configuration as a Python dictionary.
    """
    try:
        if file_path.endswith(".json"):
            with open(file_path, "r") as f:
                return json.load(f)
        elif file_path.endswith((".yaml", ".yml")):
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported input format. Use JSON or YAML.")
    except Exception as e:
        print(f"[ERROR] Failed to parse {file_path}: {e}")
        return {}
