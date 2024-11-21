from typing import Optional

from lily.models.stash_graphql_models.studio import Studio
from tests.testing_utils.generate_random_unique_id import generate_random_unique_id
from tests.testing_utils.generic import generic


def create_studio(
    id: Optional[int] = None, name: Optional[str] = None, parent_studio: Optional[Studio] = None
) -> Studio:
    if id is None:
        id = generate_random_unique_id()

    if name is None:
        name = generic.finance.company()

    studio = Studio.model_validate(
        {
            "id": id,
            "name": name,
            "parent_studio": parent_studio,
            "child_studios": [],
            "aliases": [],
            "tags": [],
            "rating100": None,
            "favorite": generic.random.choice([True, False]),
            "created_at": generic.datetime.datetime(),
            "updated_at": generic.datetime.datetime(),
        }
    )

    if parent_studio is not None:
        parent_studio.child_studios.append(studio)

    return studio
