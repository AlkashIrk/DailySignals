import pandas as pd

from model.CandlesInfo import CandlesInfo


class PandasData:
    df: pd.DataFrame

    def __init__(self, candles: CandlesInfo):
        candles: CandlesInfo = candles
        info = candles.candles
        df = pd.DataFrame.from_records([i.to_dict() for i in info])
        df = df.sort_values(['time'])
        df.set_index('time', inplace=True, drop=False)
        self.df = df
