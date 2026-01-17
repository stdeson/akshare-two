# API直连实现方案

## 目标
为以下接口提取数据源URL和参数，并实现直连API版本：

| 接口名称 | 功能描述 | 数据源 |
|---------|---------|--------|
| stock_cyq_em | 筹码分布 | 东方财富 |
| stock_lhb_stock_detail_em | 龙虎榜详情 | 东方财富 |
| stock_zygc_em | 主营业务构成 | 东方财富 |
| stock_zyjs_ths | 主营业务介绍 | 同花顺 |
| tool_trade_date_hist_sina | 交易日历 | 新浪 |
| stock_profile_cninfo | 公司简介 | 巨潮 |
| macro_china_market_margin_sh/sz | 融资融券 | 交易所 |
| stock_zh_a_hist_pre_min_em | 盘前竞价数据 | 东方财富 |
| stock_bid_ask_em | 内外盘 | 东方财富 |
| stock_individual_fund_flow | 资金流向 | 东方财富 |

## 现有直连API实现参考

### EastMoneyClient 结构
```python
class EastMoneyClient:
    def fetch_historical_klines(self, symbol, klt, fqt, start_date, end_date):
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {...}
        
    def fetch_realtime_quote(self, symbol):
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        params = {...}
```

### 实现模式
1. 在 `eastmoney/client.py` 中添加新的fetch方法
2. 在 `eastmoney/utils.py` 中添加数据解析函数
3. 创建新模块目录（如 `modules/market/`）
4. 实现 base.py（抽象基类）
5. 实现 provider（如 `eastmoney_direct.py`）
6. 实现 factory.py（工厂类）
7. 在 `__init__.py` 中添加统一接口

## 需要提取的信息

对每个接口需要提取：
1. **API URL** - 完整的请求地址
2. **请求方法** - GET/POST
3. **请求参数** - 参数名称、类型、是否必填
4. **响应格式** - JSON结构
5. **字段映射** - 原始字段到标准字段的映射

## 实施步骤

### 步骤1：URL提取
从AkShare源码或文档中提取每个接口的：
- 请求URL
- 请求参数
- 响应字段

### 步骤2：模块设计
根据功能分类创建模块：
- `modules/market/` - 龙虎榜、融资融券
- `modules/analysis/` - 筹码分布、资金流向
- `modules/calendar/` - 交易日历
- 扩展 `modules/info/` - 主营业务、公司简介
- 扩展 `modules/realtime/` - 盘前竞价、内外盘

### 步骤3：客户端扩展
在 `eastmoney/client.py` 中添加新方法：
- `fetch_chip_distribution()` - 筹码分布
- `fetch_lhb_detail()` - 龙虎榜详情
- `fetch_business_composition()` - 主营业务构成
- `fetch_pre_market_auction()` - 盘前竞价
- `fetch_bid_ask()` - 内外盘
- `fetch_fund_flow()` - 资金流向

### 步骤4：数据解析
在 `eastmoney/utils.py` 中添加解析函数：
- `parse_chip_distribution_data()`
- `parse_lhb_detail_data()`
- 等等...

### 步骤5：模块实现
按照现有模式实现各模块

### 步骤6：统一接口
在 `__init__.py` 中添加：
- `get_chip_distribution()`
- `get_lhb_detail()`
- `get_business_composition()`
- 等等...

## 下一步行动

需要从AkShare文档/源码中提取每个接口的具体实现细节。

参考文档：https://akshare.akfamily.xyz/data/

建议方式：
1. 逐个查看AkShare文档中这些接口的说明
2. 提取URL、参数、响应格式
3. 整理成结构化信息
4. 开始实现
