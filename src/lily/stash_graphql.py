import re
import time
from pathlib import Path
from typing import Any, Optional

import requests
from lily.lily_logging.lily_logger import get_lily_logger
from lily.lily_logging.stash_logger import StashLogger
from lily.models.stash_graphql_models.performer import PERFORMER_FRAGMENT
from lily.models.stash_graphql_models.scene import SCENE_FRAGMENT, Scene
from lily.models.stash_graphql_models.stash_plugin_config import StashPluginConfig
from lily.models.stash_graphql_models.studio import (
    PARTIAL_STUDIO_FRAGMENT,
    STUDIO_FRAGMENT,
    Studio,
)
from lily.models.stash_graphql_models.tag import PARTIAL_TAG_FRAGMENT, TAG_FRAGMENT, Tag
from lily.models.stash_graphql_models.video_file import VIDEO_FILE_FRAGMENT


class StashGraphQL:
    def __init__(self, graphql_url: str, cookies: Optional[dict[Any, Any]] = None):
        self.graphql_url = graphql_url
        self.cookies = cookies

        self.stash_logger = StashLogger()
        self.logger = get_lily_logger()

    def test_connection(self):
        query = """
            {
                systemStatus {
                    status
                }
                version {
                    version
                }
            }
            """

        response, _ = self.send_request(query)
        systemStatus = response["systemStatus"]["status"]

        if systemStatus != "OK":
            raise RuntimeError(f"Stash System status is not OK. systemStatus: {systemStatus}")

    def get_all_scenes(self) -> list[Scene]:
        query = (
            """
            query GetAllScenes($filter: FindFilterType) {
                findScenes(filter: $filter) {
                    count
                    scenes {
                        ...SceneFragment                        
                    }
                }
            }
        """
            + SCENE_FRAGMENT
            + VIDEO_FILE_FRAGMENT
            + STUDIO_FRAGMENT
            + PARTIAL_STUDIO_FRAGMENT
            + PERFORMER_FRAGMENT
            + PARTIAL_TAG_FRAGMENT
        )

        response, execution_time = self.send_request(
            query, {"filter": {"direction": "DESC", "page": 1, "per_page": -1, "sort": "updated_at"}}
        )

        scenes_count = response["findScenes"]["count"]
        scenes_dict = response["findScenes"]["scenes"]

        self.logger.info(f"Retrieved {scenes_count} scene(s), took {execution_time:.2f} seconds")

        return [Scene.model_validate(scene_dict) for scene_dict in scenes_dict]

    def find_scenes_by_id(self, scene_ids: list[int]) -> list[Scene]:
        query = (
            """
            query FindScenes($scene_ids: [Int!]) {
                findScenes(scene_ids: $scene_ids) {
                    count
                    scenes {
                        ...SceneFragment
                    }
                }
            }
        """
            + SCENE_FRAGMENT
            + VIDEO_FILE_FRAGMENT
            + STUDIO_FRAGMENT
            + PARTIAL_STUDIO_FRAGMENT
            + PERFORMER_FRAGMENT
            + PARTIAL_TAG_FRAGMENT
        )

        response, execution_time = self.send_request(query, {"scene_ids": scene_ids})

        scenes_count = response["findScenes"]["count"]
        scenes_dict = response["findScenes"]["scenes"]

        self.logger.info(f"Retrieved {scenes_count} scene(s), took {execution_time:.2f} seconds")

        return [Scene.model_validate(scene_dict) for scene_dict in scenes_dict]

    def get_all_studios(self) -> list[Studio]:
        query = (
            """
            query GetAllStudios($filter: FindFilterType) {
                findStudios(filter: $filter) {
                    count
                    studios {
                        ...StudioFragment
                    }
                }
            }
        """
            + STUDIO_FRAGMENT
            + PARTIAL_STUDIO_FRAGMENT
            + PARTIAL_TAG_FRAGMENT
        )

        response, execution_time = self.send_request(
            query, {"filter": {"direction": "DESC", "page": 1, "per_page": -1, "sort": "updated_at"}}
        )

        studios_count = response["findStudios"]["count"]
        studios_dict = response["findStudios"]["studios"]

        self.logger.info(f"Retrieved {studios_count} studio(s), took {execution_time:.2f} seconds")

        return [Studio.model_validate(studio_dict) for studio_dict in studios_dict]

    def get_all_tags(self) -> list[Tag]:
        query = (
            """
            query GetAllTags($filter: FindFilterType) {
                findTags(filter: $filter) {
                    count
                    tags {
                        ...TagFragment
                    }
                }
            }
        """
            + TAG_FRAGMENT
            + PARTIAL_TAG_FRAGMENT
        )

        response, execution_time = self.send_request(
            query, {"filter": {"direction": "DESC", "page": 1, "per_page": -1, "sort": "updated_at"}}
        )

        tags_count = response["findTags"]["count"]
        tags_dict = response["findTags"]["tags"]

        self.logger.info(f"Retrieved {tags_count} tag(s), took {execution_time:.2f} seconds")

        return [Tag.model_validate(tag_dict) for tag_dict in tags_dict]

    def get_plugin_configuration(self) -> StashPluginConfig:
        query = """
            query GetLilyPluginConfiguration {
                configuration {
                    plugins(include: "lily")
                }
            }
        """

        response, execution_time = self.send_request(query)
        plugin_config_dict = response["configuration"]["plugins"].get("lily")

        if not plugin_config_dict:
            self.logger.warning("Lily plugin configuration was not found in Stash, using default values")
            plugin_config_dict = {}
        else:
            self.logger.info(f"Retrieved Lily plugin configuration, took {execution_time:.2f} seconds")

        return StashPluginConfig.model_validate(plugin_config_dict)

    def move_file(self, video_file_id: int, dst_path: Path) -> None:
        query = """
            mutation MoveFile($input: MoveFilesInput!) {
                moveFiles (input: $input)
            }
        """

        dst_path = dst_path.resolve()

        variables: dict[Any, Any] = {
            "input": {
                "ids": [video_file_id],
                "destination_folder": str(dst_path.parent.resolve()),
                "destination_basename": dst_path.name,
            }
        }

        response, execution_time = self.send_request(query, variables)

        if response["moveFiles"] is not True:
            raise RuntimeError("Failed to move file")

        self.logger.info(f"Moved file, took {execution_time:.2f} seconds")

    def format_request_body_for_logging(self, request_body: dict[str, Any]) -> str:
        # Replace "\n" with " ", then remove extra spaces
        return re.sub(r"\s+", " ", str(request_body).replace("\\n", " ").strip())

    def send_request(self, query: str, variables: Optional[dict[Any, Any]] = None) -> tuple[dict[Any, Any], float]:
        body: dict[str, Any] = {"query": query, "variables": variables}

        try:
            start_time = time.time()
            response = requests.post(self.graphql_url, json=body, cookies=self.cookies)
            response.raise_for_status()
            response_json = response.json()
            execution_time = time.time() - start_time

        except Exception as e:
            self.logger.debug(f"Request URL: {self.graphql_url}")
            self.logger.debug("Request Body: " + f"{self.format_request_body_for_logging(body)}")

            self.stash_logger.error(f"Exception occurred while sending request: {e}")
            self.logger.exception(f"Exception occurred while sending request: {e}")
            raise

        if "errors" in response_json:
            raise RuntimeError(f"Received Error in Response: {response_json}")

        response_data = response_json["data"]

        return response_data, execution_time
