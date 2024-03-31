import configparser
import os

from tinkoff.invest import SubscriptionInterval

# путь до конфигурации по умолчанию
DEFAULT_CONFIG_PATH = "config/config.cfg"

# подписка на интервал в 15 минут по умолчанию
DEFAULT_SUBSCRIPTION_INTERVAL = SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIFTEEN_MINUTES

# количество используемых свечей для расчета индикаторов 100 по умолчанию
DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE = 100


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Config:
    # путь до файла конфигурации
    config_path: str

    #
    __configparser: configparser.ConfigParser

    # токен для подключения к API Тинькофф Инвестиции
    tinkoff_token: str

    # токен для отправки сообщений в телеграм
    telegram_token: str

    # интервал подписки
    subscription_interval: SubscriptionInterval

    # минимальное количество свечей для расчета
    candles_for_calculation_min_size: int

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path

        # интервал подписки по умолчанию
        self.subscription_interval = DEFAULT_SUBSCRIPTION_INTERVAL

        # количество свечей для расчета
        self.candles_for_calculation_min_size = DEFAULT_CANDLES_FOR_CALCULATION_MIN_SIZE

        # чтение файла конфигурации
        self.__read_config()

        # назначение токена от investAPI
        self.tinkoff_token = self.__get_param_from_cfg(section_name="Main",
                                                       param_name="tinkoff_token",
                                                       print_error=True,
                                                       terminate=True)

        # назначение токена от телеграма
        self.telegram_token = self.__get_param_from_cfg(section_name="Main",
                                                        param_name="telegram_token",
                                                        print_error=True,
                                                        terminate=True)

    def __read_config(self):
        if not os.path.isfile(self.config_path):
            text = "Файл конфигурации не обнаружен.\nОжидаемое место расположение конфигурации:\n\t{path}".format(
                path=os.path.abspath(self.config_path))
            print(text)
            exit(0)

        self.__configparser = configparser.ConfigParser(interpolation=None)
        self.__configparser.read(self.config_path, encoding="UTF-8")

    def __get_param_from_cfg(self, section_name: str, param_name: str, print_error=False, terminate=False):
        try:
            value = self.__configparser.get(section_name, param_name)
            return value
        except Exception as e:
            if print_error:
                print("Возникла ошибка при чтении параметра конфигурации {param_name} из секции {section_name}".format(
                    param_name=param_name,
                    section_name=section_name
                ))
                print("Exception message:\n\t%s" % e)
            if terminate:
                exit(0)
            return None
