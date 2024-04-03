from dataclasses import dataclass

from tinkoff.invest import SubscriptionInterval

from model.events.BaseEvent import BaseEvent


@dataclass
class CandleEvent(BaseEvent):
    figi: str
    interval: SubscriptionInterval

    def __init__(self, figi: str, interval: SubscriptionInterval):
        super().__init__()
        self.figi = figi
        self.interval = interval
