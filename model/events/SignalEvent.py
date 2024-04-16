from tinkoff.invest import SubscriptionInterval

from model.events.BaseEvent import BaseEvent
from model.events.CalculateIndicatorsEvent import CalculateIndicatorsEvent


class SignalEvent(BaseEvent):
    figi: str
    message: str
    interval: SubscriptionInterval

    def __init__(self, event: CalculateIndicatorsEvent, message: str):
        super().__init__()
        self.figi = event.figi
        self.interval = event.interval
        self.message = message
