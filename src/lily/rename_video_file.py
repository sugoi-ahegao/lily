from pathlib import Path

from lily.lily_logging.lily_logger import get_lily_dry_run_logger, get_lily_logger, get_lily_rename_logger
from lily.lily_logging.stash_logger import get_stash_logger
from lily.lily_results import LilyResults
from lily.models.stash_graphql_models.stash_plugin_config import StashPluginConfig
from lily.stash_context import StashContext
from lily.stash_graphql import StashGraphQL
from lily.utils.path_utils import are_paths_on_same_drive

REMOVE_EMPTY_SRC_DIRS = True


def rename_video_file(
    stash_context: StashContext, dst_path: Path, stash_plugin_config: StashPluginConfig, stash_graphql: StashGraphQL
):
    logger = get_lily_logger()
    rename_logger = get_lily_rename_logger()
    dry_run_logger = get_lily_dry_run_logger()
    stash_logger = get_stash_logger()

    logger.info(f'Final Destination Path: "{dst_path}"')

    src_path = stash_context.video_file.path

    # If the source and destination are on different drives,
    # and "allow rename across drives" is disabled, no need to rename
    if not stash_plugin_config.allow_rename_across_drives:
        if not are_paths_on_same_drive(src_path, dst_path):
            logger.info("Skipping - Destination would be on a different drive")
            LilyResults.cross_drive_conflict_counter.inc()
            return

    if not stash_plugin_config.dry_run_disabled:
        rename_message = f"[DRY-RUN RENAME] '{src_path.resolve()}' --> '{dst_path.resolve()}'"
        stash_logger.info(rename_message)
        dry_run_logger.info(rename_message)
        LilyResults.dry_run_renamed_counter.inc()
        return

    try:
        stash_graphql.move_file(stash_context.video_file.id, dst_path)
        rename_message = f"[RENAMED] '{src_path.resolve()}' --> '{dst_path.resolve()}'"
        stash_logger.info(rename_message)
        rename_logger.info(rename_message)
        LilyResults.renamed_counter.inc()

    except Exception:
        message = f"[FAILED TO RENAME] '{src_path.resolve()}' --> '{dst_path.resolve()}'"
        stash_logger.error(message)
        logger.error(message)
        LilyResults.rename_failed_counter.inc()
