from commons import global_vars
from commons.cfg import get_param_from_cfg, read_config
from commons.tinkoff.subscribe import connect_to_api


def check_config_params():
    var_name = "tinkoff_token"
    check_param = get_param_from_cfg("Main", var_name, print_error=True, terminate=True)
    if check_param is not None:
        global_vars.tinkoff_token = check_param

    var_name = "telegram_token"
    check_param = get_param_from_cfg("Main", var_name, print_error=True, terminate=True)
    if check_param is not None:
        global_vars.telegram_token = check_param


if __name__ == '__main__':
    # открываем файл конфигурации
    read_config()
    # применяем параметры из него
    check_config_params()

    # подключаемся к API Tinkoff
    connect_to_api()
