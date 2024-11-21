import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from lily.utils.path_utils import dir_exists, file_exists


@dataclass(frozen=True)
class PluginArgs:
    user_settings_path: Path
    plugin_dir: Path
    logging_config_file_path: Optional[Path]


def parse_plugin_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-settings-path", required=True, type=lambda x: is_valid_file(parser, x))
    parser.add_argument("--plugin-dir", required=True, type=lambda x: is_valid_dir(parser, x))
    parser.add_argument("--logging-config-file-path", required=False, type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()

    plugin_args = PluginArgs(**vars(args))

    return plugin_args


def is_valid_file(parser: argparse.ArgumentParser, arg: str):
    if not file_exists(Path(arg)):
        parser.error("The file '%s' does not exist!" % arg)
    else:
        return Path(arg)


def is_valid_dir(parser: argparse.ArgumentParser, arg: str):
    if not dir_exists(Path(arg)):
        parser.error("The directory '%s' does not exist!" % arg)
    else:
        return Path(arg)
