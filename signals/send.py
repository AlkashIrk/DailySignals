from commons.telegram.send_to_telegram import send_to_telegram
from model.config.Config import Config
from model.events import SignalEvent


def send_signal(event: SignalEvent):
    message = event.message

    if Config().telegram_enabled:
        send_to_telegram(message=message, chat_id=Config().telegram_chat_id, telegram_token=Config().telegram_token)
