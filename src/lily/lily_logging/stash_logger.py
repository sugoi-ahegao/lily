import sys


class StashLogger:
    def trace(self, message: str):
        self._log_to_stash(b"t", message)

    def debug(self, message: str):
        self._log_to_stash(b"d", message)

    def info(self, message: str):
        self._log_to_stash(b"i", message)

    def warn(self, message: str):
        self._log_to_stash(b"w", message)

    def error(self, message: str):
        self._log_to_stash(b"e", message)

    def _get_log_prefix(self, level_char: bytes):
        start_level_char = b"\x01"
        end_level_char = b"\x02"

        result = start_level_char + level_char + end_level_char
        return result.decode()

    def _log_to_stash(self, level_char: bytes, message: str):
        full_message = self._get_log_prefix(level_char) + message + "\n"
        print(full_message, file=sys.stderr, flush=True)


def get_stash_logger():
    return StashLogger()
