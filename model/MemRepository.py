from dateutil.tz import tz
from tinkoff.invest import Candle

from commons.tinkoff.history_data import get_history_candles
from model.CandlesInfo import CandlesInfo, CandleInfo
from model.Config import Config
from model.Instrument import Instrument
from model.Singleton import Singleton


class MemRepository(Singleton):
    """
    inMemory репозиторий инструментов и свечей
    """
    instruments = {}
    candles = {}

    def update_instruments(self, instruments_: dict):
        self.instruments = instruments_

        # загрузка исторических свечей по инструментам
        self.__prepare_candles()

    def update_candles(self, event: Candle, print_to_console=False):
        """
        Обновление данных в репозитории для свечей
        :param event: событие по свече
        :param print_to_console: необходим ли вывод свечи в консоль 
        :return: 
        """""
        figi = event.figi

        candles = self.__get_candles(event)

        candle = CandleInfo().fill_by_candle_event(candle_event=event)
        if print_to_console:
            candle.print(instrument=MemRepository().instruments.get(figi),
                         to_zone=tz.gettz("Europe/Moscow"))

        candles.append(candle_info=candle)
        self.candles.update({figi: candles})

    def __get_candles(self, event: Candle) -> CandlesInfo:
        """
        Получение свечей по Candel-event из памяти
        :param event:
        :return:
        """

        figi = event.figi
        interval = event.interval

        candles = self.candles.get(figi)
        if candles is None:
            instrument: Instrument = self.instruments.get(figi)
            candles: CandlesInfo = CandlesInfo(instrument, interval)

        return candles

    def __prepare_candles(self):
        """
        Проверка наличия достаточного количества свечей для расчета осциляторов/индикаторов
        :return:
        """

        for instrument in self.instruments.values():
            instrument: Instrument = instrument
            figi = instrument.figi
            candles_in_memory = self.candles.get(figi)

            if candles_in_memory is None:
                historic = get_history_candles(instrument=instrument)
                candles_info = CandlesInfo(instrument, Config().subscription_interval)
                candles_info.append_historic(historic)
                self.candles.update({figi: candles_info})
