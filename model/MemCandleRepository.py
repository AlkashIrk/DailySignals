from dateutil.tz import tz
from tinkoff.invest import Candle

from commons.tinkoff.history_data import get_history_candles
from events.CandleEvent import CandleEvent
from events.EventBus import EventBus
from model.CandlesInfo import CandlesInfo, CandleInfo
from model.Config import Config
from model.Instrument import Instrument
from model.Singleton import Singleton


class MemCandleRepository(Singleton):
    """
    inMemory репозиторий инструментов и свечей
    """
    instruments = {}
    candles = {}

    @classmethod
    def update_instruments(cls, instruments_: dict):
        cls.instruments = instruments_

        # загрузка исторических свечей по инструментам
        cls.__prepare_candles()

    @classmethod
    def update_candles(cls, event: Candle, print_to_console=False):
        """
        Обновление данных в репозитории для свечей
        :param event: событие по свече
        :param print_to_console: необходим ли вывод свечи в консоль 
        :return: 
        """""
        figi = event.figi

        candles = cls.__get_candles(event)

        candle = CandleInfo().fill_by_candle_event(candle_event=event)
        if print_to_console:
            candle.print(instrument=MemCandleRepository.instruments.get(figi),
                         to_zone=tz.gettz("Europe/Moscow"))

        candles.append(candle_info=candle)
        cls.candles.update({figi: candles})

        # сообщение в EventBus о новой свече
        EventBus().emit(CandleEvent.event_name(), CandleEvent(figi))

    @classmethod
    def __get_candles(cls, event: Candle) -> CandlesInfo:
        """
        Получение свечей по Candel-event из памяти
        :param event:
        :return:
        """

        figi = event.figi
        interval = event.interval

        candles = cls.candles.get(figi)
        if candles is None:
            instrument: Instrument = cls.instruments.get(figi)
            candles: CandlesInfo = CandlesInfo(instrument, interval)

        return candles

    @classmethod
    def __prepare_candles(cls):
        """
        Проверка наличия достаточного количества свечей для расчета осциляторов/индикаторов
        :return:
        """

        for instrument in cls.instruments.values():
            instrument: Instrument = instrument
            figi = instrument.figi
            candles_in_memory = cls.candles.get(figi)

            if candles_in_memory is None:
                historic = get_history_candles(instrument=instrument)
                candles_info = CandlesInfo(instrument, Config().subscription_interval)
                candles_info.append_historic(historic)
                cls.candles.update({figi: candles_info})
