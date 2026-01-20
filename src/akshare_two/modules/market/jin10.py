"""
Jin10 implementation for market data.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from logftz import logger

import pandas as pd

from akshare_two.jin10.client import Jin10Client


class Jin10:
    """
    Jin10 implementation for margin data (融资融券数据).
    """

    def __init__(self) -> None:
        self.client = Jin10Client()

    def get_margin_data(self, date: str) -> Dict[str, Any]:
        """
        获取指定日期的融资融券数据.

        Args:
            date: 日期 (YYYY-MM-DD format)

        Returns:
            Dict containing:
                - margin_balance: 融资余额 (亿元)
                - margin_buy: 融资买入额 (亿元)
        """
        return self.client.get_margin_data(date)
