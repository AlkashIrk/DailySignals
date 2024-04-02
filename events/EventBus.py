from typing import Any

from pyee import EventEmitter

from events.CandleEvent import CandleEvent
from model.MemSignalRepository import MemSignalRepository
from model.Singleton import Singleton


class EventBus(Singleton):
    ee: EventEmitter

    def __init__(self):
        self.ee = EventEmitter()

        # регистрация вызова методов по события
        self.__configure()

    def emit(self,
             event: str,
             *args: Any,
             **kwargs: Any, ):
        self.ee.emit(event, *args, **kwargs)

    def __configure(self):
        self.ee.on(CandleEvent.event_name(), MemSignalRepository.calculate)
