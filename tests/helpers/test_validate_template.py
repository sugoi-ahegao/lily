import pytest
from src.lily.helpers.validate_template import validate_template_identifiers


class TestValidateTemplateIdentifiers:
    def test_simple_template(self):
        template = "${title}"
        expected_identifiers = ["title"]

        validate_template_identifiers(template, expected_identifiers)

    def test_all_expected_identifiers_present(self):
        template = "${title} ${date}"
        expected_identifiers = ["title", "date"]

        validate_template_identifiers(template, expected_identifiers)

    def test_unexpected_identifier(self):
        template = "${title} ${date}"
        expected_identifiers = ["title"]

        with pytest.raises(AssertionError):
            validate_template_identifiers(template, expected_identifiers)

    def test_missing_identifier(self):
        template = "${title}"
        expected_identifiers = ["title", "date"]

        with pytest.raises(AssertionError):
            validate_template_identifiers(template, expected_identifiers)
