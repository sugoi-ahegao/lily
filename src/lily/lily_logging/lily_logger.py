import logging
import logging.config
import logging.handlers
from typing import Any, Optional

from lily.lily_logging.lily_logger_adapter import LilyLoggerAdapter

logging_setup_complete = False


def setup_logging(logging_config_dict: Optional[dict[Any, Any]] = None, enabled: bool = True):
    global logging_setup_complete

    assert logging_setup_complete is False, "Logging can only be setup once!"

    if enabled:
        assert logging_config_dict is not None, "logging config dict must be provided if logging is enabled!"
        logging.config.dictConfig(logging_config_dict)
    else:
        assert logging_config_dict is None, "logging config dict should not be provided if logging is disabled!"
        logging.disable(logging.CRITICAL)  # Disable all logging

    logging_setup_complete = True


def get_lily_logger():
    assert logging_setup_complete, "Logging must be configured before calling getting lily logger!"

    return LilyLoggerAdapter(logging.getLogger("lily"))


def get_lily_rename_logger():
    assert logging_setup_complete, "Logging must be configured before calling getting rename logger!"

    return LilyLoggerAdapter(logging.getLogger("rename"))


def get_lily_dry_run_logger():
    assert logging_setup_complete, "Logging must be configured before calling getting dry-run logger!"

    return LilyLoggerAdapter(logging.getLogger("dry-run"))
