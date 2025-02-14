from typing import Optional

from tests.testing_utils.generate_random_unique_id import generate_random_unique_id
from tests.testing_utils.generic import generic

from lily.models.stash_graphql_models.performer import Performer
from lily.models.stash_graphql_models.scene import Scene
from lily.models.stash_graphql_models.studio import Studio
from lily.models.stash_graphql_models.tag import PartialTag


def create_scene(
    title: Optional[str] = None,
    date: Optional[str] = None,
    organized: Optional[bool] = None,
    studio: Optional[Studio] = None,
    performers: Optional[list[Performer]] = None,
    tags: Optional[list[PartialTag]] = None,
    rating100: Optional[int] = None,
    o_counter: Optional[int] = None,
    stash_ids: Optional[list[dict[str, str]]] = None,
) -> Scene:
    if organized is None:
        organized = generic.random.choice([True, False])

    if stash_ids is None:
        stash_ids = []

    if tags is None:
        tags = []

    return Scene.model_validate(
        {
            "id": generate_random_unique_id(),
            "title": title,
            "details": None,
            "date": date,
            "rating100": rating100,
            "organized": organized,
            "o_counter": o_counter,
            "created_at": generic.datetime.datetime(),
            "updated_at": generic.datetime.datetime(),
            "stash_ids": stash_ids,
            "files": [],
            "studio": studio,
            "tags": tags,
            "performers": performers or [],
        }
    )
