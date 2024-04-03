import time
from dataclasses import dataclass

import pandas as pd
from ta.volatility import KeltnerChannel

from model.signals import Signal
from model.signals.PandasData import PandasData


@dataclass
class KeltChannel(Signal):
    df: pd.DataFrame
    signal_name = "KeltnerChannel"
    calc_time = 0
    round_var = 3

    def __init__(self, data: PandasData, window=20, original_version=False, window_atr=1):
        start_time = time.time()
        df = data.df.drop(columns=['open'])

        signal = KeltnerChannel(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            window=window,
            original_version=original_version,
            window_atr=window_atr
        )

        df[self.signal_name] = signal.keltner_channel_lband()
        self.df = df
        self.calc_time = time.time() - start_time

        super().update_values()
