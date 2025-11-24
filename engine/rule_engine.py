from typing import Dict, Any, List

class RuleEngine:
    """
    Decides which template modules to include based on input config.
    Supports AWS: VPC, EC2, ALB, S3, RDS, Lambda, DynamoDB, CloudFront, Route53, CloudWatch, Secrets.
    Returns:
        dict with template_path and variables to render
    """
    # Mapping resource keys to template module names
    MODULE_MAP = {
        'vpc': 'vpc',
        'ec2': 'ec2',
        'alb': 'alb',
        's3': 's3',
        'rds': 'rds',
        'iam': 'iam',
        'lambda': 'lambda',
        'dynamodb': 'dynamodb',
        'cloudfront': 'cloudfront',
        'route53': 'route53',
        'cloudwatch': 'cloudwatch',
        'secrets': 'secrets'
    }

    def process(self, config: Dict[str, Any], selected_service: str = None) -> Dict[str, Any]:
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
            'enable_lambda': resources.get('lambda', False),
            'enable_dynamodb': resources.get('dynamodb', False),
            'enable_cloudfront': resources.get('cloudfront', False),
            'enable_route53': resources.get('route53', False),
            'enable_cloudwatch': resources.get('cloudwatch', False),
            'enable_secrets': resources.get('secrets', False),
            'tags': {
                'Project': 'IntelligentIaC',
                'Env': env
            }
        }

        # Decide which modules to include
        modules: List[str] = ['vpc', 'ec2', 'iam']
        optional_modules = [
            ('s3', vars['enable_s3']),
            ('alb', vars['enable_alb']),
            ('rds', vars['enable_rds']),
            ('lambda', vars['enable_lambda']),
            ('dynamodb', vars['enable_dynamodb']),
            ('cloudfront', vars['enable_cloudfront']),
            ('route53', vars['enable_route53']),
            ('cloudwatch', vars['enable_cloudwatch']),
            ('secrets', vars['enable_secrets'])
        ]

        for mod_name, enabled in optional_modules:
            if enabled:
                modules.append(self.MODULE_MAP[mod_name])

        # Filter by single selected service if provided
        if selected_service:
            if selected_service in modules:
                modules = [selected_service]
            else:
                raise ValueError(f"Service '{selected_service}' is not available or not enabled in config.")

        return {
            'template_path': f'templates/{provider}/',
            'variables': vars,
            'modules': modules
        }
