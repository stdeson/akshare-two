"""
Jin10 implementation for market data.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from akshare_two.jin10.client import Jin10Client

from ..cache import cache


class Jin10:
    """
    Jin10 implementation for margin data (融资融券数据).
    """

    def __init__(self) -> None:
        self.client = Jin10Client()

    @cache("margin_cache", key=lambda self, date: f"margin_{date}")
    def get_margin_data(self, date: str) -> Dict[str, Any]:
        """
        获取指定日期的融资融券数据.

        Args:
            date: 日期 (YYYY-MM-DD format)

        Returns:
            Dict containing:
                - date: 日期
                - margin_balance: 融资余额 (亿元)
                - margin_buy: 融资买入额 (亿元)
                - margin_pure: 融资净买 (亿元)
                - sh_balance: 上海融资余额 (亿元)
                - sz_balance: 深圳融资余额 (亿元)
        """
        try:
            # 获取上海和深圳的融资数据
            sh_raw = self.client.fetch_market_margin_sh()
            sz_raw = self.client.fetch_market_margin_sz()

            # 解析数据
            sh_data = self._parse_margin_data(sh_raw, date)
            sz_data = self._parse_margin_data(sz_raw, date)

            if not sh_data or not sz_data:
                return {}

            # 计算合计值
            margin_balance = sh_data["balance"] + sz_data["balance"]
            margin_buy = sh_data["buy"] + sz_data["buy"]

            # 计算融资净买
            margin_pure = None
            if (
                sh_data.get("prev_balance") is not None
                and sz_data.get("prev_balance") is not None
            ):
                margin_pure = margin_balance - (
                    sh_data["prev_balance"] + sz_data["prev_balance"]
                )

            return {
                "date": date,
                "margin_balance": round(margin_balance, 2),
                "margin_buy": round(margin_buy, 2),
                "margin_pure": (
                    round(margin_pure, 2) if margin_pure is not None else None
                ),
                "sh_balance": round(sh_data["balance"], 2),
                "sz_balance": round(sz_data["balance"], 2),
            }

        except Exception as e:
            raise ValueError(f"Failed to get margin data: {e}") from e

    def _parse_margin_data(
        self, raw_data: Dict[str, Any], target_date: str
    ) -> Optional[Dict[str, float]]:
        """
        解析原始 margin 数据.

        Args:
            raw_data: 原始 API 响应数据
            target_date: 目标日期 (YYYY-MM-DD)

        Returns:
            Dict with balance, buy, and prev_balance values, or None if not found
        """
        try:
            # Jin10 API 返回的数据格式需要根据实际响应调整
            # 这里假设返回的数据在 data 字段中
            data_list = raw_data.get("data", [])

            if not data_list:
                return None

            # 将目标日期转换为 Jin10 格式 (YYYY-MM-DD -> YYYY-mm-dd)
            target_dt = datetime.strptime(target_date, "%Y-%m-%d")

            # 查找目标日期的数据
            target_data = None
            prev_data = None

            for i, item in enumerate(data_list):
                # Jin10 日期格式可能是 "2024-01-18" 或其他格式
                item_date_str = item.get("date", "")
                try:
                    # 尝试解析日期
                    if isinstance(item_date_str, str) and len(item_date_str) == 10:
                        item_dt = datetime.strptime(item_date_str, "%Y-%m-%d")
                    elif isinstance(item_date_str, str) and len(item_date_str) == 8:
                        item_dt = datetime.strptime(item_date_str, "%Y%m%d")
                    else:
                        continue

                    if item_dt.date() == target_dt.date():
                        target_data = item
                        # 获取前一天数据
                        if i > 0:
                            prev_data = (
                                data_list[i + 1] if i + 1 < len(data_list) else None
                            )
                        break
                except ValueError:
                    continue

            if target_data is None:
                return None

            # 提取数据 - 字段名需要根据实际 API 响应调整
            # 常见的字段名可能是: balance, buy, date 等
            balance = float(target_data.get("balance", 0) or 0)
            buy = float(target_data.get("buy", 0) or 0)

            prev_balance = None
            if prev_data:
                prev_balance = float(prev_data.get("balance", 0) or 0)

            return {
                "balance": balance / 1e8,  # 转换为亿元
                "buy": buy / 1e8,  # 转换为亿元
                "prev_balance": prev_balance / 1e8 if prev_balance else None,
            }

        except Exception:
            return None

    def get_margin_history(self, days: int = 30) -> pd.DataFrame:
        """
        获取最近 N 天的融资融券数据.

        Args:
            days: 天数

        Returns:
            pd.DataFrame with margin history data
        """
        try:
            raw_data = self.client.fetch_market_margin_sh()
            data_list = raw_data.get("data", [])

            if not data_list:
                return pd.DataFrame()

            records = []
            for item in data_list[:days]:
                date_str = item.get("date", "")
                try:
                    if isinstance(date_str, str) and len(date_str) == 10:
                        date = datetime.strptime(date_str, "%Y-%m-%d").strftime(
                            "%Y-%m-%d"
                        )
                    elif isinstance(date_str, str) and len(date_str) == 8:
                        date = datetime.strptime(date_str, "%Y%m%d").strftime(
                            "%Y-%m-%d"
                        )
                    else:
                        continue

                    balance = float(item.get("balance", 0) or 0) / 1e8
                    buy = float(item.get("buy", 0) or 0) / 1e8

                    records.append(
                        {
                            "date": date,
                            "margin_balance": balance,
                            "margin_buy": buy,
                        }
                    )
                except (ValueError, TypeError):
                    continue

            return pd.DataFrame(records)

        except Exception as e:
            raise ValueError(f"Failed to get margin history: {e}") from e
