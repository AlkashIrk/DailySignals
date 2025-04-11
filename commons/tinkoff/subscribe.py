import asyncio
from time import sleep

from tinkoff.invest import TradingStatus, MarketDataResponse, Candle
from tinkoff.invest.market_data_stream.async_market_data_stream_manager import AsyncMarketDataStreamManager

from commons.Timer import Timer
from commons.instruments import load_from_csv
from commons.tinkoff.api_v2 import authorize_async
from events.config import init_event_bus
from model.config.Config import Config
from model.data_structure.AuthData import AuthData
from model.data_structure.SubsInstruments import SubsInstruments
from model.repository.MemCandleRepository import MemCandleRepository

watch_dog: Timer
RECONNECT_TIMEOUT_SEC = 30
WATCHDOG_TIMEOUT_SEC = 600


def connect_to_api():
    """
    Подключение к API
    :return:
    """
    global watch_dog

    # объект для авторизации
    auth = AuthData(token=Config().tinkoff_token)

    # инициируем шину событий, для обмена сообщений
    init_event_bus()

    while True:
        try:
            # задаем список интересующих инструментов и интервал для подписки на свечи
            instruments = SubsInstruments(
                interval=Config().subscription_interval,
                instruments=load_from_csv(Config().csv_file_with_shares)
            )

            # проверяем актуальность инструментов
            instruments.check()

            # заполняем inMemory репозиторий инструментами и историческими свечами
            MemCandleRepository.update_instruments(instruments.get_instrument_by_figi_dict())
            asyncio.run(subscribe(auth, instruments))
        except Exception as inst:
            try:
                watch_dog.cancel()
            except Exception as e:
                print("\t%s" % e)
            # в случае потери связи, переподписываемся через 30 секунд
            print("\t%s" % inst)
            sleep(RECONNECT_TIMEOUT_SEC)


async def subscribe(auth: AuthData,
                    instruments: SubsInstruments
                    ):
    """
    Подписка на стримы событий
    :param auth: объект для авторизации
    :param instruments: список инструментов, для подписки
    :return:
    """
    global watch_dog

    async with authorize_async(auth=auth) as client:
        market_data_stream: AsyncMarketDataStreamManager = (
            client.create_market_data_stream()
        )

        # инициализация watch_dog подписки
        watch_dog = Timer(WATCHDOG_TIMEOUT_SEC, timeout_callback, market_data_stream)

        # подписка на свечи
        market_data_stream.candles.subscribe(instruments.get_subscribe_list_for_candles())
        sleep(1)

        # подписка на торговые статусы инструментов и расписание торгов
        market_data_stream.info.subscribe(instruments.get_subscribe_list_for_trade_info())

        async for market_data in market_data_stream:
            # перезапуск watchdog на подписку
            watch_dog.restart()
            data: MarketDataResponse = market_data
            if data.candle:
                candle_event(data.candle)
            if data.trading_status:
                info_event(data.trading_status)


async def timeout_callback(streams: AsyncMarketDataStreamManager):
    # отписка от всех стримов
    print("timeout_callback")
    try:
        for stream in streams:
            stream: AsyncMarketDataStreamManager = stream
            stream.stop()
    except Exception as e:
        print("\t%s" % e)


def candle_event(event: Candle):
    """
    Обработчик событий по свечам
    :param event:
    :return:
    """

    # обновляем репозиторий свежими данными
    MemCandleRepository.update_candles(event=event, print_to_console=False)


def info_event(event: TradingStatus):
    """
    Обработчик событий торговых статусов инструментов и расписаний торгов
    :param event:
    :return:
    """

    figi = event.figi
