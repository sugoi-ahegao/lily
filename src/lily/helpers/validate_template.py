from string import Template


def validate_template_identifiers(template: str, expected_identifiers: list[str]):
    template_identifiers = Template(template).get_identifiers()

    # Ensure no unexpected identifiers are present
    for template_identifier in template_identifiers:
        if template_identifier not in expected_identifiers:
            raise AssertionError(f"Template contains unexpected identifier: {template_identifier}")

    # Ensure all expected identifiers are present
    for expected_identifier in expected_identifiers:
        if expected_identifier not in template_identifiers:
            raise AssertionError(f"Template does not contain expected identifier: {expected_identifier}")
