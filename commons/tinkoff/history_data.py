from datetime import datetime, timedelta
from time import sleep
from typing import Optional, List

from pytz import timezone
from tinkoff.invest import SubscriptionInterval

from commons.tinkoff.api_v2 import authorize
from model.config.Config import Config
from model.data_structure.AuthData import AuthData
from model.data_structure.Instrument import Instrument


def get_history_candles(
        instrument: Instrument,
        candles_size=0,
        level=0,
        date_to: Optional[datetime] = None, ) -> List["HistoricCandle"]:
    """
    Получение свечей через запрос
    :param instrument: запрашиваемый инструмент
    :param candles_size: количество свечей для рекурсивного вызова
    :param level: уровень рекурсии
    :param date_to: конечная дата запроса
    :return:
    """

    auth = AuthData(token=Config().tinkoff_token)

    if date_to is None:
        date_to = datetime.now(timezone("Europe/Moscow"))

    # ограничения по максимальному запрашиваемому периоду
    # https://russianinvestments.github.io/investAPI/load_history/
    if Config().subscription_interval == SubscriptionInterval.SUBSCRIPTION_INTERVAL_30_MIN:
        date_from = date_to - timedelta(days=2)
    elif Config().subscription_interval == SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_HOUR:
        date_from = date_to - timedelta(days=7)
    elif Config().subscription_interval in (SubscriptionInterval.SUBSCRIPTION_INTERVAL_2_HOUR,
                                            SubscriptionInterval.SUBSCRIPTION_INTERVAL_4_HOUR):
        date_from = date_to - timedelta(weeks=4)
    elif Config().subscription_interval == SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_DAY:
        date_from = date_to - timedelta(weeks=16)
    elif Config().subscription_interval == SubscriptionInterval.SUBSCRIPTION_INTERVAL_WEEK:
        date_from = date_to - timedelta(weeks=50)
    elif Config().subscription_interval == SubscriptionInterval.SUBSCRIPTION_INTERVAL_MONTH:
        date_from = date_to - timedelta(weeks=200)
    else:
        date_from = date_to - timedelta(days=1)

    with authorize(auth=auth) as client:
        try:
            response = client.market_data.get_candles(
                figi=instrument.figi,
                from_=date_from,
                to=date_to,
                interval=Config().subscription_interval
            )
        except Exception as e:
            print("\t%s" % e)
            return []
        result = response.candles
        if len(result) + candles_size < Config().candles_for_calculation_min_size:
            # лимит 300 запросов в минуту (Сервис котировок)
            # https://russianinvestments.github.io/investAPI/limits/
            sleep(0.25)
            if level < 10:
                previous_period = get_history_candles(instrument=instrument,
                                                      candles_size=len(result) + candles_size,
                                                      level=level + 1,
                                                      date_to=date_from)
            else:
                previous_period = []
            previous_period.extend(result)
            result = previous_period
    return result
