from tinkoff.invest import AsyncClient, Client

from model.AuthData import AuthData


def authorize_async(auth: AuthData) -> AsyncClient:
    return AsyncClient(token=auth.token)


def authorize(auth: AuthData) -> Client:
    return Client(token=auth.token)
