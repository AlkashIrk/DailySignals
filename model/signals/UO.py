import time
from dataclasses import dataclass

import pandas as pd
from ta.momentum import UltimateOscillator

from model.signals import Signal
from model.signals.PandasData import PandasData


@dataclass
class UO(Signal):
    df: pd.DataFrame
    signal_name = "UO"
    calc_time = 0

    def __init__(self, data: PandasData):
        start_time = time.time()
        df = data.df.drop(columns=['open'])

        signal = UltimateOscillator(
            high=df["high"],
            low=df["low"],
            close=df["close"],
        )
        df[self.signal_name] = signal.ultimate_oscillator()
        self.df = df
        self.calc_time = time.time() - start_time

        super().update_values()
