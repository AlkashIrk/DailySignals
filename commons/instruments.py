import os
from typing import List

import pandas as pd
from tinkoff.invest import Share

from model.data_structure.Instrument import Instrument

CSV_SEPARATOR = '\t'


def load_from_csv(file_path: str) -> List[Instrument]:
    if not os.path.isfile(file_path):
        text = "CSV файл инструментов не обнаружен.\n\tОжидаемое место расположение файла:\n\t{path}".format(
            path=os.path.abspath(file_path))
        print(text)
        instruments = load_instruments()
    else:
        df = pd.read_csv(filepath_or_buffer=file_path, sep=CSV_SEPARATOR)
        instruments = [Instrument(**kwargs) for kwargs in df.to_dict(orient='records')]

    return instruments


def load_instruments() -> List[Instrument]:
    instruments = []

    instruments.append(Instrument(name="Сбер Банк", figi="BBG004730N88", ticker="SBER"))
    instruments.append(Instrument(name="ЛУКОЙЛ", figi="BBG004731032", ticker="LKOH"))
    instruments.append(Instrument(name="Яндекс", figi="BBG006L8G4H1", ticker="YNDX"))

    return instruments
