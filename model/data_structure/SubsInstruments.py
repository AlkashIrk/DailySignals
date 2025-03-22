from dataclasses import dataclass

from tinkoff.invest import SubscriptionInterval, CandleInstrument, InfoInstrument

from commons.tinkoff.check_instrument import get_instrument
from model.data_structure.Instrument import Instrument


@dataclass
class SubsInstruments:
    instruments: list
    interval: SubscriptionInterval

    def set_instruments(self, instruments: list):
        self.instruments = instruments

    def get_subscribe_list_for_candles(self):
        """
        Подготовка списка для подписки на свечи
        :return:
        """
        candle_subs = []

        for instrument in self.instruments:
            instrument: Instrument = instrument
            candle_subs.append(CandleInstrument(figi=instrument.figi, interval=self.interval))

        return candle_subs

    def get_subscribe_list_for_trade_info(self):
        """
        Подготовка списка для подписки на состояние торгов
        :return:
        """
        info_subs = []

        for instrument in self.instruments:
            instrument: Instrument = instrument
            info_subs.append(InfoInstrument(figi=instrument.figi))

        return info_subs

    def get_instrument_by_figi_dict(self):
        """
        Получение списка инструментов
        :return:
        """
        instrument_dict = {}

        for instrument in self.instruments:
            instrument: Instrument = instrument
            instrument_dict.update({instrument.figi: instrument})

        return instrument_dict

    def check(self):
        """
        Проверка наличия инструмента на бирже
        :return:
        """
        instrument_dict = {}
        instrument_ignore = []
        for instrument in self.instruments:
            instrument: Instrument = instrument
            value = get_instrument(instrument)
            if value is not None:
                instrument_dict.update({instrument.figi: instrument})
            else:
                instrument_ignore.append(instrument)

        for instrument in instrument_ignore:
            self.instruments.remove(instrument)

        return instrument_dict
