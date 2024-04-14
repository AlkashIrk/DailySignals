from model.events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from model.repository.MemCandleRepository import MemCandleRepository
from model.signals.Signal import Signal


def calculate_signals(event: CalculateIndicatorsEvent):
    pd_data = MemCandleRepository.get_pandas_data(event)

    signals = Signal().read_config()
    triggers_list = signals.check_signals(pd_data)

    if len(triggers_list) == 0:
        return

    instrument = MemCandleRepository.instruments.get(event.figi)
    message = signals.get_console_message(instrument=instrument, triggered_signals=triggers_list)

    print(message)
