import pytest
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_utils.generic import generic

from lily.fields.field_rating import RatingFieldSettings, format_rating_field


class TestRatingField:
    def test_formats_rating_correctly(self):
        scene = create_scene(rating100=50)
        assert format_rating_field(scene.rating100, RatingFieldSettings()) == "50"

    def test_formats_random_rating_correctly(self):
        scene = create_scene(rating100=generic.random.randint(0, 100))
        assert format_rating_field(scene.rating100, RatingFieldSettings()) == f"{scene.rating100}"

    def test_return_empty_string_if_no_rating(self):
        scene = create_scene(rating100=None)
        assert format_rating_field(scene.rating100, RatingFieldSettings()) == ""

    def test_formats_rating_with_template(self):
        scene = create_scene(rating100=95)
        assert format_rating_field(scene.rating100, RatingFieldSettings(template="(${rating})")) == "(95)"
        assert format_rating_field(scene.rating100, RatingFieldSettings(template="${rating} 123")) == "95 123"

    def test_raises_error_for_invalid_template(self):
        scene = create_scene(rating100=95)
        with pytest.raises(ValueError):
            format_rating_field(scene.rating100, RatingFieldSettings(template="invalid template"))

    def test_maps_rating_correctly(self):
        scene = create_scene(rating100=95)
        assert format_rating_field(scene.rating100, RatingFieldSettings(mappings={"== 95": "A"})) == "A"

    def test_maps_rating_with_multiple_mappings(self):
        scene = create_scene(rating100=95)
        mappings = {"== 90": "A", "< 95": "B", ">= 90": "C"}

        assert format_rating_field(scene.rating100, RatingFieldSettings(mappings=mappings)) == "C"

    def test_maps_rating_based_on_order(self):
        scene = create_scene(rating100=95)

        assert format_rating_field(scene.rating100, RatingFieldSettings(mappings={"== 95": "A", ">= 90": "B"})) == "A"

    def test_maps_rating_falls_on_default_value(self):
        scene = create_scene(rating100=85)

        assert format_rating_field(scene.rating100, RatingFieldSettings(mappings={"== 95": "A", ">= 90": "B"})) == "85"

    def test_maps_rating_with_template(self):
        scene = create_scene(rating100=95)

        assert (
            format_rating_field(scene.rating100, RatingFieldSettings(template="(${rating})", mappings={"== 95": "A"}))
            == "(A)"
        )
        assert (
            format_rating_field(scene.rating100, RatingFieldSettings(template="${rating} 123", mappings={"== 95": "A"}))
            == "A 123"
        )
