import logging
import uuid
from contextlib import contextmanager
from typing import Any, MutableMapping, Optional

RUN_ID = str(uuid.uuid4())[:5]
_scene_id: Optional[int] = None
_rule_id: Optional[int] = None


class LilyLoggerAdapter(logging.LoggerAdapter[logging.Logger]):
    def process(self, msg: Any, kwargs: MutableMapping[str, Any]) -> tuple[Any, MutableMapping[str, Any]]:
        prefix = f"[run-{RUN_ID}]"

        if _scene_id is not None:
            prefix += f" [scene-{_scene_id}]"

        if _rule_id is not None:
            prefix += f" [rule-{_rule_id}]"

        new_message = "%s %s" % (prefix, msg)

        return new_message, kwargs

    @classmethod
    @contextmanager
    def with_scene_id(cls, scene_id: Optional[int]):
        global _scene_id

        _scene_id = scene_id

        try:
            yield
        finally:
            _scene_id = None

    @classmethod
    @contextmanager
    def with_rule_id(cls, rule_id: int):
        global _rule_id

        _rule_id = rule_id

        try:
            yield
        finally:
            _rule_id = None
