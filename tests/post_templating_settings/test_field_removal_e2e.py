from pathlib import Path

from tests.testing_model_creators.create_performer import create_performer
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_user_settings import create_user_settings
from tests.testing_model_creators.create_video_file import create_video_file

from lily.process_video_file import process_video_file
from lily.utils.path_utils import are_paths_equal


class TestFieldRemovalOrder:
    def test_no_fields_are_removed_when_path_is_not_too_long(self):
        scene = create_scene(title="Scene Title", date="2023-01-01")
        stash_context = create_stash_context(scene=scene, video_file=create_video_file())

        template_file_dir = "/[VIDEOS]"
        template_file_name = "${title} ${date}"
        field_removal_order = ["date"]

        generated_file_path = Path("/[VIDEOS]/Scene Title 2023-01-01.mp4")

        # Test 1:
        # When full generated path < max path length
        # Then use the full generated path

        user_settings = create_user_settings(
            template_file_dir=template_file_dir,
            template_file_name=template_file_name,
            field_removal_order=field_removal_order,
            # max path length is the length of the generated path + 1
            max_path_length=len(str(generated_file_path.resolve())) + 1,
        )

        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(generated_file_path, actual_file_path)

        # Test 2:
        # When full generated path = max path length
        # Then use the full generated path

        user_settings = create_user_settings(
            template_file_dir=template_file_dir,
            template_file_name=template_file_name,
            field_removal_order=field_removal_order,
            # max path length is the same as the generated path
            max_path_length=len(str(generated_file_path.resolve())),
        )

        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(generated_file_path, actual_file_path)

    def test_field_is_removed_when_path_is_too_long(self):
        scene = create_scene(title="Scene Title", date="2023-01-01")
        stash_context = create_stash_context(scene=scene, video_file=create_video_file())

        template_file_dir = "/[VIDEOS]"
        template_file_name = "${title} ${date}"
        field_removal_order = ["date"]

        generated_file_path = Path("/[VIDEOS]/Scene Title 2023-01-01.mp4")
        generated_file_path_without_date = Path("/[VIDEOS]/Scene Title.mp4")

        # Test:
        # When full generated path > max path length
        # Then remove a field from the generated path

        user_settings = create_user_settings(
            template_file_dir=template_file_dir,
            template_file_name=template_file_name,
            field_removal_order=field_removal_order,
            # max path length is less than the generated path with date
            max_path_length=len(str(generated_file_path.resolve())) - 1,
        )

        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(generated_file_path_without_date, actual_file_path)

    def test_multiple_fields_are_removed_when_path_is_too_long(self):
        scene = create_scene(title="Scene Title", date="2023-01-01", performers=[create_performer(name="Performer 1")])
        stash_context = create_stash_context(scene=scene, video_file=create_video_file())

        template_file_dir = "/[VIDEOS]"
        template_file_name = "My Video ${title} ${date} ${performers}"
        field_removal_order = ["performers", "date", "title"]

        # full_generated_file_path = "/[VIDEOS]/My Video Scene Title 2023-01-01 Performer 1.mp4"
        generated_file_path_without_date_or_title_or_performers = Path("/[VIDEOS]/My Video.mp4")

        # Test:
        # When full generated path > max path length
        # Then keep removing fields from the full generated path until it does not exceed max path length

        user_settings = create_user_settings(
            template_file_dir=template_file_dir,
            template_file_name=template_file_name,
            field_removal_order=field_removal_order,
            # max path length is the same as the generated path without date
            max_path_length=len(str(generated_file_path_without_date_or_title_or_performers.resolve())),
        )

        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(generated_file_path_without_date_or_title_or_performers, actual_file_path)
