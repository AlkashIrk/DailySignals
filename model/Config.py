import configparser
import os

DEFAULT_CONFIG_PATH = "config/config.cfg"


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

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path

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
