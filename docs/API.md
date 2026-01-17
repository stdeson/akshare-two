# AKShare Two API 文档

## 历史数据 (Historical Data)

### `get_hist_data(symbol, interval="1d", adjust="", source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://push2his.eastmoney.com/api/qt/stock/kline/get`
- `sina_direct` → 新浪财经 `https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData`

## 实时数据 (Realtime Data)

### `get_current_data(symbol, source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://push2.eastmoney.com/api/qt/stock/get`
- `xueqiu_direct` → 雪球 `https://stock.xueqiu.com/v5/stock/quote.json` (需要认证)

### `get_bid_ask_details(symbol, source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://push2.eastmoney.com/api/qt/stock/details/get`

## 财务数据 (Financial Data)

### `get_balance_sheet(symbol, source="eastmoney_direct")`
### `get_income_statement(symbol, source="eastmoney_direct")`
### `get_cash_flow(symbol, source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://datacenter-web.eastmoney.com/api/data/v1/get`

## 资金流向 (Fund Flow)

### `get_fund_flow(symbol, period="daily", source="eastmoney")`

**数据源路由：**
- `eastmoney` → 东方财富 `https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get`

## 龙虎榜 (Billboard)

### `get_billboard_detail(symbol, start_date, end_date, source="eastmoney")`

**数据源路由：**
- `eastmoney` → 东方财富 `https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_BILLBOARD_DAILYDETAILSBUY`

## 个股信息 (Stock Info)

### `get_basic_info(symbol, source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://push2.eastmoney.com/api/qt/stock/get`

### `get_main_business(symbol, source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/PageAjax`

### `get_stock_news(symbol, page_size=100, source="eastmoney_direct")`

**数据源路由：**
- `eastmoney_direct` → 东方财富 `https://np-listapi.eastmoney.com/comm/wap/getListInfo`

## 内部交易 (Insider Trading)

### `get_inner_trade_data(symbol, source="xueqiu_direct")`

**数据源路由：**
- `xueqiu_direct` → 雪球 `https://stock.xueqiu.com/v5/stock/f10/cn/skholderchg.json` (需要认证)

## 使用示例

```python
from akshare_two import get_hist_data, get_current_data, get_fund_flow

# 获取历史数据
df = get_hist_data(symbol="600519", interval="1d", source="eastmoney_direct")

# 获取实时数据
df = get_current_data(symbol="600519", source="eastmoney_direct")

# 获取资金流向
df = get_fund_flow(symbol="600519", period="daily", source="eastmoney")
```

## 注意事项

1. 所有接口均为直连官方 API，不依赖 akshare 库
2. 雪球 API 需要 cookie 认证才能正常使用
3. 股票代码格式：6 位数字（如 "600519"），系统会自动添加市场前缀
