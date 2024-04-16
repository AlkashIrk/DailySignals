from model.events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from model.events.CandleEvent import CandleEvent
from model.events.EventBus import EventBus
from model.events.SignalEvent import SignalEvent
from model.repository.MemSignalRepository import MemSignalRepository
from signals.calculate import calculate_signals
from signals.send import send_signal


def init_event_bus():
    # при событии CandleEvent проверяем необходимость пересчета индикаторов
    EventBus.register_handler(CandleEvent.event_name(), MemSignalRepository.calculate)

    # при событии CalculateIndicatorsEvent запускаем пересчет индикаторов
    EventBus.register_handler(CalculateIndicatorsEvent.event_name(), calculate_signals)

    # отправка сообщения в Telegram
    EventBus.register_handler(SignalEvent.event_name(), send_signal)
