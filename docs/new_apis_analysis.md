# 新接口分析与实施方案

## 接口列表与分类

### 1. 公司信息类
| AkShare接口 | 功能 | 数据源 | 优先级 |
|------------|------|--------|--------|
| stock_zygc_em | 主营业务构成 | 东方财富 | 高 |
| stock_zyjs_ths | 主营业务介绍 | 同花顺 | 中 |
| stock_profile_cninfo | 公司简介 | 巨潮资讯 | 中 |

### 2. 市场交易类
| AkShare接口 | 功能 | 数据源 | 优先级 |
|------------|------|--------|--------|
| stock_lhb_stock_detail_em | 龙虎榜详情 | 东方财富 | 高 |
| macro_china_market_margin_sh | 融资融券(沪) | 上交所 | 中 |
| macro_china_market_margin_sz | 融资融券(深) | 深交所 | 中 |

### 3. 实时/盘口数据类
| AkShare接口 | 功能 | 数据源 | 优先级 |
|------------|------|--------|--------|
| stock_zh_a_hist_pre_min_em | 盘前竞价数据 | 东方财富 | 高 |
| stock_bid_ask_em | 内外盘数据 | 东方财富 | 高 |

### 4. 资金/技术分析类
| AkShare接口 | 功能 | 数据源 | 优先级 |
|------------|------|--------|--------|
| stock_individual_fund_flow | 个股资金流向 | 东方财富 | 高 |
| stock_cyq_em | 筹码分布 | 东方财富 | 中 |

### 5. 市场基础类
| AkShare接口 | 功能 | 数据源 | 优先级 |
|------------|------|--------|--------|
| tool_trade_date_hist_sina | 交易日历 | 新浪 | 低 |

### 6. 已实现
| AkShare接口 | 功能 | 状态 |
|------------|------|------|
| stock_zh_a_minute | 分钟K线 | ✅ 已在historical模块实现 |

## 现有架构分析

### 模块结构
```
modules/
├── historical/    # 历史数据
├── realtime/      # 实时数据
├── financial/     # 财务数据
├── info/          # 基础信息
├── news/          # 新闻数据
└── insider/       # 内部交易
```

### 实现模式
1. **base.py** - 定义抽象基类
2. **provider.py** - 实现具体数据提供者（eastmoney/sina/xueqiu等）
3. **factory.py** - 工厂类创建provider实例
4. **__init__.py** - 导出统一接口函数

### 两种实现方式
1. **AkShare封装** - 快速实现，依赖akshare库
2. **直连API** - 性能更好，需要提取URL和参数

## 实施方案

### 方案A：快速实现（推荐优先）
使用akshare封装，快速实现所有接口，后续可逐步优化为直连API

**优点：**
- 实现快速
- 代码简洁
- 维护成本低

**缺点：**
- 依赖akshare库
- 性能略低

### 方案B：完全直连
提取所有接口的URL和参数，实现直连API

**优点：**
- 性能最优
- 无外部依赖

**缺点：**
- 实现复杂
- 需要逆向分析
- 维护成本高

### 推荐方案：混合实现
1. **高优先级接口** - 直连API实现（龙虎榜、资金流向、盘前竞价、内外盘）
2. **中低优先级接口** - akshare封装实现
3. **后续优化** - 根据使用情况逐步优化为直连

## 需要创建的新模块

### 1. market模块（市场交易）
```
modules/market/
├── __init__.py
├── base.py
├── factory.py
├── eastmoney.py      # 龙虎榜（akshare封装）
└── eastmoney_direct.py  # 龙虎榜（直连API）
```

**接口：**
- `get_lhb_detail(symbol, start_date, end_date)` - 龙虎榜详情
- `get_margin_trading(market)` - 融资融券数据

### 2. analysis模块（技术分析）
```
modules/analysis/
├── __init__.py
├── base.py
├── factory.py
├── eastmoney.py      # 资金流向、筹码分布（akshare封装）
└── eastmoney_direct.py  # 资金流向（直连API）
```

**接口：**
- `get_fund_flow(symbol, start_date, end_date)` - 资金流向
- `get_chip_distribution(symbol, date)` - 筹码分布

### 3. 扩展realtime模块
在现有realtime模块中添加：
- `get_pre_market_auction(symbol)` - 盘前竞价数据
- `get_bid_ask(symbol)` - 内外盘数据

### 4. 扩展info模块
在现有info模块中添加：
- `get_business_composition(symbol)` - 主营业务构成
- `get_business_intro(symbol)` - 主营业务介绍
- `get_company_profile(symbol)` - 公司简介

### 5. calendar模块（可选）
```
modules/calendar/
├── __init__.py
├── base.py
├── factory.py
└── sina.py
```

**接口：**
- `get_trade_calendar(start_date, end_date)` - 交易日历

## 下一步行动

### 阶段1：URL提取（需要完成）
从AkShare文档/源码提取以下接口的URL和参数：
- [ ] stock_lhb_stock_detail_em
- [ ] stock_individual_fund_flow
- [ ] stock_zh_a_hist_pre_min_em
- [ ] stock_bid_ask_em
- [ ] stock_cyq_em
- [ ] stock_zygc_em
- [ ] stock_zyjs_ths
- [ ] stock_profile_cninfo
- [ ] macro_china_market_margin_sh/sz
- [ ] tool_trade_date_hist_sina

### 阶段2：模块实现
1. 创建market模块
2. 创建analysis模块
3. 扩展realtime模块
4. 扩展info模块
5. 创建calendar模块（可选）

### 阶段3：测试与文档
1. 编写单元测试
2. 更新API文档
3. 添加使用示例

## 需要确认的问题

1. **实现方式**：优先使用akshare封装还是直连API？
2. **优先级**：先实现哪些接口？
3. **模块命名**：market、analysis等模块名称是否合适？
4. **接口设计**：函数名称和参数设计是否符合预期？
