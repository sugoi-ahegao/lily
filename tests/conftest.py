from unittest.mock import patch

import pytest
from lily.lily_logging.lily_logger import setup_logging


@pytest.fixture(scope="session", autouse=True)
def setup_pytest_logging():
    setup_logging(
        logging_config_dict={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"simple": {"format": "[%(asctime)s] %(levelname)-8s %(message)s"}},
            "handlers": {"console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "simple"}},
            "root": {"level": "DEBUG", "handlers": ["console"]},
        }
    )

    yield


@pytest.fixture(autouse=True)
def patch_file_rename():
    with patch("main.rename_video_file") as mock_rename_file:
        yield mock_rename_file

        assert (
            mock_rename_file.call_count == 0
        ), f"Test attempted to call rename video file {mock_rename_file.call_count} time(s)"


@pytest.fixture(autouse=True)
def global_patch_file_exists():
    with patch("lily.process_video_file.file_exists") as mock_file_exists:
        mock_file_exists.return_value = False

        yield mock_file_exists


@pytest.fixture(scope="session", autouse=True)
def global_patch_lily_results():
    lily_results_targets = [
        "main.LilyResults",
        "lily.process_video_file.LilyResults",
        "lily.rename_video_file.LilyResults",
    ]

    patchers = [patch(target) for target in lily_results_targets]

    for patcher in patchers:
        patcher.start()

    yield

    for patcher in patchers:
        patcher.stop()
