from typing import Any

import pandas as pd


def get_secid(symbol: str) -> str:
    """将股票代码转换为东财secid格式"""
    market = 1 if symbol.startswith("6") else 0
    code = symbol.replace('.SZ', '').replace('.SH', '')
    return f"{market}.{code}"


def parse_kline_data(data: dict[str, Any]) -> pd.DataFrame:
    """解析K线数据"""
    klines = data.get("data", {}).get("klines", [])
    if not klines:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

    records = []
    for kline in klines:
        parts = kline.split(",")
        if len(parts) >= 6:
            records.append({
                "timestamp": parts[0],
                "open": float(parts[1]),
                "close": float(parts[2]),
                "high": float(parts[3]),
                "low": float(parts[4]),
                "volume": int(parts[5]),
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["timestamp"] = df["timestamp"].dt.tz_localize("Asia/Shanghai")
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    return df


def parse_realtime_data(data: dict[str, Any]) -> pd.DataFrame:
    """解析实时行情数据"""
    stock_data = data.get("data")
    if not stock_data:
        return pd.DataFrame()

    df = pd.DataFrame([{
        "symbol": stock_data.get("f57"),
        "price": stock_data.get("f43"),
        "change": stock_data.get("f169"),
        "pct_change": stock_data.get("f170"),
        "volume": stock_data.get("f47"),
        "amount": stock_data.get("f48"),
        "open": stock_data.get("f46"),
        "high": stock_data.get("f44"),
        "low": stock_data.get("f45"),
        "prev_close": stock_data.get("f60"),
    }])
    df["timestamp"] = pd.Timestamp.now(tz="Asia/Shanghai")
    return df


def resample_historical_data(df: pd.DataFrame, interval: str, multiplier: int) -> pd.DataFrame:
    """重采样历史数据"""
    if df.empty or multiplier <= 1:
        return df

    df = df.set_index("timestamp")
    freq_map = {
        "day": f"{multiplier}D",
        "week": f"{multiplier}W-MON",
        "month": f"{multiplier}MS",
        "year": f"{multiplier * 12}MS",
    }
    freq = freq_map.get(interval)
    if not freq:
        return df.reset_index()

    resampled = (
        df.resample(freq)
        .agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        })
        .dropna()
    )
    return resampled.reset_index()


def parse_limit_up_pool(raw_data: dict[str, Any]) -> pd.DataFrame:
    """解析涨停池数据"""
    if raw_data.get("code") != 200:
        return pd.DataFrame()

    result = raw_data.get("result", {})
    data_list = result.get("data", [])
    if not data_list:
        return pd.DataFrame()

    records = []
    for item in data_list:
        records.append({
            "代码": item.get("SECURITY_CODE"),
            "名称": item.get("SECURITY_NAME_ABBR"),
            "涨跌幅": item.get("CHANGE_RATE"),
            "连板数": item.get("CONTINUOUS_BOARD_NUM", 1),
            "换手率": item.get("TURNOVER_RATE"),
            "封板资金": item.get("CLOSE_FUND"),
            "成交额": item.get("DEAL_AMOUNT"),
        })
    return pd.DataFrame(records)


def parse_index_realtime(raw_data: dict[str, Any]) -> pd.DataFrame:
    """解析指数实时数据"""
    if raw_data.get("rc") != 0:
        return pd.DataFrame()

    data = raw_data.get("data", {})
    diff_list = data.get("diff", [])
    if not diff_list:
        return pd.DataFrame()

    records = []
    for item in diff_list:
        records.append({
            "代码": item.get("f12"),
            "名称": item.get("f14"),
            "最新价": item.get("f2"),
            "涨跌幅": item.get("f3"),
            "涨跌额": item.get("f4"),
            "成交量": item.get("f5"),
            "成交额": item.get("f6"),
        })
    return pd.DataFrame(records)


def parse_all_stocks_realtime(raw_data: dict[str, Any]) -> pd.DataFrame:
    """解析所有A股实时数据"""
    if raw_data.get("rc") != 0:
        return pd.DataFrame()

    data = raw_data.get("data", {})
    diff_list = data.get("diff", [])
    if not diff_list:
        return pd.DataFrame()

    records = []
    for item in diff_list:
        records.append({
            "代码": item.get("f12"),
            "名称": item.get("f14"),
            "最新价": item.get("f2"),
            "涨跌幅": item.get("f3"),
            "涨跌额": item.get("f4"),
            "成交量": item.get("f5"),
            "成交额": item.get("f6"),
            "今开": item.get("f17"),
            "最高": item.get("f15"),
            "最低": item.get("f16"),
            "昨收": item.get("f18"),
            "换手率": item.get("f8"),
        })
    return pd.DataFrame(records)
