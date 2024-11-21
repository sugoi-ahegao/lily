from types import NoneType

from lily.models.stash_graphql_models.scene import Scene

WatchedFieldSettings = NoneType


def format_watched_field(scene: Scene, settings: WatchedFieldSettings) -> str:
    if scene.o_counter is None:
        return ""

    if scene.o_counter == 0:
        return ""

    return "✅"
