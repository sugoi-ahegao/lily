from lily.lily_logging.lily_logger import get_lily_logger
from lily.models.user_settings.filter_settings import FilterSettings, filter_registry
from lily.stash_context import StashContext


def passes_all_filters(stash_context: StashContext, filter_settings: FilterSettings) -> bool:
    logger = get_lily_logger()

    for filter_name, filter_setting in filter_settings:
        # This should never happen, every filter name should have a corresponding filter function
        if filter_name not in filter_registry:
            raise ValueError(f"Filter was not found in filter registry: '{filter_name}'")

        # If filter is not set, skip
        if filter_setting is None:
            continue

        filter_function = filter_registry[filter_name]

        if not filter_function(stash_context, filter_setting):
            logger.debug(f"Failed Filter: {filter_name}")
            return False

    return True
