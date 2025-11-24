from typing import Dict, Any

class RuleEngine:
    """
    Decides which template modules to include based on input config.
    Contains rules for AWS: VPC, EC2, ALB, S3, RDS (optional), IAM.
    Returns:
        dict with template_path and variables to render
    """
    def process(self, config: Dict[str, Any]) -> Dict[str, Any]:
        provider = config['provider'].lower()
        env = config.get('environment', 'dev')
        resources = config.get('resources', {})

        # Base variables
        vars = {
            'provider': provider,
            'environment': env,
            'region': config.get('region', 'us-east-1'),
            'vpc_cidr': config.get('vpc_cidr', '10.0.0.0/16'),
            'instance_type': resources.get('instance_type', 't3.micro'),
            'instance_count': resources.get('count', 2),
            'enable_rds': resources.get('rds', False),
            'db_engine': resources.get('db_engine', 'postgres'),
            'db_instance_class': resources.get('db_instance_class', 'db.t3.micro'),
            'enable_s3': resources.get('s3', True),
            'enable_alb': resources.get('alb', True),
            'tags': {
                'Project': 'IntelligentIaC',
                'Env': env
            }
        }

        # Decide which modules to include
        modules = ['vpc', 'ec2', 'iam']
        if vars['enable_s3']:
            modules.append('s3')
        if vars['enable_alb']:
            modules.append('alb')
        if vars['enable_rds']:
            modules.append('rds')

        return {
            'template_path': f'templates/{provider}/',
            'variables': vars,
            'modules': modules
        }
