"""
Jin10 Client for accessing financial data APIs.
"""

from typing import Any, Dict, List, Optional

import requests


class Jin10Client:
    """
    A client for interacting directly with Jin10's data APIs.
    """

    def __init__(self) -> None:
        self.session = requests.Session()
        self.base_url = "https://datacenter.jin10.com"

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to Jin10 API.
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_market_margin_sh(self) -> Dict[str, Any]:
        """
        Fetch Shanghai market margin data (融资融券数据 - 上海).
        Data is usually published around 08:45 on trading days for the previous day.
        """
        return self._make_request(
            "/reportType/dc_market_margin_sse",
            params={"isNew": "1"},
        )

    def fetch_market_margin_sz(self) -> Dict[str, Any]:
        """
        Fetch Shenzhen market margin data (融资融券数据 - 深圳).
        Data is usually published around 08:45 on trading days for the previous day.
        """
        return self._make_request(
            "/reportType/dc_market_margin_sze",
            params={"isNew": "1"},
        )

    def fetch_market_margin(self) -> Dict[str, Any]:
        """
        Fetch combined margin data for both Shanghai and Shenzhen markets.
        """
        sh_data = self.fetch_market_margin_sh()
        sz_data = self.fetch_market_margin_sz()
        return {
            "shanghai": sh_data,
            "shenzhen": sz_data,
        }
