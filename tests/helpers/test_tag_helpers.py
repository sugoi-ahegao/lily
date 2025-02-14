from tests.testing_model_creators.create_tag import create_tag
from tests.testing_utils.flip_coin import flip_coin
from tests.testing_utils.generic import generic

from lily.helpers.tag_helpers import get_sub_tags


class TestTagHelpers:
    def test_get_sub_tags_with_randomly_nested_tags(self):
        parent_tag = create_tag()

        first_sub_tag = create_tag(parents=[parent_tag])

        all_tags = [parent_tag, first_sub_tag]
        sub_tags = [first_sub_tag]

        for _ in range(100):
            if flip_coin():
                random_sub_tag = generic.random.choice(sub_tags)
                new_tag = create_tag(parents=[random_sub_tag])

                all_tags.append(new_tag)
                sub_tags.append(new_tag)

            else:
                new_tag = create_tag()

                all_tags.append(new_tag)

        generated_sub_tags = get_sub_tags(parent_tag, all_tags)

        sub_tag_ids = set([tag.id for tag in sub_tags])
        generated_sub_tag_ids = set([tag.id for tag in generated_sub_tags])

        assert sub_tag_ids == generated_sub_tag_ids
