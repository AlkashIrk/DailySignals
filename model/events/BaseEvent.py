from datetime import datetime

from dateutil import tz


class BaseEvent:
    time: datetime

    def __init__(self):
        self.time = datetime.now(tz.gettz("UTC"))

    @classmethod
    def event_name(cls) -> str:
        return cls.__name__
