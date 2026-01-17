from typing import Any

import requests


class EastMoneyClient:
    """
    A client for interacting directly with EastMoney's data APIs.
    This class handles session management, request signing, and API calls.
    """

    def __init__(self) -> None:
        self.session = requests.Session()

    def _get_security_id(self, symbol: str) -> str:
        """
        Converts a stock symbol to EastMoney's internal secid format.
        e.g., '600519' -> '1.600519', '000001' -> '0.000001'
        """
        symbol = symbol.upper()
        if symbol.startswith("SZ"):
            market = "0"
            code = symbol[2:]
        elif symbol.startswith("SH"):
            market = "1"
            code = symbol[2:]
        elif symbol.startswith("HK"):
            market = "116"
            code = symbol[2:]
        elif len(symbol) == 6:
            if symbol.startswith(("000", "001", "002", "003", "300", "200")):
                market = "0"
            elif symbol.startswith(
                ("600", "601", "603", "605", "688", "900", "5", "6")
            ):
                market = "1"
            else:
                market = "0"  # Default to SZ for ambiguity
            code = symbol
        elif len(symbol) == 5:  # HK Market
            market = "116"
            code = symbol
        else:
            market = "0"
            code = symbol
        return f"{market}.{code}"

    def fetch_historical_klines(
        self, symbol: str, klt: str, fqt: str, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """
        Fetches historical K-line (candlestick) data.
        """
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        secid = self._get_security_id(symbol)
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": klt,
            "fqt": fqt,
            "secid": secid,
            "beg": start_date,
            "end": end_date,
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_realtime_quote(self, symbol: str) -> dict[str, Any]:
        """
        Fetches real-time quote data for a single stock.
        """
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        secid = self._get_security_id(symbol)
        params = {
            "invt": "2",
            "fltt": "2",
            "fields": (
                "f43,f57,f58,f169,f170,f46,f60,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530"
            ),
            "secid": secid,
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_fund_flow(self, symbol: str, klt: str = "101") -> dict[str, Any]:
        """
        Fetches individual stock fund flow data.
        klt: 101=daily, 102=weekly, 103=monthly
        """
        url = "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get"
        secid = self._get_security_id(symbol)
        params = {
            "lmt": "0",
            "klt": klt,
            "secid": secid,
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_billboard_detail(
        self, symbol: str, start_date: str = "", end_date: str = ""
    ) -> dict[str, Any]:
        """
        Fetches billboard (龙虎榜) detail data.
        """
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        filter_str = f'(SECURITY_CODE="{symbol}")'
        if start_date:
            filter_str += f'(TRADE_DATE>=\'{start_date}\')'
        if end_date:
            filter_str += f'(TRADE_DATE<=\'{end_date}\')'
        params = {
            "reportName": "RPT_BILLBOARD_DAILYDETAILSBUY",
            "filter": filter_str,
            "pageNumber": "1",
            "pageSize": "500",
            "sortColumns": "BUY",
            "sortTypes": "-1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_bid_ask_details(self, symbol: str) -> dict[str, Any]:
        """
        Fetches bid/ask transaction details (内外盘).
        """
        url = "https://push2.eastmoney.com/api/qt/stock/details/get"
        secid = self._get_security_id(symbol)
        params = {
            "secid": secid,
            "fields1": "f1,f2,f3,f4",
            "fields2": "f51,f52,f53,f54,f55",
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_auction_data(self, symbol: str) -> dict[str, Any]:
        """
        Fetches pre-market auction data (盘前竞价).
        """
        url = "https://push2.eastmoney.com/api/qt/stock/auction/get"
        secid = self._get_security_id(symbol)
        params = {
            "secid": secid,
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_main_business(self, symbol: str) -> dict[str, Any]:
        """
        Fetches main business composition (主营业务构成).
        """
        # 判断市场代码
        if symbol.startswith(("6", "5")):
            code = f"SH{symbol}"
        else:
            code = f"SZ{symbol}"
        
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/PageAjax"
        params = {"code": code}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore

    def fetch_stock_news(
        self, symbol: str, page_size: int = 100, page_index: int = 1
    ) -> dict[str, Any]:
        """
        Fetches stock news (个股新闻).
        """
        url = "https://np-listapi.eastmoney.com/comm/wap/getListInfo"
        params = {
            "client": "wap",
            "type": "1",
            "mTypeAndCode": f"0_{symbol}",
            "pageSize": str(page_size),
            "pageIndex": str(page_index),
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()  # type: ignore
