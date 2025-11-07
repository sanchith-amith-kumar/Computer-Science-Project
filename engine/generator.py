from jinja2 import Environment, FileSystemLoader
import os

def generate_templates(rule_results: dict, output_dir="examples/output_terraform"):
    """
    Generates Terraform IaC templates using Jinja2 templates and rule-engine output.
    """
    os.makedirs(output_dir, exist_ok=True)
    env = Environment(loader=FileSystemLoader("./"))

    for name, data in rule_results.items():
        template = env.get_template(data["template"])
        rendered = template.render(**data["variables"])

        output_path = os.path.join(output_dir, f"{name}.tf")
        with open(output_path, "w") as f:
            f.write(rendered)
        print(f"[INFO] Generated {output_path}")
