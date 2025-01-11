import re
from string import Template

from lily.fields.model_field_settings import FieldSettings, field_registry_file_dir, field_registry_file_name
from lily.stash_context import StashContext


def generate_file_dir(template_file_dir: str, stash_context: StashContext, field_settings: FieldSettings) -> str:
    ctx = stash_context

    # Ensure template does not contain unexpected fields
    for field_name in Template(template_file_dir).get_identifiers():
        if field_name not in field_registry_file_dir.keys():
            raise ValueError(f"Field was not found in file dir field registry: '{field_name}'")

    generated_file_dir = str(template_file_dir)

    # For each field variable in the template...
    for field_name in Template(template_file_dir).get_identifiers():
        # Get the corresponding field setting...
        field_setting = getattr(field_settings, field_name)

        # Compute the value for the field...
        formatted_field_value = field_registry_file_dir[field_name](ctx, field_setting)

        # Clean the field value...
        # replace apostrophes with typewriter apostrophes
        formatted_field_value = re.sub("[’‘”“]+", "'", formatted_field_value)
        # remove illegal characters for Windows file paths
        formatted_field_value = re.sub(r'[<>"|?*]', "", formatted_field_value)

        # Replace the field variable with its value
        generated_file_dir = Template(generated_file_dir).safe_substitute({field_name: formatted_field_value})

    return generated_file_dir.strip()


def generate_file_name(template_file_name: str, stash_context: StashContext, field_settings: FieldSettings):
    ctx = stash_context

    # Ensure template does no contain unexpected fields
    for field_name in Template(template_file_name).get_identifiers():
        if field_name not in field_registry_file_name.keys():
            raise ValueError(f"Field was not found in file name field registry: '{field_name}'")

    generated_file_name = str(template_file_name)

    # For each field variable in the template...
    for field_name in Template(template_file_name).get_identifiers():
        # Get the corresponding field setting...
        field_setting = getattr(field_settings, field_name)

        # Compute the value for the field...
        formatted_field_value = field_registry_file_name[field_name](ctx, field_setting)

        # Clean the field value...
        # replace apostrophes with typewriter apostrophes
        formatted_field_value = re.sub("[’‘”“]+", "'", formatted_field_value)
        # remove illegal characters for Windows file names
        formatted_field_value = re.sub(r'[<>:"/\\|?*]', "", formatted_field_value)
        # remove extra spaces
        formatted_field_value = re.sub(r"\s+", " ", formatted_field_value)

        # Replace the field variable with its value
        generated_file_name = Template(generated_file_name).safe_substitute({field_name: formatted_field_value})

    return generated_file_name.strip()
