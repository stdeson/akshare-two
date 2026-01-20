"""A股数据接口 - 简化版"""

from typing import Any, Literal

import pandas as pd
import requests

from .utils import (
    get_secid,
    parse_kline_data,
    parse_realtime_data,
    parse_limit_up_pool,
    parse_index_realtime,
    parse_all_stocks_realtime,
    resample_historical_data,
)

_session = requests.Session()


def _get(url: str, **kwargs) -> dict:
    """统一请求方法"""
    r = _session.get(url, timeout=30, **kwargs)
    return r.json()


def get_auction_data(symbol: str) -> dict | None:
    """获取盘前竞价数据"""
    secid = get_secid(symbol)
    url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
    params = {
        "secid": secid,
        "fields1": "f1,f2,f3,f4,f5",
        "fields2": "f51,f56,f57",
        "ndays": "1",
        "iscr": "1",
        "iscca": "0",
    }
    data = _get(url, params=params)
    trends = (data.get("data") or {}).get("trends") or []
    for s in trends:
        parts = s.split(",")
        if parts[0].endswith("09:26"):
            return {"time": parts[0], "price": float(parts[1]), "volume": int(float(parts[2]))}
    return None


def get_realtime_quote(symbol: str) -> pd.DataFrame:
    """获取个股实时行情"""
    secid = get_secid(symbol)
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "invt": "2",
        "fltt": "2",
        "fields": "f43,f57,f58,f169,f170,f46,f60,f44,f47,f48,f45",
        "secid": secid,
    }
    raw = _get(url, params=params)
    return parse_realtime_data(raw)


def get_hist_data(
    symbol: str,
    interval: Literal["minute", "hour", "day", "week", "month", "year"] = "day",
    interval_multiplier: int = 1,
    start_date: str = "19700101",
    end_date: str = "20301231",
    adjust: Literal["none", "qfq", "hfq"] = "none",
) -> pd.DataFrame:
    """获取历史K线数据"""
    secid = get_secid(symbol)

    klt_map = {"minute": "1", "hour": "60", "day": "101", "week": "102", "month": "103", "year": "104"}
    fqt_map = {"none": "0", "qfq": "1", "hfq": "2"}

    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": klt_map.get(interval, "101"),
        "fqt": fqt_map.get(adjust, "0"),
        "secid": secid,
        "beg": start_date,
        "end": end_date,
    }

    raw = _get(url, params=params)
    df = parse_kline_data(raw)
    return resample_historical_data(df, interval, interval_multiplier)


def get_fund_flow(symbol: str, klt: str = "101") -> pd.DataFrame:
    """获取资金流向"""
    secid = get_secid(symbol)
    url = "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get"
    params = {
        "lmt": "0",
        "klt": klt,
        "secid": secid,
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
    }
    raw = _get(url, params=params)
    klines = raw.get("data", {}).get("klines", [])
    if not klines:
        return pd.DataFrame()

    records = []
    for kline in klines:
        parts = kline.split(",")
        records.append({
            "timestamp": parts[0],
            "net_inflow": float(parts[2]),
            "net_inflow_main": float(parts[3]),
        })
    return pd.DataFrame(records)


def get_billboard_detail(symbol: str, start_date: str = "", end_date: str = "") -> dict:
    """获取龙虎榜详情"""
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
    return _get(url, params=params)


def get_bid_ask_details(symbol: str) -> pd.DataFrame:
    """获取内外盘明细"""
    secid = get_secid(symbol)
    url = "https://push2.eastmoney.com/api/qt/stock/details/get"
    params = {
        "secid": secid,
        "fields1": "f1,f2,f3,f4",
        "fields2": "f51,f52,f53,f54,f55",
    }
    raw = _get(url, params=params)
    details = (raw.get("data") or {}).get("details") or []
    if not details:
        return pd.DataFrame()

    lines = details.split(";") if isinstance(details, str) else details
    records = []
    for line in lines:
        if line:
            parts = line.split(",")
            if len(parts) >= 4:
                records.append({
                    "time": parts[0],
                    "price": float(parts[1]),
                    "volume": int(parts[2]),
                    "direction": "买" if int(parts[3]) == 1 else "卖",
                })
    return pd.DataFrame(records)


def get_stock_info(symbol: str) -> dict:
    """获取股票基础信息"""
    secid = get_secid(symbol)
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "invt": "2",
        "fltt": "2",
        "fields": "f57,f58,f43,f44,f45,f46,f47,f48,f169,f170",
        "secid": secid,
    }
    return _get(url, params=params)


def get_main_business(symbol: str) -> dict:
    """获取主营业务"""
    code = f"SH{symbol}" if symbol.startswith(("6", "5")) else f"SZ{symbol}"
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/PageAjax"
    params = {"code": code}
    return _get(url, params=params)


def get_stock_news(symbol: str, page_size: int = 100, page_index: int = 1) -> dict:
    """获取个股新闻"""
    url = "https://np-listapi.eastmoney.com/comm/wap/getListInfo"
    params = {
        "client": "wap",
        "type": "1",
        "mTypeAndCode": f"0_{symbol}",
        "pageSize": str(page_size),
        "pageIndex": str(page_index),
    }
    return _get(url, params=params)


def get_all_stocks_realtime() -> pd.DataFrame:
    """获取所有A股实时行情"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    all_diff = []
    page_size = 100
    pn = 1

    while True:
        params = {
            "pn": str(pn),
            "pz": page_size,
            "po": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        }
        raw = _get(url, params=params)
        if raw.get("rc") != 0:
            break
        diff = raw.get("data", {}).get("diff", [])
        if not diff:
            break
        all_diff.extend(diff)
        total = raw.get("data", {}).get("total", 0)
        if len(all_diff) >= total:
            break
        pn += 1
        if pn > 100:
            break

    return parse_all_stocks_realtime({"data": {"diff": all_diff}})


def stock_zt_pool_em(date: str) -> pd.DataFrame:
    """获取涨停池数据"""
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_BILLBOARD_DAILYDETAILSBUY",
        "filter": f"(TRADE_DATE='{date}')",
        "pageNumber": "1",
        "pageSize": "5000",
        "sortColumns": "CHANGE_RATE",
        "sortTypes": "-1",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
    }
    raw = _get(url, params=params)
    return parse_limit_up_pool(raw)


def stock_zh_index_spot_em() -> pd.DataFrame:
    """获取指数实时行情"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "1000",
        "po": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:1+s:2,m:0+t:5",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    raw = _get(url, params=params)
    return parse_index_realtime(raw)


# 兼容旧API名称
get_realtime_data = get_realtime_quote
