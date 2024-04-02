from tinkoff.invest import SubscriptionInterval

from events.BaseEvent import BaseEvent
from events.CandleEvent import CandleEvent


class CalculateIndicatorsEvent(BaseEvent):
    figi: str
    interval: SubscriptionInterval

    def __init__(self, event: CandleEvent):
        super().__init__()
        self.figi = event.figi
        self.interval = event.interval
