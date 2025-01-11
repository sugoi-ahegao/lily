from tests.testing_model_creators.create_performer import create_performer

from lily.fields.field_performers import (
    PerformerSortKey,
    sort_performers,
)


class TestPerformersSorting:
    def test_sorting_by_id_is_the_default(self):
        performer1 = create_performer(id=1)
        performer2 = create_performer(id=2)

        # sort by id
        expected = [performer1, performer2]
        actual = sort_performers(performers=[performer1, performer2])

        assert expected == actual

        # switch ids
        performer1.id, performer2.id = performer2.id, performer1.id
        expected = [performer2, performer1]
        actual = sort_performers(performers=[performer1, performer2])

        assert expected == actual

    def test_sorting_by_name(self):
        performer1 = create_performer(name="Alice Alpha")
        performer2 = create_performer(name="Bob Builder")

        # sort by name
        expected = [performer1, performer2]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.NAME])

        assert expected == actual

        # switch names
        performer1.name, performer2.name = performer2.name, performer1.name
        expected = [performer2, performer1]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.NAME])

        assert expected == actual

    def test_sorting_by_id(self):
        performer1 = create_performer(id=1)
        performer2 = create_performer(id=2)

        # sort by id
        expected = [performer1, performer2]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.ID])

        assert expected == actual

        # switch ids
        performer1.id, performer2.id = performer2.id, performer1.id
        expected = [performer2, performer1]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.ID])

    def test_sorting_by_favorite(self):
        performer1 = create_performer(favorite=True)
        performer2 = create_performer(favorite=False)

        # sort by favorite
        expected = [performer1, performer2]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.FAVORITE])

        assert expected == actual

        # switch favorites
        performer1.favorite, performer2.favorite = performer2.favorite, performer1.favorite
        expected = [performer2, performer1]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.FAVORITE])

        assert expected == actual

    def test_sorting_by_rating(self):
        performer1 = create_performer(rating100=100)
        performer2 = create_performer(rating100=20)

        # sort by rating
        expected = [performer1, performer2]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.RATING])

        assert expected == actual

        # switch ratings
        performer1.rating100, performer2.rating100 = (
            performer2.rating100,
            performer1.rating100,
        )
        expected = [performer2, performer1]
        actual = sort_performers(performers=[performer1, performer2], sort_by=[PerformerSortKey.RATING])

        assert expected == actual

    def test_different_sorting_keys_with_multiple_performers(self):
        performer1 = create_performer(id=1, name="Charlie Chaplin", rating100=30, favorite=False)
        performer2 = create_performer(id=2, name="Alice Alpha", rating100=10, favorite=False)
        performer3 = create_performer(id=3, name="Bob Builder", rating100=20, favorite=True)

        performers = [performer1, performer2, performer3]

        sorted_by_ids = [performer1, performer2, performer3]
        sorted_by_names = [performer2, performer3, performer1]
        sorted_by_ratings = [performer1, performer3, performer2]
        sorted_by_favorite = [performer3, performer1, performer2]

        assert sorted_by_ids == sort_performers(performers=performers, sort_by=[PerformerSortKey.ID])
        assert sorted_by_names == sort_performers(performers=performers, sort_by=[PerformerSortKey.NAME])
        assert sorted_by_ratings == sort_performers(performers=performers, sort_by=[PerformerSortKey.RATING])
        assert sorted_by_favorite == sort_performers(performers=performers, sort_by=[PerformerSortKey.FAVORITE])

    def test_sorting_by_multiple_keys_at_the_same_time(self):
        performer1 = create_performer(id=1, name="Charlie Chaplin", rating100=10, favorite=False)
        performer2 = create_performer(id=2, name="Alice Alpha", rating100=30, favorite=False)
        performer3 = create_performer(id=3, name="Bob Builder", rating100=10, favorite=True)

        performers = [performer1, performer2, performer3]

        # sort by favorite, rating, name
        expected = [performer3, performer2, performer1]
        actual = sort_performers(performers=performers, sort_by=[PerformerSortKey.FAVORITE, PerformerSortKey.RATING])

        assert expected == actual

        # sort by name, rating
        # since all performers have different names, its basically sort by name
        expected = [performer2, performer3, performer1]
        actual = sort_performers(performers=performers, sort_by=[PerformerSortKey.NAME, PerformerSortKey.RATING])

        assert expected == actual

    def test_sorting_by_multiple_keys_with_same_rating(self):
        performer1 = create_performer(id=1, name="Alice Alpha", rating100=10, favorite=False)
        performer2 = create_performer(id=2, name="Bob Builder", rating100=10, favorite=False)
        performer3 = create_performer(id=3, name="Charlie Chaplin", rating100=10, favorite=True)

        performers = [performer1, performer2, performer3]

        # sort by favorite, rating, name
        expected = [performer3, performer1, performer2]
        actual = sort_performers(
            performers=performers, sort_by=[PerformerSortKey.FAVORITE, PerformerSortKey.RATING, PerformerSortKey.NAME]
        )

        assert expected == actual
