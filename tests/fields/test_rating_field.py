import pytest
from lily.fields.rating_field import RatingFieldSettings, format_rating_field
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_utils.generic import generic


class TestRatingField:
    def test_format_rating_correctly(self):
        scene = create_scene(rating100=50)
        assert format_rating_field(scene, RatingFieldSettings()) == "50"

    def test_formats_random_rating_correctly(self):
        scene = create_scene(rating100=generic.random.randint(0, 100))
        assert format_rating_field(scene, RatingFieldSettings()) == f"{scene.rating100}"

    def test_return_empty_string_if_no_rating(self):
        scene = create_scene(rating100=None)
        assert format_rating_field(scene, RatingFieldSettings()) == ""

    def test_formats_rating_with_template(self):
        scene = create_scene(rating100=95)
        assert format_rating_field(scene, RatingFieldSettings(template="(${rating})")) == "(95)"
        assert format_rating_field(scene, RatingFieldSettings(template="${rating} 123")) == "95 123"

    def test_raises_error_for_invalid_template(self):
        scene = create_scene(rating100=95)
        with pytest.raises(AssertionError):
            format_rating_field(scene, RatingFieldSettings(template="invalid template"))
