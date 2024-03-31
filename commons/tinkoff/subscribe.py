import asyncio
from time import sleep
from typing import List

from tinkoff.invest import TradingStatus, MarketDataResponse, Candle
from tinkoff.invest.market_data_stream.async_market_data_stream_manager import AsyncMarketDataStreamManager

from commons.instruments import load_instruments
from commons.tinkoff.api_v2 import authorize_async
from commons.tinkoff.history_data import get_history_candles
from model.AuthData import AuthData
from model.Config import Config
from model.SubsInstruments import SubsInstruments

# коллекция свечей по инструменту с ключем FIGI
CANDLES_IN_MEMORY = {}

# коллекция инструментов с ключем FIGI
INSTRUMENT_BY_FIGI = {}


def connect_to_api():
    """
    Подключение к API
    :return:
    """

    global INSTRUMENT_BY_FIGI
    # объект для авторизации
    auth = AuthData(token=Config().tinkoff_token)

    # задаем список интересующих инструментов и интервал для подписки на свечи
    instruments = SubsInstruments(
        interval=Config().subscription_interval,
        instruments=load_instruments()
    )

    INSTRUMENT_BY_FIGI = instruments.get_instrument_by_figi_dict()

    try:
        asyncio.run(subscribe(auth, instruments))
    except Exception as inst:
        print("\t%s" % inst)


async def subscribe(auth: AuthData,
                    instruments: SubsInstruments
                    ):
    """
    Подписка на стримы событий
    :param auth: объект для авторизации
    :param instruments: список инструментов, для подписки
    :return:
    """

    # загрузка исторических свечей перед подпиской на свечи
    prepare_candles_in_memory()

    while True:
        async with authorize_async(auth=auth) as client:
            # отписка от всех
            market_data_stream: AsyncMarketDataStreamManager = (
                client.create_market_data_stream()
            )
            market_data_stream.stop()
            sleep(1)

            # подпсика на свечи
            market_data_stream.candles.subscribe(instruments.get_subscribe_list_for_candles())
            sleep(1)

            # подписка на торговые статусы инструментов и расписание торгов
            market_data_stream.info.subscribe(instruments.get_subscribe_list_for_trade_info())

            async for market_data in market_data_stream:
                data: MarketDataResponse = market_data
                if data.candle:
                    candle_event(data.candle)
                if data.trading_status:
                    info_event(data.trading_status)

        # в случае если подписка отвалится, переподписываемся через 30 секунд
        sleep(30)


def candle_event(event: Candle):
    """
    Обработчик событий по свечам
    :param event:
    :return:
    """

    figi = event.figi


def info_event(event: TradingStatus):
    """
    Обработчик событий торговых статусов инструментов и расписаний торгов
    :param event:
    :return:
    """

    figi = event.figi


def prepare_candles_in_memory():
    """
    Проверка наличия достаточного количества свечей дял расчета осциляторов
    :return:
    """
    global CANDLES_IN_MEMORY
    global INSTRUMENT_BY_FIGI

    for instrument in INSTRUMENT_BY_FIGI.values():
        figi = instrument.figi
        candles: List["HistoricCandle"] = CANDLES_IN_MEMORY.get(figi)

        if candles is None:
            historic = get_history_candles(instrument=instrument)
            CANDLES_IN_MEMORY.update({figi: historic})
