from dataclasses import dataclass

from events.BaseEvent import BaseEvent


@dataclass
class CandleEvent(BaseEvent):
    figi: str
