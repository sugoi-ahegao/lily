from pathlib import Path
from unittest.mock import create_autospec

from lily.models.stash_graphql_models.stash_plugin_config import StashPluginConfig
from lily.rename_video_file import rename_video_file
from lily.stash_graphql import StashGraphQL

from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_utils.generic import generic


def test_file_is_not_renamed_if_dry_run_is_enabled():
    stash_ctx = create_stash_context()
    destination_path = Path("/path/to/file.mp4")
    mock_stash_graphql = create_autospec(StashGraphQL, instance=True)

    stash_plugin_config = StashPluginConfig(
        dry_run_enabled=True,
        # Configuration of "allow rename across drives" should not matter
        allow_rename_across_drives=generic.random.choice([True, False]),
    )

    rename_video_file(
        stash_context=stash_ctx,
        dst_path=destination_path,
        stash_plugin_config=stash_plugin_config,
        stash_graphql=mock_stash_graphql,
    )

    mock_stash_graphql.move_file.assert_not_called()


def test_file_in_different_drive_is_not_renamed_if_renames_across_drives_are_disabled():
    stash_ctx = create_stash_context()
    destination_path = Path("O:/path/to/file.mp4")  # Different drive
    mock_stash_graphql = create_autospec(StashGraphQL, instance=True)

    stash_plugin_config = StashPluginConfig(
        # Configuration of "dry run" should not matter
        dry_run_enabled=generic.random.choice([True, False]),
        allow_rename_across_drives=False,
    )

    # If the source and destination are on different drives,
    # and "allow rename across drives" is disabled, no need to rename
    rename_video_file(
        stash_context=stash_ctx,
        dst_path=destination_path,
        stash_plugin_config=stash_plugin_config,
        stash_graphql=mock_stash_graphql,
    )

    mock_stash_graphql.move_file.assert_not_called()


def test_file_is_renamed():
    stash_ctx = create_stash_context()
    destination_path = Path("O:/path/to/file.mp4")  # Different drive
    mock_stash_graphql = create_autospec(StashGraphQL, instance=True)

    stash_plugin_config = StashPluginConfig(dry_run_enabled=False, allow_rename_across_drives=True)
    rename_video_file(
        stash_context=stash_ctx,
        dst_path=destination_path,
        stash_plugin_config=stash_plugin_config,
        stash_graphql=mock_stash_graphql,
    )

    mock_stash_graphql.move_file.assert_called()
