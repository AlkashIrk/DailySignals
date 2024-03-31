from commons.tinkoff.subscribe import connect_to_api
from model.Config import Config

if __name__ == '__main__':
    # читаем файл конфигурации и применяем параметры
    cfg = Config()

    # подключаемся к API Tinkoff
    connect_to_api()
