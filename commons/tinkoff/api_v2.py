from tinkoff.invest import AsyncClient, Client, Quotation

from model.AuthData import AuthData


def authorize_async(auth: AuthData) -> AsyncClient:
    return AsyncClient(token=auth.token)


def authorize(auth: AuthData) -> Client:
    return Client(token=auth.token)


def get_float_from_quo(value: Quotation) -> float:
    """
    Получение float из Quotation
    """
    try:
        nano = value.nano / (10 ** 9)
    except:
        nano = 0

    try:
        units = value.units
    except:
        units = 0

    value = units + nano
    return value
