import pytest
from lily.helpers.studio_hierarchy import create_studio_hierarchy
from tests.testing_model_creators.create_studio import create_studio


def test_create_studio_hierarchy_with_three_studios():
    studio1 = create_studio()
    studio2 = create_studio(parent_studio=studio1)
    studio3 = create_studio(parent_studio=studio2)

    studios = [studio1, studio2, studio3]

    assert create_studio_hierarchy(studio1, studios) == [studio1]
    assert create_studio_hierarchy(studio2, studios) == [studio1, studio2]
    assert create_studio_hierarchy(studio3, studios) == [studio1, studio2, studio3]


def test_create_studio_hierarchy_with_cycles():
    studio1 = create_studio()
    studio2 = create_studio(parent_studio=studio1)
    studio3 = create_studio(parent_studio=studio2)

    studio1.parent_studio = studio3
    studio3.child_studios.append(studio1)

    studios = [studio1, studio2, studio3]

    with pytest.raises(RuntimeError):
        create_studio_hierarchy(studio1, studios)


def test_studio_hierarchy_with_no_parent():
    studio = create_studio()

    studios = [studio]

    assert create_studio_hierarchy(studio, studios) == [studio]
