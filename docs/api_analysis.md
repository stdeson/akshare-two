# AkShare接口分析与实施方案

## 待实现接口列表

| 接口名称                        | 功能描述     | 功能分类 | 数据源   |
| ------------------------------- | ------------ | -------- | -------- |
| stock_cyq_em                    | 筹码分布     | 技术分析 | 东方财富 |
| stock_lhb_stock_detail_em       | 龙虎榜详情   | 市场交易 | 东方财富 |
| stock_zygc_em                   | 主营业务构成 | 公司信息 | 东方财富 |
| stock_zyjs_ths                  | 主营业务介绍 | 公司信息 | 同花顺   |
| tool_trade_date_hist_sina       | 交易日历     | 市场基础 | 新浪     |
| stock_profile_cninfo            | 公司简介     | 公司信息 | 巨潮     |
| macro_china_market_margin_sh/sz | 融资融券     | 市场交易 | 交易所   |
| stock_zh_a_minute               | 分钟K线      | 历史数据 | 已实现   |
| stock_zh_a_hist_pre_min_em      | 盘前竞价数据 | 实时数据 | 东方财富 |
| stock_bid_ask_em                | 内外盘       | 实时数据 | 东方财富 |
| stock_individual_fund_flow      | 资金流向     | 资金分析 | 东方财富 |

## 功能模块分类

### 1. 公司信息模块 (info)

- stock_zygc_em - 主营业务构成
- stock_zyjs_ths - 主营业务介绍
- stock_profile_cninfo - 公司简介

### 2. 市场交易模块 (market)

- stock_lhb_stock_detail_em - 龙虎榜详情
- macro_china_market_margin_sh/sz - 融资融券

### 3. 实时数据模块 (realtime)

- stock_zh_a_hist_pre_min_em - 盘前竞价数据
- stock_bid_ask_em - 内外盘

### 4. 技术分析模块 (analysis)

- stock_cyq_em - 筹码分布
- stock_individual_fund_flow - 资金流向

### 5. 市场基础模块 (calendar)

- tool_trade_date_hist_sina - 交易日历

## 现有项目架构分析

### 架构模式

```
modules/
├── base.py          # 抽象基类
├── factory.py       # 工厂类
├── eastmoney.py     # 东方财富实现（调用akshare）
└── eastmoney_direct.py  # 东方财富直连实现
```

### 实现特点

1. 使用抽象基类定义接口
2. 工厂模式创建数据提供者
3. 缓存装饰器提升性能
4. 统一的数据格式输出
5. 支持多数据源切换

## 实施方案

### 阶段1：扩展公司信息模块

在 `src/akshare_two/modules/info/` 中添加：

- 主营业务构成接口
- 主营业务介绍接口
- 公司简介接口

### 阶段2：创建市场交易模块

创建 `src/akshare_two/modules/market/` 包含：

- 龙虎榜详情接口
- 融资融券接口

### 阶段3：扩展实时数据模块

在 `src/akshare_two/modules/realtime/` 中添加：

- 盘前竞价数据接口
- 内外盘数据接口

### 阶段4：创建技术分析模块

创建 `src/akshare_two/modules/analysis/` 包含：

- 筹码分布接口
- 资金流向接口

### 阶段5：创建市场基础模块

创建 `src/akshare_two/modules/calendar/` 包含：

- 交易日历接口

## 下一步行动

1. 查找每个接口在AkShare中的具体实现
2. 提取数据源URL和请求参数
3. 设计统一的API接口
4. 实现各模块的代码
5. 编写测试用例
6. 更新文档

## 需要确认的信息

1. 是否需要实现所有接口，还是优先实现部分？
2. 是否需要直连实现，还是先用akshare封装？
3. 数据格式是否需要特殊处理？
