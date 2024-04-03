from model.events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from model.repository.MemCandleRepository import MemCandleRepository
from model.signals import *


def calculate_signals(event: CalculateIndicatorsEvent):
    pd_data = MemCandleRepository.get_pandas_data(event)

    rsi = RSI(pd_data)
    rsi.print_info()

    sto = STO(pd_data)
    sto.print_info()

    uo = UO(pd_data)
    uo.print_info()

    kc = KeltChannel(pd_data)
    kc.print_info()
