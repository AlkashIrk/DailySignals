from dateutil.tz import tz
from tinkoff.invest import Candle

from commons.tinkoff.history_data import get_history_candles
from model.Singleton import Singleton
from model.config.Config import Config
from model.data_structure.CandlesInfo import CandlesInfo, CandleInfo
from model.data_structure.Instrument import Instrument
from model.events.CalculateIndicatorsEvent import CalculateIndicatorsEvent
from model.events.CandleEvent import CandleEvent
from model.events.EventBus import EventBus
from model.signals.PandasData import PandasData


class MemCandleRepository(Singleton):
    """
    inMemory репозиторий инструментов и свечей
    """
    instruments = {}
    candles = {}

    @classmethod
    def update_instruments(cls, instruments_: dict):
        cls.instruments = instruments_

        cls.candles.clear()

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
        interval = event.interval
        instrument: Instrument = MemCandleRepository.instruments.get(figi)

        candles = cls.__get_candles(event)

        candle = CandleInfo().fill_by_candle_event(candle_event=event)
        if print_to_console:
            candle.print(instrument=MemCandleRepository.instruments.get(figi),
                         to_zone=tz.gettz("Europe/Moscow"))

        candles.append(candle_info=candle)
        cls.candles.update({figi: candles})

        # последняя цена по инструменту
        instrument.last_price = candle.close

        # сообщение в EventBus о новой свече
        EventBus.emit(CandleEvent.event_name(),
                      CandleEvent(figi=figi, interval=interval)
                      )

    @classmethod
    def get_all_candles(cls) -> dict:
        return cls.candles

    @classmethod
    def __get_candles(cls, event: Candle) -> CandlesInfo:
        """
        Получение свечей по Candle-event из памяти
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
    def __get_candles_by_indicator_event(cls, event: CalculateIndicatorsEvent) -> CandlesInfo:
        """
        Получение свечей по CalculateIndicatorsEvent из памяти
        :param event:
        :return:
        """

        figi = event.figi
        interval = event.interval

        candles = cls.candles.get(figi)
        if candles is None:
            instrument: Instrument = cls.instruments.get(figi)
            candles: CandlesInfo = CandlesInfo(instrument, interval)

        # проверяем размер коллекции свечей в памяти
        # при необходимости оставляем только последние актуальные
        candles_limit_size = Config().candles_for_calculation_min_size
        if len(candles.candles) > candles_limit_size:
            candles_sorted_list = list(candles.candles)
            candles_sorted_list.sort()
            candles.candles = set(candles_sorted_list[-candles_limit_size:])

        return candles

    @classmethod
    def __prepare_candles(cls):
        """
        Проверка наличия достаточного количества свечей для расчета осцилляторов/индикаторов
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

    @classmethod
    def get_pandas_data(cls, event: CalculateIndicatorsEvent) -> PandasData:
        candles = cls.__get_candles_by_indicator_event(event)
        return PandasData(candles=candles)
