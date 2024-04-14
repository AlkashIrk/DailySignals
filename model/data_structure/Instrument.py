from dataclasses import dataclass


@dataclass
class Instrument:
    figi: str
    name: str
    ticker: str
    last_price: float = 0
