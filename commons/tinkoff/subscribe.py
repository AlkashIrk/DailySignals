import asyncio
from time import sleep

from tinkoff.invest import TradingStatus, MarketDataResponse, Candle
from tinkoff.invest.market_data_stream.async_market_data_stream_manager import AsyncMarketDataStreamManager

from commons.instruments import load_instruments
from commons.tinkoff.api_v2 import authorize_async
from events.config import init_event_bus
from model.config.Config import Config
from model.data_structure.AuthData import AuthData
from model.data_structure.SubsInstruments import SubsInstruments
from model.repository.MemCandleRepository import MemCandleRepository


def connect_to_api():
    """
    Подключение к API
    :return:
    """

    # объект для авторизации
    auth = AuthData(token=Config().tinkoff_token)

    # задаем список интересующих инструментов и интервал для подписки на свечи
    instruments = SubsInstruments(
        interval=Config().subscription_interval,
        instruments=load_instruments()
    )

    # инициируем шину событий, для обмена сообщений
    init_event_bus()

    # заполняем inMemory репозиторий инструментами и историческими свечами
    MemCandleRepository.update_instruments(instruments.get_instrument_by_figi_dict())

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

    # обновляем репозиторий свежими данными
    MemCandleRepository.update_candles(event=event, print_to_console=True)


def info_event(event: TradingStatus):
    """
    Обработчик событий торговых статусов инструментов и расписаний торгов
    :param event:
    :return:
    """

    figi = event.figi
