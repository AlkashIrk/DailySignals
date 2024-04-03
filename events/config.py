from model.events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from model.events.CandleEvent import CandleEvent
from model.events.EventBus import EventBus
from model.repository.MemSignalRepository import MemSignalRepository
from signals.calculate import calculate_signals


def init_event_bus():
    # при событии CandleEvent проверяем необходимость пересчета индикаторов
    EventBus.register_handler(CandleEvent.event_name(), MemSignalRepository.calculate)

    # при событии CalculateIndicatorsEvent запускаем пересчет индикаторов
    EventBus.register_handler(CalculateIndicatorsEvent.event_name(), calculate_signals)
