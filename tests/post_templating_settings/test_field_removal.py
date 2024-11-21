from lily.process_video_file import remove_fields_from_template


class TestRemoveFieldsFromTemplate:
    def test_removing_single_field_from_template(self):
        template_string = "Scene Title: ${title}"

        fields_to_remove = ["title"]

        assert remove_fields_from_template(template_string, fields_to_remove) == "Scene Title: "

    def test_removing_multiple_fields_from_template(self):
        template_string = "Scene Title: ${title} ${date}"

        fields_to_remove = ["title", "date"]

        assert remove_fields_from_template(template_string, fields_to_remove) == "Scene Title:  "

    def test_removing_no_fields_from_template(self):
        template_string = "Scene Title: ${title} ${date}"

        fields_to_remove: list[str] = []

        assert remove_fields_from_template(template_string, fields_to_remove) == "Scene Title: ${title} ${date}"

    def test_removing_nonexistent_field_from_template(self):
        template_string = "Scene Title: ${title} ${date}"

        fields_to_remove = ["performers"]

        assert remove_fields_from_template(template_string, fields_to_remove) == template_string

    def test_removing_field_in_the_middle_of_the_template(self):
        template_string = "Scene Title: ${title} ${date}"

        fields_to_remove = ["date"]

        assert remove_fields_from_template(template_string, fields_to_remove) == "Scene Title: ${title} "
