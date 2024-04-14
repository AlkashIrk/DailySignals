import time
from dataclasses import dataclass

import pandas as pd
from ta.momentum import StochasticOscillator

from model.signals.Indicator import Indicator
from model.signals.PandasData import PandasData


@dataclass
class STO(Indicator):
    df: pd.DataFrame
    signal_name = "STO"
    calc_time = 0

    def __init__(self, data: PandasData):
        start_time = time.time()
        df = data.df.drop(columns=['open'])

        signal = StochasticOscillator(
            close=df["close"],
            low=df["low"],
            high=df["high"]
        )
        df[self.signal_name] = signal.stoch_signal()
        self.df = df
        self.calc_time = time.time() - start_time

        super().update_values()
