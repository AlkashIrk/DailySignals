from tinkoff.invest import AsyncClient, Client

from model.AuthData import AuthData


def authorize(auth: AuthData, is_async=False) -> AsyncClient:
    if is_async:
        return AsyncClient(token=auth.token)
    else:
        return Client(token=auth.token)
