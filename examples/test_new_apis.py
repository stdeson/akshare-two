"""测试新实现的6个API接口（不依赖akshare）"""

from akshare_two.modules.analysis.eastmoney import EastMoneyFundFlow
from akshare_two.modules.market.eastmoney import EastMoneyBillboard
from akshare_two.modules.realtime.eastmoney_direct import EastMoneyDirectRealtime
from akshare_two.modules.info.eastmoney_direct import EastMoneyDirectInfo


def test_fund_flow():
    """测试资金流向"""
    print("\n=== 测试资金流向 ===")
    try:
        provider = EastMoneyFundFlow(symbol="600519")
        df = provider.get_fund_flow(period="daily")
        print(f"获取到 {len(df)} 条资金流向数据")
        if not df.empty:
            print(df.head())
    except Exception as e:
        print(f"资金流向测试失败: {e}")


def test_billboard_detail():
    """测试龙虎榜详情"""
    print("\n=== 测试龙虎榜详情 ===")
    try:
        provider = EastMoneyBillboard(symbol="600519")
        df = provider.get_billboard_detail("2024-01-01", "2024-12-31")
        print(f"获取到 {len(df)} 条龙虎榜数据")
        if not df.empty:
            print(df.head())
    except Exception as e:
        print(f"龙虎榜测试失败: {e}")


def test_bid_ask():
    """测试内外盘"""
    print("\n=== 测试内外盘 ===")
    try:
        provider = EastMoneyDirectRealtime(symbol="600519")
        df = provider.get_bid_ask_details()
        print(f"获取到 {len(df)} 条内外盘数据")
        if not df.empty:
            print(df.head())
    except Exception as e:
        print(f"内外盘测试失败: {e}")


def test_pre_market():
    """测试盘前竞价"""
    print("\n=== 测试盘前竞价 ===")
    try:
        provider = EastMoneyDirectRealtime(symbol="600519")
        df = provider.get_auction_data()
        print(f"获取到 {len(df)} 条盘前竞价数据")
        if not df.empty:
            print(df.head())
    except Exception as e:
        print(f"盘前竞价测试失败: {e}")


def test_business_composition():
    """测试主营业务构成"""
    print("\n=== 测试主营业务构成 ===")
    try:
        provider = EastMoneyDirectInfo(symbol="600519")
        df = provider.get_main_business()
        print(f"获取到 {len(df)} 条主营业务数据")
        if not df.empty:
            print(df.head())
    except Exception as e:
        print(f"主营业务构成测试失败: {e}")


def test_stock_news():
    """测试个股新闻"""
    print("\n=== 测试个股新闻 ===")
    try:
        provider = EastMoneyDirectInfo(symbol="600519")
        df = provider.get_stock_news(page_size=10)
        print(f"获取到 {len(df)} 条新闻数据")
        if not df.empty:
            print(df.head())
    except Exception as e:
        print(f"个股新闻测试失败: {e}")


if __name__ == "__main__":
    print("开始测试新实现的API接口...")
    test_fund_flow()
    test_billboard_detail()
    test_bid_ask()
    test_pre_market()
    test_business_composition()
    test_stock_news()
    print("\n测试完成！")
