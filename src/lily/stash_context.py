from lily.models.stash_graphql_models.scene import Scene
from lily.models.stash_graphql_models.studio import Studio
from lily.models.stash_graphql_models.tag import Tag
from lily.models.stash_graphql_models.video_file import VideoFile


class StashContext:
    def __init__(
        self,
        scene: Scene,
        video_file: VideoFile,
        studios: list[Studio],
        tags: list[Tag],
    ):
        self.scene = scene
        self.video_file = video_file
        self.studios = studios
        self.tags = tags
