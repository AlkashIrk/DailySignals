import configparser
import os

from commons import global_vars

config: configparser.ConfigParser


def get_param_from_cfg(section_name: str, param_name: str, print_error=False, terminate=False):
    global config
    try:
        value = config.get(section_name, param_name)
        return value
    except Exception as e:
        if print_error:
            print("Возникла ошибка при чтении параметра конфигурации %s из секции %s" % (param_name, section_name))
            print("Exception message:\n\t%s" % e)
        if terminate:
            exit(0)
        return None


def read_config():
    global config
    if not os.path.isfile(global_vars.config_path):
        text = "Файл конфигурации не обнаружен.\nОжидаемое место расположение конфигурации:\n\t{path}".format(
            path=os.path.abspath(global_vars.config_path))
        print(text)
        exit(0)

    config = configparser.ConfigParser(interpolation=None)
    config.read(global_vars.config_path, encoding="UTF-8")
