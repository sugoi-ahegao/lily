from types import NoneType

from lily.models.stash_graphql_models.scene import Scene
from lily.stash_context import StashContext

WatchedFieldSettings = NoneType


def watched_field(stash_context: StashContext, settings: WatchedFieldSettings) -> str:
    return format_watched_field(stash_context.scene, settings)


def format_watched_field(scene: Scene, settings: WatchedFieldSettings) -> str:
    if scene.o_counter is None:
        return ""

    if scene.o_counter == 0:
        return ""

    return "✅"
