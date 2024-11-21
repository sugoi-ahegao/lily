from lily.fields.studio_hierarchy_as_path_field import (
    StudioHierarchyAsPathFieldSettings,
    format_studio_hierarchy_as_path_field,
)
from tests.testing_model_creators.create_studio import create_studio


class TestStudioHierarchyAsPathField:
    def test_formats_studio_hierarchy_as_path_correctly(self):
        studio1 = create_studio()
        studio2 = create_studio(parent_studio=studio1)
        studio3 = create_studio(parent_studio=studio2)

        studios = [studio1, studio2, studio3]

        expected = f"{studio1.name}"
        actual = format_studio_hierarchy_as_path_field(studio1, studios, StudioHierarchyAsPathFieldSettings())
        assert actual == expected

        expected = f"{studio1.name}/{studio2.name}"
        actual = format_studio_hierarchy_as_path_field(studio2, studios, StudioHierarchyAsPathFieldSettings())
        assert actual == expected

        expected = f"{studio1.name}/{studio2.name}/{studio3.name}"
        actual = format_studio_hierarchy_as_path_field(studio3, studios, StudioHierarchyAsPathFieldSettings())
        assert actual == expected
