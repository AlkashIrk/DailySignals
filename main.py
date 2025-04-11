import sys

from commons.tinkoff.subscribe import connect_to_api
from flask_app.flask_app import run_flask
from model.config.Config import Config

if __name__ == '__main__':
    import threading

    # читаем файл конфигурации и применяем параметры
    cfg = Config()

    try:
        # подключаемся к API Tinkoff
        t2 = threading.Thread(target=connect_to_api)
        t2.daemon = True
        t2.start()
        run_flask()
    except Exception as e:
        print("Unexpected error:" + str(e))
        sys.exit()
