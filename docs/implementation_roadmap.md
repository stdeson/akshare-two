# 新接口实施路线图

## 项目现状分析

### 现有架构模式

项目采用模块化设计，每个功能模块包含：

- `base.py` - 抽象基类定义接口
- `provider.py` - 具体实现（eastmoney/sina/xueqiu等）
- `factory.py` - 工厂类创建provider实例
- 在 `__init__.py` 中导出统一接口

### 两种实现方式

1. **AkShare封装** - 调用akshare库（如 [`xueqiu.py`](src/akshare_two/modules/insider/xueqiu.py:34)）
2. **直连API** - 直接调用数据源API（如 [`eastmoney_direct.py`](src/akshare_two/modules/financial/eastmoney_direct.py:101)）

## 接口分类与优先级

### 高优先级（核心交易数据）

| 接口                       | 功能       | 数据源   | 建议模块 |
| -------------------------- | ---------- | -------- | -------- |
| stock_lhb_stock_detail_em  | 龙虎榜详情 | 东方财富 | market   |
| stock_individual_fund_flow | 资金流向   | 东方财富 | analysis |
| stock_zh_a_hist_pre_min_em | 盘前竞价   | 东方财富 | realtime |
| stock_bid_ask_em           | 内外盘     | 东方财富 | realtime |

### 中优先级（公司信息）

| 接口                 | 功能         | 数据源   | 建议模块 |
| -------------------- | ------------ | -------- | -------- |
| stock_zygc_em        | 主营业务构成 | 东方财富 | info     |
| stock_cyq_em         | 筹码分布     | 东方财富 | analysis |
| stock_zyjs_ths       | 主营业务介绍 | 同花顺   | info     |
| stock_profile_cninfo | 公司简介     | 巨潮     | info     |

### 低优先级（市场基础）

| 接口                            | 功能     | 数据源 | 建议模块 |
| ------------------------------- | -------- | ------ | -------- |
| macro_china_market_margin_sh/sz | 融资融券 | 交易所 | market   |
| tool_trade_date_hist_sina       | 交易日历 | 新浪   | calendar |

## 实施策略

### 阶段1：URL提取与验证

需要从AkShare源码或通过抓包分析提取每个接口的：

- API URL
- 请求参数
- 响应字段结构
- 字段含义

**参考资源：**

- AkShare文档: https://akshare.akfamily.xyz/data/
- 东方财富API模式参考: [`eastmoney_direct.py`](src/akshare_two/modules/financial/eastmoney_direct.py:101)

### 阶段2：创建新模块

#### 2.1 market模块（市场交易数据）

```
src/akshare_two/modules/market/
├── __init__.py
├── base.py
├── factory.py
└── eastmoney_direct.py
```

**接口设计：**

```python
# 龙虎榜详情
get_lhb_detail(symbol: str, start_date: str, end_date: str) -> pd.DataFrame

# 融资融券
get_margin_trading(market: Literal["sh", "sz"], start_date: str, end_date: str) -> pd.DataFrame
```

#### 2.2 analysis模块（技术分析数据）

```
src/akshare_two/modules/analysis/
├── __init__.py
├── base.py
├── factory.py
└── eastmoney_direct.py
```

**接口设计：**

```python
# 资金流向
get_fund_flow(symbol: str, market: str = "all") -> pd.DataFrame

# 筹码分布
get_chip_distribution(symbol: str, date: str = None) -> pd.DataFrame
```

#### 2.3 扩展realtime模块

在 [`modules/realtime/`](src/akshare_two/modules/realtime/) 中添加：

**接口设计：**

```python
# 盘前竞价数据
get_pre_market_auction(symbol: str, date: str = None) -> pd.DataFrame

# 内外盘数据
get_bid_ask(symbol: str) -> pd.DataFrame
```

#### 2.4 扩展info模块

在 [`modules/info/`](src/akshare_two/modules/info/) 中添加：

**接口设计：**

```python
# 主营业务构成
get_business_composition(symbol: str, date: str = None) -> pd.DataFrame

# 主营业务介绍
get_business_intro(symbol: str) -> pd.DataFrame

# 公司简介
get_company_profile(symbol: str) -> pd.DataFrame
```

### 阶段3：扩展EastMoneyClient

在 [`eastmoney/client.py`](src/akshare_two/eastmoney/client.py:6) 中添加新方法：

```python
def fetch_lhb_detail(self, symbol, start_date, end_date):
    """获取龙虎榜详情"""

def fetch_fund_flow(self, symbol, market):
    """获取资金流向"""

def fetch_pre_market_auction(self, symbol, date):
    """获取盘前竞价数据"""

def fetch_bid_ask(self, symbol):
    """获取内外盘数据"""
```

### 阶段4：数据解析工具

在 [`eastmoney/utils.py`](src/akshare_two/eastmoney/utils.py:6) 中添加解析函数：

```python
def parse_lhb_data(data: dict) -> pd.DataFrame:
    """解析龙虎榜数据"""

def parse_fund_flow_data(data: dict) -> pd.DataFrame:
    """解析资金流向数据"""
```

### 阶段5：统一接口导出

在 [`__init__.py`](src/akshare_two/__init__.py:1) 中添加新接口：

```python
from .modules.market.factory import MarketDataFactory
from .modules.analysis.factory import AnalysisDataFactory

def get_lhb_detail(...) -> pd.DataFrame:
    """获取龙虎榜详情"""

def get_fund_flow(...) -> pd.DataFrame:
    """获取资金流向"""
```

## 关键技术点

### 1. 东方财富API模式

基于 [`eastmoney_direct.py`](src/akshare_two/modules/financial/eastmoney_direct.py:101) 的实现：

```python
api_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
params = {
    "reportName": "RPT_XXX",  # 不同数据类型
    "filter": f'(SECURITY_CODE="{symbol}")',
    "pageNumber": "1",
    "pageSize": "1000",
    "sortColumns": "REPORT_DATE",
    "sortTypes": "-1",
    "columns": "FIELD1,FIELD2,..."
}
```

### 2. 数据标准化

- 统一时间格式为 `Asia/Shanghai` 时区
- 统一字段命名（英文小写+下划线）
- 统一数据类型转换

### 3. 缓存机制

使用 [`cache`](src/akshare_two/modules/cache.py:1) 装饰器提升性能

## 下一步行动

1. **URL提取** - 需要从AkShare源码或抓包分析提取具体的API URL和参数
2. **模块实现** - 按优先级逐步实现各模块
3. **测试验证** - 编写单元测试确保功能正确
4. **文档更新** - 更新API文档和使用示例

## 需要确认的问题

1. 是否优先实现高优先级接口（龙虎榜、资金流向、盘前竞价、内外盘）？
2. 是否需要我提取具体的API URL和参数信息？
3. 模块命名（market、analysis）是否合适？
