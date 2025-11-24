import os
import subprocess
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List

class TemplateGenerator:
    def __init__(self, template_path: str):
        """
        Initializes the Jinja2 environment.
        :param template_path: relative path to templates folder
        """
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def run_terraform_fmt(self, tf_path: str):
        """
        Runs 'terraform fmt' on a file or directory to ensure correct formatting.
        """
        subprocess.run(['terraform', 'fmt', tf_path], check=False)

    def generate(self, modules: List[str], variables: Dict, output_dir: str):
        """
        Generates Terraform files from Jinja2 templates.
        :param modules: list of module names to generate (without .tf.j2)
        :param variables: dictionary of variables for template rendering
        :param output_dir: directory to write generated files
        """
        os.makedirs(output_dir, exist_ok=True)

        # Render module templates
        for mod in modules:
            tpl_name = f"{mod}.tf.j2"
            try:
                tpl = self.env.get_template(tpl_name)
            except Exception as e:
                raise FileNotFoundError(f"Template not found: {tpl_name} in {self.env.loader.searchpath}") from e

            rendered = tpl.render(**variables)
            out_path = os.path.join(output_dir, f"{mod}.tf")
            with open(out_path, 'w') as f:
                f.write(rendered)

            # Auto-format each file
            self.run_terraform_fmt(out_path)

        # Render common templates if present
        for common_tpl in ['variables.tf.j2', 'outputs.tf.j2', 'provider.tf.j2']:
            try:
                tpl = self.env.get_template(common_tpl)
                rendered = tpl.render(**variables)
                out_path = os.path.join(output_dir, common_tpl.replace('.j2', ''))
                with open(out_path, 'w') as f:
                    f.write(rendered)

                # Auto-format common files
                self.run_terraform_fmt(out_path)
            except:
                # optional templates may not exist
                continue

        # Optional: format entire directory at the end
        self.run_terraform_fmt(output_dir)
