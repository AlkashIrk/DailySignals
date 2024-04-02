import datetime

from events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from events.CandleEvent import CandleEvent
from events.EventBus import EventBus
from model.Config import Config
from model.Singleton import Singleton


class MemSignalRepository(Singleton):
    """
    inMemory репозиторий сигналов по инструментам
    """
    instruments = {}

    @classmethod
    def calculate(cls, event: CandleEvent):
        figi = event.figi

        last_calculate_time = cls.instruments.get(figi, 0)
        current_time = datetime.datetime.now()

        if last_calculate_time == 0 or (
                current_time > last_calculate_time + datetime.timedelta(minutes=Config().calculate_signals_interval)):
            cls.instruments.update({figi: current_time})

            # сообщение в EventBus о необходимости расчета индикаторов
            EventBus.emit(CalculateIndicatorsEvent.event_name(),
                          CalculateIndicatorsEvent(event=event)
                          )
