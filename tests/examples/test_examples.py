from pathlib import Path
from typing import Any, Optional

import pytest

from lily.models.core import BaseModelWithExactAttributes
from lily.models.user_settings.user_settings import UserSettings, load_user_settings
from lily.process_video_file import process_video_file
from lily.stash_context import StashContext
from lily.stash_graphql import StashGraphQL
from lily.utils.load_yaml_file import load_yaml_file
from lily.utils.path_utils import are_paths_equal


@pytest.mark.default_cassette("test_examples.yaml")
@pytest.mark.vcr
@pytest.mark.parametrize(
    "user_settings_file_name, expected_renames_file_name",
    [
        ("minimal-user-settings.yaml", "minimal-user-settings.renames.yaml"),
        # ("path-based-user-settings.yaml", "path-based-user-settings.renames.yaml"),
        ("tags-based-user-settings.yaml", "path-based-user-settings.renames.yaml"),
    ],
)
def test_examples(user_settings_file_name: str, expected_renames_file_name: str):
    user_settings_file_path = Path("./examples") / Path(user_settings_file_name)
    expected_renames_file_path = Path("./examples/expected_renames") / Path(expected_renames_file_name)

    user_settings = load_user_settings(load_yaml_file(user_settings_file_path))
    expected_renames = load_expected_renames(load_yaml_file(expected_renames_file_path))
    generated_renames = generate_renames(user_settings)

    for scene_id in expected_renames:
        if scene_id not in generated_renames:
            raise ValueError(
                f"Generated renames does not contain scene id: {scene_id}. "
                f"Expected rename: {scene_id} => {expected_renames[scene_id]}",
            )

    for scene_id in generated_renames:
        if scene_id not in expected_renames:
            raise ValueError(
                f"Expected renames does not contain scene id: {scene_id}. "
                f"Generated rename: {{{scene_id} => {generated_renames[scene_id]}}}"
            )

    for scene_id in expected_renames:
        expected_dst_path = expected_renames[scene_id]
        generated_dst_path = generated_renames[scene_id]

        if expected_dst_path is None or generated_dst_path is None:
            assert expected_dst_path == generated_dst_path
            continue

        assert are_paths_equal(expected_dst_path, generated_dst_path)


def load_expected_renames(expected_results_dict: dict[Any, Any]):
    class ExpectedResults(BaseModelWithExactAttributes):
        renames: dict[int, Optional[Path]]

    expected_results = ExpectedResults.model_validate(expected_results_dict)

    return expected_results.renames


def generate_renames(user_settings: UserSettings):
    stash_graphql = StashGraphQL("http://localhost:9995/graphql")

    scenes = stash_graphql.get_all_scenes()
    studios = stash_graphql.get_all_studios()
    tags = stash_graphql.get_all_tags()
    stash_libraries = stash_graphql.get_stash_libraries()

    results: dict[int, Optional[Path]] = {}

    for scene in scenes:
        for video_file in scene.files:
            stash_context = StashContext(
                scene=scene, video_file=video_file, studios=studios, tags=tags, stash_libraries=stash_libraries
            )

            destination_path = process_video_file(stash_context=stash_context, user_settings=user_settings)

            results[scene.id] = destination_path

    return results
