# AkShare依赖完全移除实施计划

## 目标
将项目中所有使用akshare的模块改为直连官方API（东方财富、新浪、雪球等）

## 当前状态

### 已完成直连实现的模块
- ✅ [`historical/eastmoney_direct.py`](../src/akshare_one/modules/historical/eastmoney_direct.py) - 东方财富历史数据
- ✅ [`realtime/eastmoney_direct.py`](../src/akshare_one/modules/realtime/eastmoney_direct.py) - 东方财富实时数据
- ✅ [`financial/eastmoney_direct.py`](../src/akshare_one/modules/financial/eastmoney_direct.py) - 东方财富财务数据
- ✅ [`info/eastmoney_direct.py`](../src/akshare_one/modules/info/eastmoney_direct.py) - 东方财富信息数据
- ✅ [`analysis/eastmoney.py`](../src/akshare_one/modules/analysis/eastmoney.py) - 资金流向
- ✅ [`market/eastmoney.py`](../src/akshare_one/modules/market/eastmoney.py) - 龙虎榜

### 需要移除akshare的模块（8个）

#### 1. [`historical/eastmoney.py`](../src/akshare_one/modules/historical/eastmoney.py)
**当前使用的akshare接口**:
- `ak.stock_zh_a_hist_min_em()` - 分钟K线
- `ak.stock_zh_a_hist()` - 日线数据
- `ak.fund_etf_hist_sina()` - ETF数据

**替换方案**: 
- 使用[`EastMoneyClient.fetch_historical_klines()`](../src/akshare_one/eastmoney/client.py:48)
- 已有直连实现: [`EastMoneyDirectHistorical`](../src/akshare_one/modules/historical/eastmoney_direct.py)

**操作**: 删除此文件，使用eastmoney_direct.py替代

---

#### 2. [`historical/sina.py`](../src/akshare_one/modules/historical/sina.py)
**当前使用的akshare接口**:
- `ak.stock_zh_a_minute()` - A股分钟数据
- `ak.stock_zh_b_minute()` - B股分钟数据
- `ak.stock_zh_a_daily()` - A股日线数据
- `ak.stock_zh_b_daily()` - B股日线数据

**替换方案**: 创建SinaClient直连实现
- API端点: `https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData`
- 参数: symbol, scale (1=1分钟, 240=日线), ma, datalen

**操作**: 创建sina/client.py和sina直连实现

---

#### 3. [`realtime/eastmoney.py`](../src/akshare_one/modules/realtime/eastmoney.py)
**当前使用的akshare接口**:
- `ak.stock_zh_a_spot_em()` - 沪深京A股实时行情

**替换方案**:
- 使用[`EastMoneyClient.fetch_realtime_quote()`](../src/akshare_one/eastmoney/client.py:69)
- 已有直连实现: [`EastMoneyDirectRealtime`](../src/akshare_one/modules/realtime/eastmoney_direct.py)

**操作**: 删除此文件，使用eastmoney_direct.py替代

---

#### 4. [`realtime/xueqiu.py`](../src/akshare_one/modules/realtime/xueqiu.py)
**当前使用的akshare接口**:
- `ak.stock_individual_spot_xq()` - 雪球实时行情

**替换方案**: 创建XueqiuClient直连实现
- API端点: `https://stock.xueqiu.com/v5/stock/quote.json`
- 参数: symbol (如"SH600000"), extend="detail"
- Headers: User-Agent, Referer

**操作**: 创建xueqiu/client.py和xueqiu直连实现

---

#### 5. [`info/eastmoney.py`](../src/akshare_one/modules/info/eastmoney.py)
**当前使用的akshare接口**:
- `ak.stock_individual_info_em()` - 东方财富个股信息

**替换方案**:
- API端点: `https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/Index`
- 参数: code (如"SH600000")
- 已有部分实现在[`EastMoneyDirectInfo`](../src/akshare_one/modules/info/eastmoney_direct.py)

**操作**: 在EastMoneyClient中添加fetch_stock_info方法，删除info/eastmoney.py

---

#### 6. [`news/eastmoney.py`](../src/akshare_one/modules/news/eastmoney.py)
**当前使用的akshare接口**:
- `ak.stock_news_em()` - 东方财富个股新闻

**替换方案**:
- 已在[`EastMoneyClient.fetch_stock_news()`](../src/akshare_one/eastmoney/client.py:177)实现
- 需要调试API参数以获取正确数据

**操作**: 修复stock_news API，删除news/eastmoney.py

---

#### 7. [`insider/xueqiu.py`](../src/akshare_one/modules/insider/xueqiu.py)
**当前使用的akshare接口**:
- `ak.stock_inner_trade_xq()` - 雪球内部交易数据

**替换方案**: 创建XueqiuClient直连实现
- API端点: `https://stock.xueqiu.com/v5/stock/f10/cn/skholderchg.json`
- 参数: symbol (如"SH600000"), count=100
- Headers: User-Agent, Referer

**操作**: 创建xueqiu/client.py和xueqiu直连实现

---

#### 8. [`financial/sina.py`](../src/akshare_one/modules/financial/sina.py)
**当前使用的akshare接口**:
- `ak.stock_financial_report_sina()` - 新浪财务报表

**替换方案**: 创建SinaClient直连实现
- API端点: 
  * 资产负债表: `https://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{symbol}/ctrl/all/displaytype/4.phtml`
  * 利润表: `https://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{symbol}/ctrl/all/displaytype/4.phtml`
  * 现金流量表: `https://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{symbol}/ctrl/all/displaytype/4.phtml`
- 需要HTML解析

**操作**: 创建sina/client.py和sina直连实现

---

## 实施步骤

### 阶段1: 创建新的客户端类（优先级：高）

1. **创建SinaClient** (`src/akshare_one/sina/client.py`)
   - fetch_minute_data() - 分钟K线
   - fetch_daily_data() - 日线数据
   - fetch_financial_report() - 财务报表（需要HTML解析）

2. **创建XueqiuClient** (`src/akshare_one/xueqiu/client.py`)
   - fetch_realtime_quote() - 实时行情
   - fetch_insider_trades() - 内部交易

3. **扩展EastMoneyClient** (`src/akshare_one/eastmoney/client.py`)
   - fetch_stock_info() - 个股信息
   - 修复fetch_stock_news() - 个股新闻

### 阶段2: 更新模块实现（优先级：高）

1. **删除使用akshare的模块**:
   - 删除 `historical/eastmoney.py`
   - 删除 `realtime/eastmoney.py`
   - 删除 `info/eastmoney.py`
   - 删除 `news/eastmoney.py`

2. **创建新的直连实现**:
   - 创建 `historical/sina_direct.py` - 使用SinaClient
   - 创建 `realtime/xueqiu_direct.py` - 使用XueqiuClient
   - 创建 `insider/xueqiu_direct.py` - 使用XueqiuClient
   - 创建 `financial/sina_direct.py` - 使用SinaClient

### 阶段3: 更新工厂类和导出（优先级：中）

1. **更新Factory类**:
   - `historical/factory.py` - 移除"eastmoney"，保留"eastmoney_direct"，添加"sina_direct"
   - `realtime/factory.py` - 移除"eastmoney"和"xueqiu"，添加"eastmoney_direct"和"xueqiu_direct"
   - `info/factory.py` - 移除"eastmoney"，保留"eastmoney_direct"
   - `news/factory.py` - 更新为使用直连实现
   - `insider/factory.py` - 移除"xueqiu"，添加"xueqiu_direct"
   - `financial/factory.py` - 移除"sina"，添加"sina_direct"

2. **更新__init__.py**:
   - 移除所有akshare相关的导入
   - 更新默认provider为直连实现

### 阶段4: 移除依赖和清理（优先级：高）

1. **更新pyproject.toml**:
   - 移除 `akshare>=1.17.80` 依赖
   - 添加必要的直连依赖: `requests>=2.31.0`, `pandas>=2.0.0`, `beautifulsoup4>=4.12.0` (用于HTML解析)

2. **更新文档**:
   - 更新README.md说明不再依赖akshare
   - 更新示例代码使用新的provider名称

3. **测试验证**:
   - 运行所有测试确保功能正常
   - 验证所有API接口可用

---

## API端点汇总

### 东方财富 (EastMoney)
- 历史K线: `https://push2his.eastmoney.com/api/qt/stock/kline/get`
- 实时行情: `https://push2.eastmoney.com/api/qt/stock/get`
- 资金流向: `https://push2.eastmoney.com/api/qt/stock/fflow/kline/get`
- 龙虎榜: `https://datacenter-web.eastmoney.com/api/data/v1/get`
- 内外盘: `https://push2.eastmoney.com/api/qt/stock/details/get`
- 主营业务: `https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/PageAjax`
- 个股信息: `https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/Index`
- 财务数据: `https://datacenter-web.eastmoney.com/api/data/v1/get`

### 新浪 (Sina)
- K线数据: `https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData`
- 财务报表: `https://money.finance.sina.com.cn/corp/go.php/vFD_*/stockid/{symbol}/ctrl/all/displaytype/4.phtml`

### 雪球 (Xueqiu)
- 实时行情: `https://stock.xueqiu.com/v5/stock/quote.json`
- 内部交易: `https://stock.xueqiu.com/v5/stock/f10/cn/skholderchg.json`

---

## 预期收益

1. **性能提升**: 直连API减少中间层，提高响应速度
2. **依赖简化**: 移除akshare及其所有依赖包
3. **可维护性**: 完全掌控API调用逻辑，便于调试和优化
4. **稳定性**: 不受akshare版本更新影响
5. **灵活性**: 可以根据需求自定义API参数和数据处理

---

## 风险和注意事项

1. **API变更**: 官方API可能随时变更，需要持续维护
2. **反爬虫**: 某些API可能有访问频率限制，需要添加重试和限流机制
3. **数据格式**: 直连API返回的数据格式可能与akshare不同，需要仔细测试
4. **认证要求**: 某些API（如雪球）可能需要特殊的Headers或Cookie
5. **HTML解析**: 新浪财务报表返回HTML，需要使用BeautifulSoup解析

---

## 下一步行动

1. 创建SinaClient和XueqiuClient
2. 扩展EastMoneyClient添加缺失的方法
3. 创建所有直连实现模块
4. 更新工厂类和导出
5. 移除akshare依赖
6. 全面测试验证
