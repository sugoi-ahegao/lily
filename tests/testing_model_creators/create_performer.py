from typing import Optional

import mimesis
from lily.models.stash_graphql_models.performer import GenderEnum, Performer
from tests.testing_utils.flip_coin import flip_coin
from tests.testing_utils.generate_random_unique_id import generate_random_unique_id
from tests.testing_utils.generic import generic


def create_performer(
    id: Optional[int] = None,
    name: Optional[str] = None,
    favorite: Optional[bool] = None,
    rating100: Optional[int] = None,
    gender: Optional[GenderEnum] = None,
) -> Performer:
    if id is None:
        id = generate_random_unique_id()

    if name is None:
        # quality of life feature - if gender is female, make a female name, else random
        name = generic.person.full_name(gender=mimesis.Gender.FEMALE if gender == GenderEnum.FEMALE else None)

    if favorite is None:
        favorite = generic.random.choice([True, False])

    if rating100 is None:
        rating100 = None if flip_coin() else generic.random.randint(0, 100)

    if gender is None:
        gender = None if flip_coin() else generic.random.choice_enum_item(GenderEnum)

    return Performer.model_validate(
        {
            "id": id,
            "name": name,
            "disambiguation": None,
            "gender": gender,
            "birthdate": None,
            "ethnicity": None,
            "alias_list": [],
            "favorite": favorite,
            "tags": [],
            "rating100": rating100,
            "created_at": generic.datetime.datetime(),
            "updated_at": generic.datetime.datetime(),
        }
    )
