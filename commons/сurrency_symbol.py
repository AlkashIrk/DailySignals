currency_symbol = {
    "": "",
    "rub": "₽",
    "usd": "$",
    "eur": "€",
    "cny": "¥",
    "kzt": "₸",
    "hkd": "HK$",
}


def get_symbol(currency_name: str) -> str:
    symbol = ""
    if currency_name is not None:
        symbol = currency_symbol.get(currency_name.lower(), "")

    return symbol
