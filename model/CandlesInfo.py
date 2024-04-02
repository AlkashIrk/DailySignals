from datetime import datetime
from typing import List, Optional

from dateutil.tz import tzlocal
from tinkoff.invest import SubscriptionInterval, Candle, HistoricCandle

from commons.tinkoff.api_v2 import get_float_from_quo
from model.Instrument import Instrument


class CandlesInfo:
    instrument: Instrument
    interval: SubscriptionInterval
    candles: set

    def __init__(self, instrument: Instrument, interval: SubscriptionInterval):
        self.instrument = instrument
        self.interval = interval
        self.candles = set()

    def __str__(self):
        value = "{name} ({ticker})".format(
            name=self.instrument.name,
            ticker=self.instrument.ticker
        )
        return value

    def append(self, candle_info: Optional["CandleInfo"]):
        self.candles.discard(candle_info)
        self.candles.add(candle_info)

    def append_historic(self, historic: List["HistoricCandle"]):
        for historic_candle in historic:
            ca = CandleInfo().fill_by_history(figi=self.instrument.figi,
                                              interval=self.interval,
                                              historic_candle=historic_candle)
            self.candles.add(ca)


class CandleInfo:
    time: datetime
    figi: str
    interval: SubscriptionInterval
    volume: int
    open: float
    close: float
    low: float
    high: float

    def fill_by_candle_event(self, candle_event: Candle):
        self.figi = candle_event.figi
        self.interval = candle_event.interval

        self.time = candle_event.time
        self.volume = candle_event.volume

        self.open = get_float_from_quo(candle_event.open)
        self.close = get_float_from_quo(candle_event.close)
        self.low = get_float_from_quo(candle_event.low)
        self.high = get_float_from_quo(candle_event.high)
        return self

    def fill_by_history(self,
                        figi: str,
                        interval: SubscriptionInterval,
                        historic_candle: HistoricCandle):
        self.figi = figi
        self.interval = interval

        self.time = historic_candle.time
        self.volume = historic_candle.volume

        self.open = get_float_from_quo(historic_candle.open)
        self.close = get_float_from_quo(historic_candle.close)
        self.low = get_float_from_quo(historic_candle.low)
        self.high = get_float_from_quo(historic_candle.high)
        return self

    def __eq__(self, other):
        if isinstance(other, CandleInfo):
            return self.figi == other.figi and \
                   self.interval == other.interval and \
                   self.time == other.time
        return False

    def __hash__(self):
        return hash((self.figi, self.interval, self.time))

    def __lt__(self, other):
        return self.time.__lt__(other.time)

    def __str__(self):
        value = "{time} o={open} c={close} low={low} high={high} v={volume}".format(
            time=self.time,
            open=self.open,
            close=self.close,
            low=self.low,
            high=self.high,
            volume=self.volume
        )

        return value

    def to_dict(self):
        return {
            'time': self.time,
            'open': self.open,
            'close': self.close,
            'low': self.low,
            'high': self.high,
            'volume': self.volume
        }

    def print(self,
              instrument: Optional[Instrument] = None,
              to_zone: Optional[tzlocal] = None
              ):

        local_time = self.time
        if to_zone is not None:
            local_time = self.time.astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")

        if instrument is not None:
            value = "{time} {name} ".format(
                name=instrument.name,
                time=local_time
            )
        else:
            value = "{time} ".format(
                time=local_time)

        value = value + "o={open} c={close} l={low} h={high} v={volume}".format(
            open=self.open,
            close=self.close,
            low=self.low,
            high=self.high,
            volume=self.volume
        )

        print(value)
