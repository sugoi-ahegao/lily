from collections import deque
from typing import Optional

from lily.models.stash_graphql_models.studio import Studio


def create_studio_hierarchy(studio: Studio, all_studios: list[Studio]) -> list[Studio]:
    """
    Create a studio hierarchy with the input studio as the bottom of the hierarchy (list)
    """

    def find_parent_studio(studio: Studio) -> Optional[Studio]:
        if studio.parent_studio is None:
            return None

        for curr_studio in all_studios:
            if curr_studio.id == studio.parent_studio.id:
                return curr_studio
        return None

    studio_hierarchy = deque([studio])
    explored_studio_ids = set([studio.id])

    curr_studio = studio
    while curr_studio := find_parent_studio(curr_studio):
        if curr_studio.id in explored_studio_ids:
            raise RuntimeError(f"Studio Cycle Detected. Already explored Studio ID: {curr_studio.id}")

        explored_studio_ids.add(curr_studio.id)
        studio_hierarchy.appendleft(curr_studio)

    return list(studio_hierarchy)
