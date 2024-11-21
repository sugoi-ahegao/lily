from lily.filters.matches_any_source_dirs import matches_any_source_dir
from lily.filters.matches_any_studio import matches_any_studio
from lily.filters.matches_organized_value import matches_organized_value
from lily.filters.matches_source_dir import matches_source_dir
from lily.filters.matches_studio import matches_studio
from lily.lily_logging.lily_logger import get_lily_logger
from lily.models.user_settings.filter_settings import FilterSettings
from lily.stash_context import StashContext


def passes_all_filters(stash_context: StashContext, filter_settings: FilterSettings) -> bool:
    logger = get_lily_logger()

    if filter_settings.matches_organized_value is not None:
        if not matches_organized_value(stash_context, filter_settings.matches_organized_value):
            logger.debug("Failed Filter: matches_organized_value")
            return False

    if filter_settings.matches_studio is not None:
        if not matches_studio(stash_context, filter_settings.matches_studio):
            logger.debug("Failed Filter: matches_studio")
            return False

    if filter_settings.matches_any_studio is not None:
        if not matches_any_studio(stash_context, filter_settings.matches_any_studio):
            logger.debug("Failed Filter: matches_any_studio")
            return False

    if filter_settings.matches_source_dir is not None:
        if not matches_source_dir(stash_context, filter_settings.matches_source_dir):
            logger.debug("Failed Filter: matches_source_dir")
            return False

    if filter_settings.matches_any_source_dir is not None:
        if not matches_any_source_dir(stash_context, filter_settings.matches_any_source_dir):
            logger.debug("Failed Filter: matches_any_source_dir")
            return False

    return True
