import time
from dataclasses import dataclass

import pandas as pd
from ta.momentum import RSIIndicator

from model.signals.Indicator import Indicator
from model.signals.PandasData import PandasData


@dataclass
class RSI(Indicator):
    df: pd.DataFrame
    signal_name = "RSI"
    calc_time = 0

    def __init__(self, data: PandasData, window=5):
        start_time = time.time()
        df = data.df.drop(columns=['open', 'low', 'high'])

        signal = RSIIndicator(
            close=df["close"],
            window=window
        )
        df[self.signal_name] = signal.rsi()
        self.df = df
        self.calc_time = time.time() - start_time

        super().update_values()
