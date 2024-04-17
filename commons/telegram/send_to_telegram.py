from urllib.parse import quote

import requests


def send_to_telegram(message: str,
                     chat_id=None,
                     telegram_token=None):
    message = message.replace("\t", "    ")
    message = quote(message, safe="", encoding="utf-8")

    url = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}".format(
        token=telegram_token,
        chat_id=chat_id,
        text=message)

    # убираем предпросмотр
    url = url + "&parse_mode=html&disable_web_page_preview=True"

    try:
        requests.get(url)
    except Exception as e:
        print(e)
