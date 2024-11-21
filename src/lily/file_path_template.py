import re
from string import Template

from lily.fields.date_field import format_date_field
from lily.fields.performers_field import format_performers_field
from lily.fields.rating_field import format_rating_field
from lily.fields.resolution_field import format_resolution_field
from lily.fields.source_video_dir_field import format_source_video_dir_field
from lily.fields.studio_field import format_studio_field
from lily.fields.studio_hierarchy_as_path_field import format_studio_hierarchy_as_path_field
from lily.fields.studio_hierarchy_field import format_studio_hierarchy_field
from lily.fields.title_field import format_title_field
from lily.fields.watched_field import format_watched_field
from lily.models.user_settings.field_settings import FieldSettings
from lily.stash_context import StashContext


def generate_file_dir(template_file_path: str, run_context: StashContext, field_settings: FieldSettings) -> str:
    ctx = run_context

    new_file_dir = (
        Template(template_file_path)
        .safe_substitute(
            {
                "date": format_date_field(ctx.scene.date, field_settings.date),
                "rating": format_rating_field(ctx.scene, field_settings.rating),
                "resolution": format_resolution_field(ctx.video_file, field_settings.resolution),
                "studio": format_studio_field(ctx.scene.studio, field_settings.studio),
                "studio_hierarchy_as_path": format_studio_hierarchy_as_path_field(
                    ctx.scene.studio, ctx.studios, field_settings.studio_hierarchy_as_path
                ),
                "source_video_dir": format_source_video_dir_field(ctx.video_file),
            }
        )
        .strip()
    )

    unknown_fields = Template(new_file_dir).get_identifiers()

    if len(unknown_fields) > 0:
        raise Exception(f"Unknown fields in template: {unknown_fields}")

    # Use typewriter for Apostrophe
    new_file_dir = re.sub("[’‘”“]+", "'", new_file_dir)

    # Remove illegal characters for Windows file paths
    new_file_dir = re.sub(r'[<>"|?*]', "", new_file_dir)

    return new_file_dir


def generate_file_name(template_file_name: str, run_context: StashContext, field_settings: FieldSettings):
    ctx = run_context

    new_file_name = (
        Template(template_file_name)
        .safe_substitute(
            {
                "title": format_title_field(ctx.scene.title, field_settings.title),
                "date": format_date_field(ctx.scene.date, field_settings.date),
                "performers": format_performers_field(ctx.scene.performers, field_settings.performers),
                "rating": format_rating_field(ctx.scene, field_settings.rating),
                "resolution": format_resolution_field(ctx.video_file, field_settings.resolution),
                "studio": format_studio_field(ctx.scene.studio, field_settings.studio),
                "studio_hierarchy": format_studio_hierarchy_field(
                    ctx.scene.studio, ctx.studios, field_settings.studio_hierarchy
                ),
                "watched": format_watched_field(ctx.scene, field_settings.watched),
            }
        )
        .strip()
    )

    unknown_fields = Template(new_file_name).get_identifiers()

    if len(unknown_fields) > 0:
        raise Exception(f"Unknown fields in template: {unknown_fields}")

    # Replace apostrophes with typewriter apostrophes
    new_file_name = re.sub("[’‘”“]+", "'", new_file_name)

    # Remove illegal characters for Windows file names
    new_file_name = re.sub(r'[<>:"/\\|?*]', "", new_file_name)

    # Remove extra spaces
    new_file_name = re.sub(r"\s+", " ", new_file_name)

    return new_file_name
