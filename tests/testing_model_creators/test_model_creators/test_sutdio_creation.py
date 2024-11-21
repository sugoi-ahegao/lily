from lily.models.stash_graphql_models.studio import Studio
from tests.testing_model_creators.create_studio import create_studio


class TestStudioCreation:
    def test_studio_creator_returns_studio(self):
        studio = create_studio()

        assert isinstance(studio, Studio)

    def test_studio_creator_does_not_return_same_studio_twice(self):
        studio1 = create_studio()
        studio2 = create_studio()

        assert studio1 != studio2
        assert studio1.id != studio2.id
        assert studio1.name != studio2.name

    def test_studio_name_is_set(self):
        name = "My Studio"
        studio = create_studio(name=name)

        assert studio.name == name
