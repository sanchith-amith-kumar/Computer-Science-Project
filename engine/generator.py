import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict

class TemplateGenerator:
    def __init__(self, template_path: str):
        # relative path expected
        self.env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True)

    def generate(self, modules: list, variables: Dict, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        # Render module templates
        for mod in modules:
            tpl_name = f"{mod}.tf.j2"
            try:
                tpl = self.env.get_template(tpl_name)
            except Exception as e:
                raise FileNotFoundError(f"Template not found: {tpl_name} in template path") from e
            rendered = tpl.render(**variables)
            out_path = os.path.join(output_dir, f"{mod}.tf")
            with open(out_path, 'w') as f:
                f.write(rendered)

        # Render common templates if present
        for common_tpl in ['variables.tf.j2', 'outputs.tf.j2', 'provider.tf.j2']:
            try:
                tpl = self.env.get_template(common_tpl)
                rendered = tpl.render(**variables)
                out_path = os.path.join(output_dir, common_tpl.replace('.j2',''))
                with open(out_path, 'w') as f:
                    f.write(rendered)
            except:
                # optional
                continue
