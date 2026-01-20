"""
Jin10 Client for accessing financial data APIs.
"""

from typing import Any, Dict, List, Optional

import requests
import time


class Jin10Client:
    """
    A client for interacting directly with Jin10's data APIs.
    """

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
                "Referer": "https://datacenter.jin10.com/",
                "Origin": "https://datacenter.jin10.com",
                "x-app-id": "rU6QIu7JHe2gOUeR",
                "x-version": "1.0.0",
            }
        )
        self.base_url = "https://datacenter-api.jin10.com"

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to Jin10 API.
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_margin_data(self, date: str) -> Dict[str, Any]:
        """
        Fetch combined margin data for Shanghai and Shenzhen markets.
        API: https://datacenter-api.jin10.com/reports/list_v2
        """
        ts = int(time.time() * 1000)
        attr_sh = "1"
        attr_sz = "2"
        sh_resp = self._make_request(
            "/reports/list_v2",
            params={"max_date": "", "category": "fs", "attr_id": attr_sh, "_": str(ts)},
        )
        sz_resp = self._make_request(
            "/reports/list_v2",
            params={"max_date": "", "category": "fs", "attr_id": attr_sz, "_": str(ts)},
        )
        sh_data = sh_resp.get("data", {})
        sz_data = sz_resp.get("data", {})
        sh_values = sh_data.get("values", [])
        sz_values = sz_data.get("values", [])
        col_date, col_buy, col_balance = 0, 1, 2
        margin_buy, margin_balance = 0, 0
        for sh_row, sz_row in zip(sh_values, sz_values):
            if sh_row[col_date] != date:
                continue
            margin_buy = (
                float(sh_row[col_buy] + sz_row[col_buy]) / 1e8
            )  # 融资买入额 (元 -> 亿元)
            margin_balance = (
                float(sh_row[col_balance] + sz_row[col_balance]) / 1e8
            )  # 融资余额 (元 -> 亿元)
        return {
            "margin_balance": margin_balance,
            "margin_buy": margin_buy,
        }
