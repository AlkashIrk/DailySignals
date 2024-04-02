from events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from model.MemCandleRepository import MemCandleRepository
from signals.model.RSI import RSI


def calculate_signals(event: CalculateIndicatorsEvent):
    pd_data = MemCandleRepository.get_pandas_data(event)

    rsi = RSI(pd_data)
    rsi.print_info()
