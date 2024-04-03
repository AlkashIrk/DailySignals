from typing import Any, Optional

from pyee import EventEmitter
from pyee.base import Handler

from model.Singleton import Singleton


class EventBus(Singleton):
    ee = EventEmitter()

    @classmethod
    def emit(cls,
             event: str,
             *args: Any,
             **kwargs: Any, ):
        cls.ee.emit(event, *args, **kwargs)

    @classmethod
    def register_handler(cls, event: str, f: Optional[Handler] = None):
        cls.ee.on(event, f)
