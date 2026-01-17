from .base import FundFlowProvider
from .eastmoney import EastMoneyFundFlow


class FundFlowFactory:
    @staticmethod
    def create(symbol: str, provider: str = "eastmoney") -> FundFlowProvider:
        if provider == "eastmoney":
            return EastMoneyFundFlow(symbol)
        raise ValueError(f"Unknown provider: {provider}")
