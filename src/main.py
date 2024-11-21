import json
import sys
import time
from sys import stdin
from typing import Any

from lily.lily_logging.lily_logger import get_lily_logger, setup_logging
from lily.lily_logging.lily_logger_adapter import LilyLoggerAdapter
from lily.lily_logging.stash_logger import get_stash_logger
from lily.lily_results import LilyResults
from lily.models.stash_graphql_models.scene import Scene
from lily.models.user_settings.user_settings import load_user_settings
from lily.plugin_arg_parser import PluginArgs, parse_plugin_args
from lily.process_video_file import process_video_file
from lily.rename_video_file import rename_video_file
from lily.stash_context import StashContext
from lily.stash_graphql import StashGraphQL
from lily.utils.load_yaml_file import load_yaml_file


def main(args: PluginArgs):
    # ----- Setup -----

    logger = get_lily_logger()
    stash_logger = get_stash_logger()

    plugin_input_str = stdin.read()
    plugin_input_dict = json.loads(plugin_input_str)
    logger.info(f"🌿 Plugin Input: {plugin_input_str}")

    user_settings_dict = load_yaml_file(args.user_settings_path)
    user_settings = load_user_settings(user_settings_dict)
    logger.info("⚙️ User Settings Loaded")

    stash_graphql = create_stash_graphql_instance(plugin_input_dict)
    stash_graphql.test_connection()
    logger.info("🛰️ Connected to Stash")

    stash_plugin_config = stash_graphql.get_plugin_configuration()
    logger.info(f"Lily Plugin Configuration: {stash_plugin_config.model_dump_json()}")

    LilyResults.setup(stash_plugin_config)

    # ----- Execution -----

    scenes = fetch_scenes(plugin_input_dict, stash_graphql)

    if len(scenes) == 0:
        raise RuntimeError("No scenes found")

    studios = stash_graphql.get_all_studios()
    tags = stash_graphql.get_all_tags()

    for scene in scenes:
        with LilyLoggerAdapter.with_scene_id(scene.id):
            for video_file in scene.files:
                logger.debug(f"🎥 Processing '{video_file.path}'")

                stash_ctx = StashContext(scene, video_file, studios, tags)
                dst_path = process_video_file(stash_ctx, user_settings)

                if dst_path is None:
                    continue

                rename_video_file(stash_ctx, dst_path, stash_plugin_config, stash_graphql)
                LilyResults.videos_processed_counter.inc()
        LilyResults.scenes_processed_counter.inc()

    stash_logger.info(LilyResults.get_results())
    logger.info(LilyResults.get_results())

    stash_logger.debug(LilyResults.get_detailed_results())
    logger.info(LilyResults.get_detailed_results())


def create_stash_graphql_instance(plugin_input_dict: dict[Any, Any]) -> StashGraphQL:
    scheme = plugin_input_dict["server_connection"]["Scheme"]
    host = plugin_input_dict["server_connection"]["Host"]
    port = plugin_input_dict["server_connection"]["Port"]
    cookies = {"session": plugin_input_dict["server_connection"]["SessionCookie"]["Value"]}

    if host == "0.0.0.0":
        host = "localhost"

    graphql_url = f"{scheme}://{host}:{port}/graphql"

    return StashGraphQL(graphql_url, cookies=cookies)


def fetch_scenes(
    plugin_input_dict: dict[Any, Any],
    stash_graphql: StashGraphQL,
) -> list[Scene]:
    logger = get_lily_logger()

    if plugin_input_dict["args"].get("mode") == "all-scenes":
        logger.info("🫡 Processing all scenes")
        scenes = stash_graphql.get_all_scenes()

    elif plugin_input_dict["args"]["hookContext"]["input"].get("ids") is not None:
        scene_ids = plugin_input_dict["args"]["hookContext"]["input"]["ids"]

        logger.info(f"🫡 Processing {len(scene_ids)} scene updates. Scene IDs: {scene_ids}")
        scenes = stash_graphql.find_scenes_by_id(scene_ids)

    elif plugin_input_dict["args"]["hookContext"]["input"].get("id") is not None:
        scene_id = plugin_input_dict["args"]["hookContext"]["input"]["id"]

        logger.info(f"🫡 Processing a single scene update. Scene ID: {scene_id}")
        scenes = stash_graphql.find_scenes_by_id([scene_id])

    else:
        raise ValueError("Unknown Execution Mode")

    return scenes


if __name__ == "__main__":
    args = parse_plugin_args()

    if args.logging_config_file_path is not None:
        plugin_dir_str = str(args.plugin_dir.resolve().as_posix())
        logging_config_dict = load_yaml_file(args.logging_config_file_path, replace={"plugin_dir": plugin_dir_str})
        setup_logging(logging_config_dict)

    else:
        setup_logging(enabled=False)

    logger = get_lily_logger()
    logger.info("🔊 Logging Setup Complete")

    stash_logger = get_stash_logger()

    logger.info("🌿 Starting Lily...")
    stash_logger.info("Starting Lily...")
    start_time = time.time()
    try:
        main(args)

    except Exception as e:
        logger.exception(e)
        raise

    execution_time = time.time() - start_time
    execution_time_message = (
        f"Lily Completed Successfully (took {(execution_time % 3600) // 60:.0f}m {execution_time % 60:.3f}s)"
    )

    stash_logger.info(execution_time_message)
    logger.info(execution_time_message)

    sys.exit(0)
