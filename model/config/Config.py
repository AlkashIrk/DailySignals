import os
import warnings

import yaml
from tinkoff.invest import SubscriptionInterval

from commons.search_helper import case_insensitive
from model.Singleton import Singleton
from model.config.Attributes import Attributes

warnings.simplefilter(action='ignore', category=FutureWarning)

# путь до конфигурации по умолчанию
DEFAULT_CONFIG_PATH = "config/config.yaml"

# путь до конфигурации сигналов по умолчанию
DEFAULT_SIGNALS_CONFIG_PATH = "config/signals.yaml"

# путь до файла с инструментами
DEFAULT_CSV_FILE = "config/shares.csv"

# подписка на интервал в 15 минут по умолчанию
DEFAULT_SUBSCRIPTION_INTERVAL = "15m"

# количество используемых свечей для расчета индикаторов 100 по умолчанию
DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE = 100

# интервалы для свечей
allow_intervals = ["1m", "2m", "3m", "5m", "10m", "15m", "30m",
                   "1h", "2h", "4h",
                   "1day", "1week", "1month"
                   ]


class Config(Singleton):
    # путь до файла конфигурации
    config_path: str

    # путь до файла конфигурации сигналов
    config_signals_path: str

    # токен для подключения к API Тинькофф Инвестиции
    tinkoff_token: str

    # включены ли сообщения в Telegram
    telegram_enabled: bool

    # токен для отправки сообщений в Telegram
    telegram_token: str

    # ID чата для сообщения
    telegram_chat_id: str

    # путь до файла с инструментами
    csv_file_with_shares: str

    # интервал подписки
    subscription_interval: SubscriptionInterval

    # минимальное количество свечей для расчета
    candles_for_calculation_min_size: int

    # интервал (в минутах) для расчета сигналов
    calculate_signals_interval: int

    # интервал (в минутах) для ограничения отправки сообщений в чат
    signals_interval: int

    first_load = True

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path

        if self.first_load:
            # чтение файла конфигурации
            self.__read_config()
            self.first_load = False

    def __read_config(self):
        if not os.path.isfile(self.config_path):
            text = "Файл конфигурации не обнаружен.\nОжидаемое место расположение конфигурации:\n\t{path}".format(
                path=os.path.abspath(self.config_path))
            print(text)
            exit(0)

        with open(self.config_path, 'r', encoding="UTF-8") as file:
            try:
                yaml_cfg = yaml.safe_load(file)
                self.__parse_yaml(cfg=yaml_cfg)
            except Exception as e:
                print("Exception on read cfg:\n\t%s" % e)
                exit(0)

    def __parse_yaml(self, cfg: dict):
        """
        Парсинг YAML конфигурации
        :param cfg:
        :return:
        """

        self.__parse_main_section(cfg)
        self.__parse_subscribe_section(cfg)

    def __parse_main_section(self, cfg: dict):
        """
        Чтение основной секции конфигурации
        :param cfg:
        :return:
        """
        section = self.__check_that_section_exist(cfg=cfg, section_name=Attributes.main_section)

        # чтение токена от investAPI
        self.tinkoff_token = case_insensitive(target=section,
                                              search_attribute=Attributes.tinkoff_token
                                              )
        # чтение токена от Telegram
        self.telegram_token = case_insensitive(target=section,
                                               search_attribute=Attributes.telegram_token
                                               )

        # чтение ID чата
        self.telegram_chat_id = case_insensitive(target=section,
                                                 search_attribute=Attributes.telegram_chat_id
                                                 )

        if self.telegram_token is not None and self.telegram_chat_id is not None:
            self.telegram_enabled = True
        else:
            self.telegram_enabled = False

    def __parse_subscribe_section(self, cfg: dict):
        """
        Чтение секции конфигурации по подписке на свечи
        :param cfg:
        :return:
        """
        section = self.__check_that_section_exist(cfg=cfg, section_name=Attributes.subs_section)

        # инструменты для подписки
        self.__check_csv_file_with_shares(section)

        # количество свечей для расчета индикатора
        self.__check_candles_size(section)

        # интервал свечей для подписки
        self.__check_interval(section)

        # интервал (в минутах) для расчета сигналов
        self.__check_calc_signal_interval(section)

        # интервал (в минутах) для ограничения отправки сообщений в чат
        self.__check_signal_interval(section)

        # конфигурация для расчета сигналов
        self.__check_signal_config_path(section)

    def __check_csv_file_with_shares(self, section: dict):
        config_value = case_insensitive(target=section,
                                        search_attribute=Attributes.csv_file_with_shares,
                                        default_value=DEFAULT_CSV_FILE
                                        )
        self.csv_file_with_shares = config_value


    def __check_candles_size(self, section: dict):
        """
        Чтение и валидация параметра отвечающего за сбор минимального количества свечей для расчета индикаторов
        :param section:
        :return:
        """
        config_value = case_insensitive(target=section,
                                        search_attribute=Attributes.candles_for_calculation_min_size,
                                        default_value=DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE
                                        )
        if type(config_value) != int:
            self.candles_for_calculation_min_size = DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE
            text = "\tЗначение для параметра {param} установлено по умолчанию на: {def_value}".format(
                param=Attributes.candles_for_calculation_min_size,
                def_value=DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE
            )
            print(text)
        else:
            self.candles_for_calculation_min_size = config_value
            if config_value < 100:
                text = "\tЗначение для параметра {param} [{value}] меньше рекомендуемого значения: {def_value}".format(
                    param=Attributes.candles_for_calculation_min_size,
                    value=config_value,
                    def_value=DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE
                )
                print(text)
            elif config_value > DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE * 2:
                text = "\tЗначение для параметра {param} [{value}] больше рекомендуемого значения: {def_value}".format(
                    param=Attributes.candles_for_calculation_min_size,
                    value=config_value,
                    def_value=DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE * 2
                )
                print(text)

    def __check_interval(self, section: dict):
        """
        Чтение и валидация параметра отвечающего за подписку на определенный интервал свечей
        :param section:
        :return:
        """
        intervals = {
            "1m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
            "2m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_2_MIN,
            "3m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_3_MIN,
            "5m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIVE_MINUTES,
            "10m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_10_MIN,
            "15m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIFTEEN_MINUTES,
            "30m": SubscriptionInterval.SUBSCRIPTION_INTERVAL_30_MIN,
            "1h": SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_HOUR,
            "2h": SubscriptionInterval.SUBSCRIPTION_INTERVAL_2_HOUR,
            "4h": SubscriptionInterval.SUBSCRIPTION_INTERVAL_4_HOUR,
            "1day": SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_DAY,
            "1week": SubscriptionInterval.SUBSCRIPTION_INTERVAL_WEEK,
            "1month": SubscriptionInterval.SUBSCRIPTION_INTERVAL_MONTH,
        }

        config_value = case_insensitive(target=section,
                                        search_attribute=Attributes.interval
                                        )
        if config_value is not None:
            config_value = str(config_value).lower()
            value_exist = allow_intervals.__contains__(config_value)
        else:
            value_exist = False

        if not value_exist:
            text = "\tЗначение для параметра {param} установлено по умолчанию на: {def_value}".format(
                param=Attributes.interval,
                def_value=DEFAULT_SUBSCRIPTION_INTERVAL
            )
            print(text)
            config_value = DEFAULT_SUBSCRIPTION_INTERVAL
            text = "\tДопустимые значения для параметра: " + ' '.join(allow_intervals)
            print(text)

        self.subscription_interval = intervals.get(config_value.lower())

    def __check_calc_signal_interval(self, section: dict):
        """
        Чтение и валидация параметра отвечающего за интервал расчета сигналов по индикаторам
        :param section:
        :return:
        """
        config_value = case_insensitive(target=section,
                                        search_attribute=Attributes.calculate_signals_interval
                                        )
        if type(config_value) != int:
            self.calculate_signals_interval = 30
            text = "\tЗначение для параметра {param} установлено по умолчанию на: {def_value} минут".format(
                param=Attributes.calculate_signals_interval,
                def_value=30
            )
            print(text)
        else:
            self.calculate_signals_interval = config_value

    def __check_signal_interval(self, section: dict):
        """
        Чтение и валидация параметра отвечающего за интервал отправки сигналов по индикаторам
        :param section:
        :return:
        """
        config_value = case_insensitive(target=section,
                                        search_attribute=Attributes.signals_interval
                                        )
        if type(config_value) != int:
            self.signals_interval = 360
            text = "\tЗначение для параметра {param} установлено по умолчанию на: {def_value} минут".format(
                param=Attributes.signals_interval,
                def_value=360
            )
            print(text)
        else:
            self.signals_interval = config_value

    def __check_signal_config_path(self, section: dict):
        """
        Чтение и валидация параметра отвечающего за расположение файла конфигурации сигналов
        :param section:
        :return:
        """
        config_value = case_insensitive(target=section,
                                        search_attribute=Attributes.signals_config_path,
                                        default_value=DEFAULT_SIGNALS_CONFIG_PATH
                                        )
        if not os.path.isfile(config_value):
            text = "\tФайл конфигурации для расчета сигналов не обнаружен.\n" \
                   "\tОжидаемое место расположение конфигурации:\n\t{path}" \
                .format(path=os.path.abspath(config_value))
            print(text)
            exit(0)
        self.config_signals_path = config_value

    def __check_that_section_exist(self, cfg: dict, section_name: str) -> dict:
        """
        Проверка наличия секции в файле конфигурации
        :param cfg:
        :param section_name:
        :return:
        """
        section = case_insensitive(target=cfg,
                                   search_attribute=section_name
                                   )
        if section is None:
            text = "\tФайл конфигурации не содержит секции {section_name}".format(
                section_name=section_name)
            print(text)
            exit(0)
        return section
