import contextlib
from unittest.mock import patch


@contextlib.contextmanager
def patch_file_exists(return_value: bool | list[bool], assert_called: bool = True):
    with patch("lily.process_video_file.file_exists") as mock_file_exists:
        if isinstance(return_value, bool):
            mock_file_exists.return_value = return_value
        else:
            mock_file_exists.side_effect = return_value

        yield

        if assert_called:
            assert mock_file_exists.call_count > 0, "file_exists is patched, but was not called"
