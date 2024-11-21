import json
from pathlib import Path
from string import Template
from typing import Optional

from lily.file_path_template import generate_file_dir, generate_file_name
from lily.helpers.validate_template import validate_template_identifiers
from lily.lily_logging.lily_logger import get_lily_logger
from lily.lily_logging.lily_logger_adapter import LilyLoggerAdapter
from lily.lily_results import LilyResults
from lily.models.user_settings.user_settings import UserSettings
from lily.passes_all_filters import passes_all_filters
from lily.stash_context import StashContext
from lily.utils.path_utils import are_paths_equal, file_exists


def process_video_file(stash_context: StashContext, user_settings: UserSettings) -> Optional[Path]:
    logger = get_lily_logger()

    selected_rule = None
    for index, rename_rule in enumerate(user_settings.rename_rules):
        with LilyLoggerAdapter.with_rule_id(index):
            if passes_all_filters(stash_context, rename_rule.filters):
                selected_rule = rename_rule
                logger.debug(f"Selected Rename Rule: {json.dumps(selected_rule.name)}")
                break

    if selected_rule is None:
        LilyResults.filtered_out_counter.inc()
        return

    # File extension should be the same as the original video file
    file_ext = Path(stash_context.video_file.basename).suffix

    # Extract template file name since it may be modified to remove fields to satisfy max path length
    template_file_name = selected_rule.template_file_name

    # Extract variables for readability
    max_path_length = selected_rule.post_templating_settings.path.max_path_length
    field_removal_order = selected_rule.post_templating_settings.path.field_removal_order

    # Initialize new file path, so that it can be used outside of while loop
    new_file_path = None

    # This loop is used to generate new file path until it does not exceed max path length
    for index in range(len(field_removal_order) + 1):
        # NOTE: Initially, index is 0, so template_file_name is not modified
        template_file_name = remove_fields_from_template(template_file_name, field_removal_order[:index])

        new_file_name = generate_file_name(template_file_name, stash_context, selected_rule.field_settings)
        new_file_dir = generate_file_dir(selected_rule.template_file_dir, stash_context, selected_rule.field_settings)
        new_file_path = Path(new_file_dir, f"{new_file_name}{file_ext}")

        new_file_path = generate_unique_file_path(
            source_file_path=stash_context.video_file.path,
            templated_file_path=new_file_path,
            duplicate_file_suffix=selected_rule.post_templating_settings.path.duplicate_suffix_template,
        )

        if not exceeds_max_path_length(new_file_path, max_path_length):
            break

        # If we are at the end of the loop and the new file path still exceeds max path length, raise error
        if index == len(field_removal_order):
            raise ValueError(
                f"Unable to generate file path that does not exceed max path length of '{max_path_length}' characters.",
                f"File path: '{new_file_path}'",
            )

    if new_file_path is None:
        raise RuntimeError("Unknown Error: Unable to generate new file path.")

    # If the source and destination are the same, no need to rename
    if are_paths_equal(stash_context.video_file.path, new_file_path):
        LilyResults.path_unchanged_counter.inc()
        return

    return new_file_path


def exceeds_max_path_length(path: Path, max_path_length: int) -> bool:
    return len(str(path.resolve())) > max_path_length


def remove_fields_from_template(template_str: str, fields_to_remove: list[str]) -> str:
    for field in fields_to_remove:
        template_str = Template(template_str).safe_substitute({field: ""})
    return template_str


def generate_unique_file_path(source_file_path: Path, templated_file_path: Path, duplicate_file_suffix: str) -> Path:
    validate_template_identifiers(duplicate_file_suffix, ["num"])

    # If the source file path is the same as the templated file path,
    # then the path is already unique, so there is no need to generate a unique file path
    if are_paths_equal(source_file_path, templated_file_path):
        return source_file_path

    if not file_exists(templated_file_path):
        return templated_file_path

    max_attempts = 10
    for i in range(1, max_attempts + 1):
        suffix = Template(duplicate_file_suffix).substitute(num=i)
        templated_file_path_with_suffix = templated_file_path.with_stem(f"{templated_file_path.stem}{suffix}")

        # If the source file path is the same as the templated file path with suffix,
        # then the path is unique
        if are_paths_equal(source_file_path, templated_file_path_with_suffix):
            return source_file_path

        # If the templated file path with a new suffix does not exist, then the path is unique
        if not file_exists(templated_file_path_with_suffix):
            return templated_file_path_with_suffix

    raise RuntimeError(f"Failed to generate unique file path after {max_attempts} attempts: {source_file_path}")
