from dataclasses import dataclass

from tinkoff.invest import SubscriptionInterval, CandleInstrument, InfoInstrument

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
