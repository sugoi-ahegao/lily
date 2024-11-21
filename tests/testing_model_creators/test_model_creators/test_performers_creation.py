from lily.models.stash_graphql_models.performer import Performer
from tests.testing_model_creators.create_performer import create_performer


class TestPerformersCreation:
    def test_performer_creator_returns_performer(self):
        performer = create_performer()

        assert isinstance(performer, Performer)

    def test_performer_creator_does_not_create_same_performer_twice(self):
        performer1 = create_performer()
        performer2 = create_performer()

        assert performer1 != performer2
        assert performer1.id != performer2.id
        assert performer1.name != performer2.name

    def test_performer_name_is_set(self):
        name = "My Performer"
        performer = create_performer(name=name)

        assert performer.name == name
