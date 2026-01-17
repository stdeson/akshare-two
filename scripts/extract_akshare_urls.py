"""
从AkShare GitHub仓库提取接口URL的脚本

使用方法：
1. 访问 https://github.com/akfamily/akshare
2. 搜索对应的函数名
3. 查看源码中的URL
"""

# 需要提取的接口列表
interfaces = {
    # 新增接口
    "stock_cyq_em": {
        "desc": "筹码分布",
        "source": "东方财富",
        "github_path": "akshare/stock_feature/stock_cyq_em.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id494"
    },
    "stock_lhb_stock_detail_em": {
        "desc": "龙虎榜详情",
        "source": "东方财富",
        "github_path": "akshare/stock_feature/stock_lhb_em.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id127"
    },
    "stock_zygc_em": {
        "desc": "主营业务构成",
        "source": "东方财富",
        "github_path": "akshare/stock_fundamental/stock_zygc_em.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id37"
    },
    "stock_zyjs_ths": {
        "desc": "主营业务介绍",
        "source": "同花顺",
        "github_path": "akshare/stock_fundamental/stock_zyjs_ths.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id38"
    },
    "tool_trade_date_hist_sina": {
        "desc": "交易日历",
        "source": "新浪",
        "github_path": "akshare/tool/tool_trade_date.py",
        "doc_url": "https://akshare.akfamily.xyz/data/tool/tool.html#id2"
    },
    "stock_profile_cninfo": {
        "desc": "公司简介",
        "source": "巨潮",
        "github_path": "akshare/stock_fundamental/stock_profile_cninfo.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id36"
    },
    "macro_china_market_margin_sh": {
        "desc": "融资融券(沪)",
        "source": "上交所",
        "github_path": "akshare/stock_feature/stock_margin.py",
        "doc_url": "https://akshare.akfamily.xyz/data/macro/macro.html"
    },
    "macro_china_market_margin_sz": {
        "desc": "融资融券(深)",
        "source": "深交所",
        "github_path": "akshare/stock_feature/stock_margin.py",
        "doc_url": "https://akshare.akfamily.xyz/data/macro/macro.html"
    },
    "stock_zh_a_hist_pre_min_em": {
        "desc": "盘前竞价数据",
        "source": "东方财富",
        "github_path": "akshare/stock/stock_zh_a_hist_pre_min_em.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id9"
    },
    "stock_bid_ask_em": {
        "desc": "内外盘",
        "source": "东方财富",
        "github_path": "akshare/stock/stock_bid_ask_em.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id10"
    },
    "stock_individual_fund_flow": {
        "desc": "资金流向",
        "source": "东方财富",
        "github_path": "akshare/stock_feature/stock_fund_flow_em.py",
        "doc_url": "https://akshare.akfamily.xyz/data/stock/stock.html#id123"
    },
    
    # 现有需要重构的接口
    "stock_zh_a_hist": {
        "desc": "历史数据(东方财富)",
        "source": "东方财富",
        "github_path": "akshare/stock/stock_zh_a_hist.py",
        "status": "已有direct实现"
    },
    "stock_zh_a_minute": {
        "desc": "分钟数据(新浪)",
        "source": "新浪",
        "github_path": "akshare/stock/stock_zh_a_minute.py"
    },
    "stock_zh_a_daily": {
        "desc": "日线数据(新浪)",
        "source": "新浪",
        "github_path": "akshare/stock/stock_zh_a_daily.py"
    },
    "stock_individual_info_em": {
        "desc": "个股信息",
        "source": "东方财富",
        "github_path": "akshare/stock_fundamental/stock_individual_info_em.py"
    },
    "stock_zh_a_spot_em": {
        "desc": "实时行情(东方财富)",
        "source": "东方财富",
        "github_path": "akshare/stock/stock_zh_a_spot_em.py",
        "status": "已有direct实现"
    },
    "stock_zh_a_spot": {
        "desc": "实时行情(雪球)",
        "source": "雪球",
        "github_path": "akshare/stock/stock_zh_a_spot.py"
    },
    "stock_news_em": {
        "desc": "个股新闻",
        "source": "东方财富",
        "github_path": "akshare/stock_feature/stock_news_em.py"
    },
    "stock_inner_trade_xq": {
        "desc": "内部交易",
        "source": "雪球",
        "github_path": "akshare/stock_feature/stock_inner_trade_xq.py"
    },
    "stock_financial_report_sina": {
        "desc": "财务数据(新浪)",
        "source": "新浪",
        "github_path": "akshare/stock_fundamental/stock_financial_sina.py"
    }
}

def print_extraction_guide():
    """打印提取指南"""
    print("=" * 80)
    print("AkShare接口URL提取指南")
    print("=" * 80)
    print()
    
    for func_name, info in interfaces.items():
        print(f"\n## {func_name} - {info['desc']}")
        print(f"数据源: {info['source']}")
        print(f"GitHub: https://github.com/akfamily/akshare/blob/master/{info['github_path']}")
        if 'doc_url' in info:
            print(f"文档: {info['doc_url']}")
        if 'status' in info:
            print(f"状态: {info['status']}")
        print()
        print("需要提取:")
        print("  - API URL")
        print("  - 请求参数")
        print("  - 响应字段")
        print("-" * 80)

if __name__ == "__main__":
    print_extraction_guide()
