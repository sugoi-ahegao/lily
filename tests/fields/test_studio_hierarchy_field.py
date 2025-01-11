from tests.testing_model_creators.create_studio import create_studio

from lily.fields.field_studio import StudioFieldSettings
from lily.fields.field_studio_hierarchy import StudioHierarchyFieldSettings, format_studio_hierarchy_field


def test_studio_hierarchy_field_formatting():
    studio1 = create_studio(name="Studio 1")
    studio2 = create_studio(parent_studio=studio1, name="Studio 2")
    studio3 = create_studio(parent_studio=studio2, name="Studio 3")

    all_studios = [studio1, studio2, studio3]

    expected = "[Studio1] [Studio2] [Studio3]"
    actual = format_studio_hierarchy_field(
        studio3,
        all_studios,
        StudioHierarchyFieldSettings(
            separator=" ", studio=StudioFieldSettings(template="[${studio}]", squeeze_name=True)
        ),
    )
    assert expected == actual
