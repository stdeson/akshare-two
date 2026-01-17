# AkShare接口URL详细信息

## 东方财富API通用模式

### 数据中心API
```python
base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
params = {
    "reportName": "RPT_XXX",  # 报表名称
    "filter": f'(SECURITY_CODE="{symbol}")',
    "pageNumber": "1",
    "pageSize": "1000",
    "sortColumns": "REPORT_DATE",
    "sortTypes": "-1",
    "columns": "ALL"
}
```

### 行情API
```python
# K线数据
url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"

# 实时行情
url = "https://push2.eastmoney.com/api/qt/stock/get"
```

## 新增接口URL（11个）

### 1. stock_individual_fund_flow - 资金流向
```python
url = "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get"
params = {
    "lmt": "0",
    "klt": "101",  # 日线
    "secid": f"{market}.{symbol}",  # 如 "1.600000"
    "fields1": "f1,f2,f3,f7",
    "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
}
```

### 2. stock_lhb_stock_detail_em - 龙虎榜详情
```python
url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
params = {
    "reportName": "RPT_BILLBOARD_STOCK_DETAIL",
    "filter": f'(SECURITY_CODE="{symbol}")(TRADE_DATE>=\'{start_date}\')',
    "pageNumber": "1",
    "pageSize": "500",
    "sortColumns": "TRADE_DATE",
    "sortTypes": "-1",
    "columns": "ALL"
}
```

### 3. stock_bid_ask_em - 内外盘
```python
url = "https://push2.eastmoney.com/api/qt/stock/details/get"
params = {
    "secid": f"{market}.{symbol}",
    "fields1": "f1,f2,f3,f4",
    "fields2": "f51,f52,f53,f54,f55"
}
```

### 4. stock_zh_a_hist_pre_min_em - 盘前竞价数据
```python
url = "https://push2.eastmoney.com/api/qt/stock/auction/get"
params = {
    "secid": f"{market}.{symbol}",
    "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13"
}
```

### 5. stock_cyq_em - 筹码分布
```python
url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
params = {
    "reportName": "RPT_LICO_FU_STKCOST",
    "filter": f'(SECURITY_CODE="{symbol}")',
    "pageNumber": "1",
    "pageSize": "1",
    "sortColumns": "TRADE_DATE",
    "sortTypes": "-1",
    "columns": "ALL"
}
```

### 6. stock_zygc_em - 主营业务构成
```python
url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
params = {
    "reportName": "RPT_F10_MAIN_BUSINESS",
    "filter": f'(SECURITY_CODE="{symbol}")',
    "pageNumber": "1",
    "pageSize": "500",
    "sortColumns": "REPORT_DATE",
    "sortTypes": "-1",
    "columns": "ALL"
}
```

### 7. stock_individual_info_em - 个股信息
```python
url = "https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/Index"
params = {
    "code": f"{market}{symbol}"  # 如 "SH600000"
}
# 返回HTML，需要解析
```

### 8. stock_news_em - 个股新闻
```python
url = "https://np-listapi.eastmoney.com/comm/wap/getListInfo"
params = {
    "cb": "callback",
    "client": "wap",
    "type": "1",
    "mTypeAndCode": f"0_{symbol}",
    "pageSize": "100",
    "pageIndex": "1",
    "callback": "jQuery"
}
```

### 9. stock_zyjs_ths - 主营业务介绍（同花顺）
```python
url = "http://basic.10jqka.com.cn/api/stock/export.php"
params = {
    "export": "main",
    "type": "last",
    "code": symbol
}
```

### 10. stock_profile_cninfo - 公司简介（巨潮）
```python
url = "http://webapi.cninfo.com.cn/api/stock/p_stock2303"
params = {
    "scode": symbol
}
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0"
}
```

### 11. macro_china_market_margin_sh/sz - 融资融券
```python
# 上交所
url = "http://query.sse.com.cn/marketdata/tradedata/queryMargin.do"
params = {
    "jsonCallBack": "jsonpCallback",
    "isPagination": "true",
    "beginDate": start_date,
    "endDate": end_date,
    "pageHelp.pageSize": "1000",
    "pageHelp.pageNo": "1",
    "pageHelp.beginPage": "1",
    "pageHelp.cacheSize": "1",
    "pageHelp.endPage": "1"
}

# 深交所
url = "http://www.szse.cn/api/report/ShowReport/data"
params = {
    "SHOWTYPE": "JSON",
    "CATALOGID": "1837_xxpl",
    "TABKEY": "tab1",
    "txtBeginDate": start_date,
    "txtEndDate": end_date,
    "radioClass": "00"
}
```

## 现有接口需要重构（8个）

### 12. stock_zh_a_minute - 分钟数据（新浪）
```python
url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
params = {
    "symbol": f"{market}{symbol}",  # 如 "sh600000"
    "scale": "1",  # 1分钟
    "ma": "no",
    "datalen": "1023"
}
```

### 13. stock_zh_a_daily - 日线数据（新浪）
```python
url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
params = {
    "symbol": f"{market}{symbol}",
    "scale": "240",  # 日线
    "ma": "no",
    "datalen": "1023"
}
```

### 14. stock_zh_a_spot - 实时行情（雪球）
```python
url = "https://stock.xueqiu.com/v5/stock/quote.json"
params = {
    "symbol": f"{market}{symbol}",  # 如 "SH600000"
    "extend": "detail"
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://xueqiu.com/"
}
```

### 15. stock_inner_trade_xq - 内部交易（雪球）
```python
url = "https://stock.xueqiu.com/v5/stock/f10/cn/skholderchg.json"
params = {
    "symbol": f"{market}{symbol}",
    "count": "100"
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://xueqiu.com/"
}
```

### 16. stock_financial_report_sina - 财务数据（新浪）
```python
# 资产负债表
url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{symbol}/ctrl/all/displaytype/4.phtml"

# 利润表
url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{symbol}/ctrl/all/displaytype/4.phtml"

# 现金流量表
url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{symbol}/ctrl/all/displaytype/4.phtml"
```

### 17-19. 已有直连实现
- stock_zh_a_hist - 已在 eastmoney_direct.py 实现
- stock_zh_a_spot_em - 已在 eastmoney_direct.py 实现
- stock_financial (eastmoney) - 已在 eastmoney_direct.py 实现

## 实施优先级

### 高优先级（东方财富API，模式统一）
1. stock_individual_fund_flow - 资金流向
2. stock_lhb_stock_detail_em - 龙虎榜详情
3. stock_bid_ask_em - 内外盘
4. stock_zh_a_hist_pre_min_em - 盘前竞价
5. stock_zygc_em - 主营业务构成
6. stock_news_em - 个股新闻

### 中优先级（需要特殊处理）
7. stock_cyq_em - 筹码分布
8. stock_individual_info_em - 个股信息（HTML解析）

### 低优先级（其他数据源）
9. stock_zyjs_ths - 同花顺
10. stock_profile_cninfo - 巨潮
11. macro_china_market_margin_sh/sz - 交易所
12. stock_zh_a_minute/daily - 新浪
13. stock_zh_a_spot - 雪球
14. stock_inner_trade_xq - 雪球
15. stock_financial_report_sina - 新浪

## 下一步行动

1. 先实现高优先级的东方财富API接口（模式统一，容易实现）
2. 扩展 EastMoneyClient 添加新方法
3. 创建新模块（market、analysis）
4. 逐步替换现有的akshare依赖
