import time

import numpy as np
import pandas as pd
from pandas import DataFrame

from model.repository.MemCandleRepository import MemCandleRepository

cached_data = {}
cache_period = 10


def prepare_instruments() -> DataFrame:
    global cached_data

    cached_key = "all_instruments"
    cached = get_cached_data(cached_key)
    if cached is not None:
        return cached

    values = dict(MemCandleRepository.get_all_candles())

    result = []
    for k, v in values.items():
        row = {
            "id": v.instrument.ticker,
            "name": v.instrument.name,
            "ticker": v.instrument.ticker,
            "figi": v.instrument.figi,
            "last_price": v.instrument.last_price
        }
        result.append(row)

    pd_data = pd.DataFrame(result)

    ts = time.time()
    cached = {cached_key: dict(ts=ts, data=pd_data)}
    cached_data.update(cached)
    return pd_data


def prepare_candles() -> DataFrame:
    global cached_data

    cached_key = "last_candles"
    cached = get_cached_data(cached_key)
    if cached is not None:
        return cached

    slice = pd.DataFrame()
    pd_data = get_full_PD()

    if pd_data.shape[0] != 0:
        pd_data.sort_values(['update_moment', 'time', 'name'], ascending=[False, False, True], inplace=True)
        slice = pd_data[:50]
        slice['time'] = slice['time'].astype(int) / 10 ** 9
        slice['id'] = np.arange(slice.shape[0])
        slice = slice[['id', 'name', 'ticker', 'time', 'open', 'close', 'low', 'high', 'volume', 'update_moment']]

        cols = ['open', 'close', 'low', 'high']
        for c in cols:
            slice[c] = slice[c].apply(lambda x: round(x, 3))

    ts = time.time()
    cached = {cached_key: dict(ts=ts, data=slice)}
    cached_data.update(cached)
    return slice


def prepare_candles_ticker(ticker: str) -> DataFrame:
    cached_key = "candles_{ticker}".format(ticker=ticker)
    cached = get_cached_data(cached_key)
    if cached is not None:
        return cached

    slice = pd.DataFrame()
    pd_data = get_full_PD()

    if pd_data.shape[0] != 0:
        slice = pd_data.loc[pd_data['ticker'].isin([ticker])]
        slice.sort_values(['update_moment', 'time', 'name'], ascending=[False, False, True], inplace=True)
        slice = slice[:50]
        slice['time'] = slice['time'].astype(int) / 10 ** 9
        slice['id'] = np.arange(slice.shape[0])
        slice = slice[['id', 'name', 'ticker', 'time', 'open', 'close', 'low', 'high', 'volume', 'update_moment']]

        cols = ['open', 'close', 'low', 'high']
        for c in cols:
            slice[c] = slice[c].apply(lambda x: round(x, 3))

    ts = time.time()
    cached = {cached_key: dict(ts=ts, data=slice)}
    cached_data.update(cached)

    return slice


def get_full_PD() -> DataFrame:
    global cached_data

    cached_key = "all_candles"
    cached = get_cached_data(cached_key)
    if cached is not None:
        return cached

    values = dict(MemCandleRepository.get_all_candles())
    result = []

    for k, v in values.items():
        row = {
            "name": v.instrument.name,
            "ticker": v.instrument.ticker
        }

        for candle in v.candles:
            from model.data_structure.CandlesInfo import CandleInfo
            candle: CandleInfo = candle
            c = candle.to_dict()
            c.update(row)
            result.append(c)

    pd_data = pd.DataFrame(result)
    # pd_data.to_csv('candles.csv', sep='\t', encoding='utf-8', index=False)
    # pd_data = pd.read_csv('candles.csv', sep='\t', encoding='utf-8')

    ts = time.time()
    cached = {cached_key: dict(ts=ts, data=pd_data)}
    cached_data.update(cached)

    return pd_data


def get_cached_data(cached_key):
    global cached_data
    ts = int(time.time())

    cached = cached_data.get(cached_key)
    if cached is not None:
        last_ts = cached.get("ts")
        if ts < last_ts + cache_period:
            return cached.get("data")
    return None


def round_data(x):
    try:
        return round(x, 2)
    except:
        return x
