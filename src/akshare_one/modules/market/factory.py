from .base import BillboardProvider
from .eastmoney import EastMoneyBillboard


class BillboardFactory:
    @staticmethod
    def create(symbol: str, provider: str = "eastmoney") -> BillboardProvider:
        if provider == "eastmoney":
            return EastMoneyBillboard(symbol)
        raise ValueError(f"Unknown provider: {provider}")
