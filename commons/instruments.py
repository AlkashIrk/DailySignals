from typing import List

from model.Instrument import Instrument


def load_instruments() -> List[Instrument]:
    instruments = []

    instruments.append(Instrument(name="Сбер Банк", figi="BBG004730N88", ticker="SBER"))
    instruments.append(Instrument(name="ЛУКОЙЛ", figi="BBG004731032", ticker="LKOH"))
    instruments.append(Instrument(name="Яндекс", figi="BBG006L8G4H1", ticker="YNDX"))

    return instruments
