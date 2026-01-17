# AkShare接口URL提取结果

## 提取方法说明

由于akshare依赖冲突，我将通过以下方式提取URL：

1. 查看AkShare GitHub源码：https://github.com/akfamily/akshare
2. 查看AkShare文档：https://akshare.akfamily.xyz/data/
3. 分析现有项目中的直连API实现模式

## 东方财富API模式（已知）

基于 [`eastmoney_direct.py`](../src/akshare_two/modules/financial/eastmoney_direct.py:101) 的实现：

```python
# 基础URL
base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"

# 通用参数模式
params = {
    "reportName": "RPT_XXX",  # 报表名称，不同接口不同
    "filter": f'(SECURITY_CODE="{symbol}")',  # 过滤条件
    "pageNumber": "1",
    "pageSize": "1000",
    "sortColumns": "REPORT_DATE",
    "sortTypes": "-1",
    "columns": "FIELD1,FIELD2,..."  # 需要的字段
}
```

## 已知的东方财富API端点

### 1. K线数据

```python
url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
params = {
    "secid": "1.600000",  # 市场代码.股票代码
    "fields1": "f1,f2,f3,f4,f5,f6",
    "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
    "klt": "101",  # K线类型：1-1分钟，5-5分钟，101-日线
    "fqt": "1",  # 复权类型：0-不复权，1-前复权，2-后复权
    "beg": "20240101",
    "end": "20241231"
}
```

### 2. 实时行情

```python
url = "https://push2.eastmoney.com/api/qt/stock/get"
params = {
    "secid": "1.600000",
    "invt": "2",
    "fltt": "2",
    "fields": "f43,f57,f58,f169,f170,f46,f60,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530"
}
```

### 3. 财务数据

```python
url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
# 资产负债表
params = {"reportName": "RPT_DMSK_FN_BALANCE", ...}
# 利润表
params = {"reportName": "RPT_DMSK_FN_INCOME", ...}
# 现金流量表
params = {"reportName": "RPT_DMSK_FN_CASHFLOW", ...}
```

## 需要提取的接口URL

### 新增接口（11个）

#### 1. stock_cyq_em - 筹码分布

- **数据源**: 东方财富
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id494
- **参数**: symbol, date
- **说明**: 需要查看akshare源码中的具体实现

#### 2. stock_lhb_stock_detail_em - 龙虎榜详情

- **数据源**: 东方财富
- **URL**: 可能是 `https://datacenter-web.eastmoney.com/api/data/v1/get`
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id127
- **参数**: symbol, start_date, end_date
- **reportName**: 可能是 `RPT_BILLBOARD_XXX`

#### 3. stock_zygc_em - 主营业务构成

- **数据源**: 东方财富
- **URL**: `https://datacenter-web.eastmoney.com/api/data/v1/get`
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id37
- **参数**: symbol, date
- **reportName**: 可能是 `RPT_F10_MAIN_BUSINESS`

#### 4. stock_zyjs_ths - 主营业务介绍

- **数据源**: 同花顺
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id38
- **参数**: symbol

#### 5. tool_trade_date_hist_sina - 交易日历

- **数据源**: 新浪财经
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/tool/tool.html#id2
- **参数**: 无

#### 6. stock_profile_cninfo - 公司简介

- **数据源**: 巨潮资讯
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id36
- **参数**: symbol

#### 7. macro_china_market_margin_sh - 融资融券(沪)

- **数据源**: 上交所
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/macro/macro.html
- **参数**: start_date, end_date

#### 8. macro_china_market_margin_sz - 融资融券(深)

- **数据源**: 深交所
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/macro/macro.html
- **参数**: start_date, end_date

#### 9. stock_zh_a_hist_pre_min_em - 盘前竞价数据

- **数据源**: 东方财富
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id9
- **参数**: symbol, date

#### 10. stock_bid_ask_em - 内外盘

- **数据源**: 东方财富
- **URL**: 待提取
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id10
- **参数**: symbol

#### 11. stock_individual_fund_flow - 资金流向

- **数据源**: 东方财富
- **URL**: `https://datacenter-web.eastmoney.com/api/data/v1/get`
- **参考**: https://akshare.akfamily.xyz/data/stock/stock.html#id123
- **参数**: symbol, market
- **reportName**: 可能是 `RPT_INDIVIDUAL_FUND_FLOW`

### 现有接口需要重构（8个）

#### 12. stock_zh_a_hist - 历史数据(东方财富)

- **当前**: 使用 `ak.stock_zh_a_hist()`
- **目标**: 已有 `eastmoney_direct.py` 实现，可以复用

#### 13. stock_zh_a_minute - 分钟数据(新浪)

- **当前**: 使用 `ak.stock_zh_a_minute()`
- **URL**: 待提取
- **数据源**: 新浪财经

#### 14. stock_zh_a_daily - 日线数据(新浪)

- **当前**: 使用 `ak.stock_zh_a_daily()`
- **URL**: 待提取
- **数据源**: 新浪财经

#### 15. stock_individual_info_em - 个股信息

- **当前**: 使用 `ak.stock_individual_info_em()`
- **URL**: `https://datacenter-web.eastmoney.com/api/data/v1/get`
- **reportName**: 待确认

#### 16. stock_zh_a_spot_em - 实时行情(东方财富)

- **当前**: 使用 `ak.stock_zh_a_spot_em()`
- **目标**: 已有 `eastmoney_direct.py` 实现，可以复用

#### 17. stock_zh_a_spot - 实时行情(雪球)

- **当前**: 使用 `ak.stock_zh_a_spot()`
- **URL**: 待提取
- **数据源**: 雪球

#### 18. stock_news_em - 个股新闻

- **当前**: 使用 `ak.stock_news_em()`
- **URL**: 待提取
- **数据源**: 东方财富

#### 19. stock_inner_trade_xq - 内部交易

- **当前**: 使用 `ak.stock_inner_trade_xq()`
- **URL**: 待提取
- **数据源**: 雪球

## 下一步行动

1. 从AkShare GitHub仓库查看源码
2. 逐个提取URL和参数
3. 验证API可用性
4. 实现直连版本
