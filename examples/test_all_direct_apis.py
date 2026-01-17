"""测试所有直连API实现"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from akshare_two.modules.historical.factory import HistoricalDataFactory
from akshare_two.modules.realtime.factory import RealtimeDataFactory
from akshare_two.modules.info.factory import InfoDataFactory
from akshare_two.modules.news.factory import NewsDataFactory
from akshare_two.modules.insider.factory import InsiderDataFactory
from akshare_two.modules.financial.factory import FinancialDataFactory
from akshare_two.modules.analysis.factory import FundFlowFactory
from akshare_two.modules.market.factory import BillboardFactory


def test_eastmoney_direct_historical():
    """测试东方财富历史数据"""
    print("\n=== 测试东方财富历史数据 ===")
    try:
        provider = HistoricalDataFactory.get_provider("eastmoney_direct", symbol="600519")
        df = provider.get_hist_data()
        print(f"✓ 获取历史数据成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_sina_direct_historical():
    """测试新浪历史数据"""
    print("\n=== 测试新浪历史数据 ===")
    try:
        provider = HistoricalDataFactory.get_provider("sina_direct", symbol="sh600519")
        df = provider.get_hist_data()
        print(f"✓ 获取历史数据成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_eastmoney_direct_realtime():
    """测试东方财富实时数据"""
    print("\n=== 测试东方财富实时数据 ===")
    try:
        provider = RealtimeDataFactory.get_provider("eastmoney_direct", symbol="600519")
        df = provider.get_current_data()
        print(f"✓ 获取实时数据成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_xueqiu_direct_realtime():
    """测试雪球实时数据"""
    print("\n=== 测试雪球实时数据 ===")
    try:
        provider = RealtimeDataFactory.get_provider("xueqiu_direct", symbol="600519")
        df = provider.get_current_data()
        print(f"✓ 获取实时数据成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_eastmoney_direct_info():
    """测试东方财富个股信息"""
    print("\n=== 测试东方财富个股信息 ===")
    try:
        provider = InfoDataFactory.get_provider("eastmoney_direct", symbol="600519")
        df = provider.get_basic_info()
        print(f"✓ 获取个股信息成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_eastmoney_direct_news():
    """测试东方财富新闻"""
    print("\n=== 测试东方财富新闻 ===")
    try:
        provider = InfoDataFactory.get_provider("eastmoney_direct", symbol="600519")
        df = provider.get_stock_news(page_size=10)
        print(f"✓ 获取新闻成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_xueqiu_direct_insider():
    """测试雪球内部交易"""
    print("\n=== 测试雪球内部交易 ===")
    try:
        provider = InsiderDataFactory.get_provider("xueqiu_direct", symbol="600519")
        df = provider.get_inner_trade_data()
        print(f"✓ 获取内部交易成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_eastmoney_direct_financial():
    """测试东方财富财务数据"""
    print("\n=== 测试东方财富财务数据 ===")
    try:
        provider = FinancialDataFactory.get_provider("eastmoney_direct", symbol="600519")
        df = provider.get_balance_sheet()
        print(f"✓ 获取财务数据成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_fund_flow():
    """测试资金流向"""
    print("\n=== 测试资金流向 ===")
    try:
        provider = FundFlowFactory.get_provider("eastmoney", symbol="600519")
        df = provider.get_fund_flow(period="daily")
        print(f"✓ 获取资金流向成功: {len(df)} 条记录")
        print(df.head(2))
    except Exception as e:
        print(f"✗ 失败: {e}")


def test_billboard():
    """测试龙虎榜"""
    print("\n=== 测试龙虎榜 ===")
    try:
        provider = BillboardFactory.get_provider("eastmoney", symbol="600519")
        df = provider.get_billboard_detail("2024-01-01", "2024-12-31")
        print(f"✓ 获取龙虎榜成功: {len(df)} 条记录")
        if len(df) > 0:
            print(df.head(2))
        else:
            print("(该股票在指定时间段内无龙虎榜数据)")
    except Exception as e:
        print(f"✗ 失败: {e}")


if __name__ == "__main__":
    print("开始测试所有直连API实现...")
    
    test_eastmoney_direct_historical()
    test_sina_direct_historical()
    test_eastmoney_direct_realtime()
    test_xueqiu_direct_realtime()
    test_eastmoney_direct_info()
    test_eastmoney_direct_news()
    test_xueqiu_direct_insider()
    test_eastmoney_direct_financial()
    test_fund_flow()
    test_billboard()
    
    print("\n测试完成！")
