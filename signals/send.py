import datetime

from commons.telegram.send_to_telegram import send_to_telegram
from model.config.Config import Config
from model.events import SignalEvent

history_of_message_time = {}


def send_signal(event: SignalEvent):
    message = event.message

    interval_dict = history_of_message_time.get(event.interval, {})
    last_send_time = interval_dict.get(event.figi, 0)
    current_time = datetime.datetime.now()

    need_send = last_send_time == 0 or (
            current_time > last_send_time + datetime.timedelta(minutes=Config().signals_interval))

    if Config().telegram_enabled and need_send:
        send_to_telegram(message=message, chat_id=Config().telegram_chat_id, telegram_token=Config().telegram_token)
        interval_dict.update({event.figi: current_time})
        history_of_message_time.update({event.interval: interval_dict})
