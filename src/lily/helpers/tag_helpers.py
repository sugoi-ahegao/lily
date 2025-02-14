from collections import deque
from typing import Optional

from lily.models.stash_graphql_models.tag import Tag

tag_id_cache = None
tag_name_cache = None

last_tags_id_ref: Optional[list[Tag]] = None
last_tags_name_ref: Optional[list[Tag]] = None


def get_tag(id: Optional[int], name: Optional[str], tags: list[Tag]):
    if (id is None) and (name is None):
        raise ValueError("Either id or name is required")
    elif (id is not None) and (name is not None):
        raise ValueError("Both id and name cannot be set")

    if id is not None:
        return get_tag_by_id(id, tags)

    if name is not None:
        return get_tag_by_name(name, tags)

    raise RuntimeError("This code should not be reachable")


def get_sub_tags(tag: Tag, tags: list[Tag]):
    sub_tags: list[Tag] = []

    search_queue = deque([tag])
    explored_ids: set[int] = set()

    while len(search_queue) != 0:
        curr_tag = search_queue.pop()

        if curr_tag.id in explored_ids:
            raise RuntimeError(f"Tag Cycle Detected. Already explored Tag ID: '{curr_tag.id}' ")

        explored_ids.add(curr_tag.id)

        for partial_child_tag in curr_tag.children:
            child_tag = get_tag_by_id(partial_child_tag.id, tags)

            sub_tags.append(child_tag)
            search_queue.append(child_tag)

    return sub_tags


def print_tag_tree(tag: Tag, tags: list[Tag], level: int = 0):
    print("\t" * level, tag.id)
    for partial_child_tag in tag.children:
        child_tag = get_tag_by_id(partial_child_tag.id, tags)
        print_tag_tree(child_tag, tags, level + 1)


def get_tag_by_id(id: int, tags: list[Tag]):
    global tag_id_cache, last_tags_id_ref

    if tag_id_cache is None or (last_tags_id_ref is not tags):
        last_tags_id_ref = tags
        tag_id_cache = {tag.id: tag for tag in tags}

    tag = tag_id_cache.get(id)

    assert tag is not None, f"Tag not found. ID: '{id}'"

    return tag


def get_tag_by_name(name: str, tags: list[Tag]):
    global tag_name_cache, last_tags_name_ref

    if (tag_name_cache is None) or (last_tags_name_ref is not tags):
        last_tags_name_ref = tags
        tag_name_cache = {tag.name: tag for tag in tags}

    tag = tag_name_cache.get(name)

    assert tag is not None, f"Tag not found. Name: '{name}'"

    return tag
