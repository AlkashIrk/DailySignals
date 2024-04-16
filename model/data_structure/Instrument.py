from dataclasses import dataclass


@dataclass
class Instrument:
    figi: str
    name: str
    ticker: str
    currency: str = ""
    last_price: float = 0

    def to_dict(self):
        return {
            'figi': self.figi,
            'name': self.name,
            'ticker': self.ticker,
            'currency': self.currency
        }
