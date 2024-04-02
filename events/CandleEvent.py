from dataclasses import dataclass

from events.BaseEvent import BaseEvent


@dataclass
class CandleEvent(BaseEvent):
    figi: str

    def __init__(self, figi: str):
        super().__init__()
        self.figi = figi
