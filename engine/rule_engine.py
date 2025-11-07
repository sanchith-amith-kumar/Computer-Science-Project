def apply_rules(config: dict) -> dict:
    """
    Applies logical rules to map user input into cloud-specific infrastructure patterns.
    Example: converts generic compute definition to AWS EC2 or GCP VM templates.
    """
    rules_output = {}

    for resource in config.get("resources", []):
        resource_type = resource.get("type")
        provider = resource.get("provider")

        if provider == "aws":
            rules_output[resource["name"]] = {
                "template": "templates/aws/ec2.tf.j2" if resource_type == "compute" else "templates/aws/vpc.tf.j2",
                "variables": resource
            }
        elif provider == "gcp":
            rules_output[resource["name"]] = {
                "template": "templates/gcp/compute.tf.j2",
                "variables": resource
            }
        elif provider == "azure":
            rules_output[resource["name"]] = {
                "template": "templates/azure/vm.tf.j2",
                "variables": resource
            }
    return rules_output
