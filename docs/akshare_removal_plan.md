# AkShare依赖移除计划

## 目标

完全移除项目对akshare的依赖，所有接口改为直连API实现

## 当前状态分析

### 现有akshare依赖模块

| 模块       | 文件         | 使用的akshare接口                                                                            |
| ---------- | ------------ | -------------------------------------------------------------------------------------------- |
| historical | eastmoney.py | ak.stock_zh_a_hist()                                                                         |
| historical | sina.py      | ak.stock_zh_a_minute(), ak.stock_zh_a_daily(), ak.stock_zh_b_minute(), ak.stock_zh_b_daily() |
| info       | eastmoney.py | ak.stock_individual_info_em()                                                                |
| realtime   | eastmoney.py | ak.stock_zh_a_spot_em()                                                                      |
| realtime   | xueqiu.py    | ak.stock_zh_a_spot()                                                                         |
| news       | eastmoney.py | ak.stock_news_em()                                                                           |
| insider    | xueqiu.py    | ak.stock_inner_trade_xq()                                                                    |
| financial  | sina.py      | ak.stock_financial_report_sina()                                                             |

### 已实现直连API模块

| 模块       | 文件                | 说明                  |
| ---------- | ------------------- | --------------------- |
| historical | eastmoney_direct.py | ✅ 已实现K线直连      |
| realtime   | eastmoney_direct.py | ✅ 已实现实时行情直连 |
| financial  | eastmoney_direct.py | ✅ 已实现财务数据直连 |

### 新增接口需求

| 接口                            | 功能         | 数据源   | 目标模块 |
| ------------------------------- | ------------ | -------- | -------- |
| stock_cyq_em                    | 筹码分布     | 东方财富 | analysis |
| stock_lhb_stock_detail_em       | 龙虎榜详情   | 东方财富 | market   |
| stock_zygc_em                   | 主营业务构成 | 东方财富 | info     |
| stock_zyjs_ths                  | 主营业务介绍 | 同花顺   | info     |
| tool_trade_date_hist_sina       | 交易日历     | 新浪     | calendar |
| stock_profile_cninfo            | 公司简介     | 巨潮     | info     |
| macro_china_market_margin_sh/sz | 融资融券     | 交易所   | market   |
| stock_zh_a_hist_pre_min_em      | 盘前竞价     | 东方财富 | realtime |
| stock_bid_ask_em                | 内外盘       | 东方财富 | realtime |
| stock_individual_fund_flow      | 资金流向     | 东方财富 | analysis |

## 实施策略

### 阶段1：URL提取（需要完成）

从AkShare源码中提取所有接口的URL和参数：

**现有模块（8个）：**

- [ ] stock_zh_a_hist (eastmoney)
- [ ] stock_zh_a_minute (sina)
- [ ] stock_zh_a_daily (sina)
- [ ] stock_zh_b_minute (sina)
- [ ] stock_zh_b_daily (sina)
- [ ] stock_individual_info_em (eastmoney)
- [ ] stock_zh_a_spot_em (eastmoney)
- [ ] stock_zh_a_spot (xueqiu)
- [ ] stock_news_em (eastmoney)
- [ ] stock_inner_trade_xq (xueqiu)
- [ ] stock_financial_report_sina (sina)

**新增接口（11个）：**

- [ ] stock_cyq_em
- [ ] stock_lhb_stock_detail_em
- [ ] stock_zygc_em
- [ ] stock_zyjs_ths
- [ ] tool_trade_date_hist_sina
- [ ] stock_profile_cninfo
- [ ] macro_china_market_margin_sh
- [ ] macro_china_market_margin_sz
- [ ] stock_zh_a_hist_pre_min_em
- [ ] stock_bid_ask_em
- [ ] stock_individual_fund_flow

### 阶段2：客户端扩展

扩展 [`eastmoney/client.py`](src/akshare_two/eastmoney/client.py:6) 添加新方法

创建新客户端：

- `sina/client.py` - 新浪财经API客户端
- `xueqiu/client.py` - 雪球API客户端
- `ths/client.py` - 同花顺API客户端（如需要）
- `cninfo/client.py` - 巨潮API客户端（如需要）

### 阶段3：重构现有模块

将现有使用akshare的模块改为直连API：

1. historical/eastmoney.py → 使用eastmoney_direct
2. historical/sina.py → 创建sina_direct
3. info/eastmoney.py → 使用eastmoney_direct
4. realtime/eastmoney.py → 使用eastmoney_direct
5. realtime/xueqiu.py → 创建xueqiu_direct
6. news/eastmoney.py → 使用eastmoney_direct
7. insider/xueqiu.py → 使用xueqiu_direct
8. financial/sina.py → 创建sina_direct

### 阶段4：实现新模块

1. 创建market模块（龙虎榜、融资融券）
2. 创建analysis模块（筹码分布、资金流向）
3. 扩展realtime模块（盘前竞价、内外盘）
4. 扩展info模块（主营业务、公司简介）
5. 创建calendar模块（交易日历）

### 阶段5：移除akshare依赖

1. 删除所有使用akshare的旧文件
2. 更新pyproject.toml移除akshare依赖
3. 更新测试用例
4. 更新文档

## URL提取方法

### 方法1：查看AkShare源码

```python
# 查看akshare安装位置
import akshare
print(akshare.__file__)

# 查看具体函数源码
import inspect
print(inspect.getsource(akshare.stock_cyq_em))
```

### 方法2：运行时抓包

使用mitmproxy或浏览器开发者工具抓取实际请求

### 方法3：查看AkShare GitHub

https://github.com/akfamily/akshare

## 下一步行动

1. 安装akshare并提取所有接口的源码
2. 分析URL、参数、响应格式
3. 整理成结构化文档
4. 逐步实现直连API版本
5. 测试验证
6. 移除akshare依赖

## 预期收益

- ✅ 无外部依赖，完全自主可控
- ✅ 性能更好，减少中间层
- ✅ 更容易维护和调试
- ✅ 减小包体积
- ✅ 更快的响应速度
