# AkShare接口URL提取清单

## 需要提取的接口信息

### 1. stock_cyq_em - 筹码分布
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id494
- **数据源**: 东方财富
- **URL**: 待提取
- **参数**: symbol (股票代码), date (日期)
- **返回字段**: 待提取

### 2. stock_lhb_stock_detail_em - 龙虎榜详情
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id127
- **数据源**: 东方财富
- **URL**: 待提取
- **参数**: symbol (股票代码), start_date, end_date
- **返回字段**: 待提取

### 3. stock_zygc_em - 主营业务构成
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id37
- **数据源**: 东方财富
- **URL**: 待提取
- **参数**: symbol (股票代码), date (报告期)
- **返回字段**: 待提取

### 4. stock_zyjs_ths - 主营业务介绍
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id38
- **数据源**: 同花顺
- **URL**: 待提取
- **参数**: symbol (股票代码)
- **返回字段**: 待提取

### 5. tool_trade_date_hist_sina - 交易日历
- **AkShare文档**: https://akshare.akfamily.xyz/data/tool/tool.html#id2
- **数据源**: 新浪财经
- **URL**: 待提取
- **参数**: 无
- **返回字段**: 待提取

### 6. stock_profile_cninfo - 公司简介
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id36
- **数据源**: 巨潮资讯
- **URL**: 待提取
- **参数**: symbol (股票代码)
- **返回字段**: 待提取

### 7. macro_china_market_margin_sh - 融资融券(沪)
- **AkShare文档**: https://akshare.akfamily.xyz/data/macro/macro.html
- **数据源**: 上交所
- **URL**: 待提取
- **参数**: start_date, end_date
- **返回字段**: 待提取

### 8. macro_china_market_margin_sz - 融资融券(深)
- **AkShare文档**: https://akshare.akfamily.xyz/data/macro/macro.html
- **数据源**: 深交所
- **URL**: 待提取
- **参数**: start_date, end_date
- **返回字段**: 待提取

### 9. stock_zh_a_hist_pre_min_em - 盘前竞价数据
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id9
- **数据源**: 东方财富
- **URL**: 待提取
- **参数**: symbol (股票代码), date (日期)
- **返回字段**: 待提取

### 10. stock_bid_ask_em - 内外盘
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id10
- **数据源**: 东方财富
- **URL**: 待提取
- **参数**: symbol (股票代码)
- **返回字段**: 待提取

### 11. stock_individual_fund_flow - 资金流向
- **AkShare文档**: https://akshare.akfamily.xyz/data/stock/stock.html#id123
- **数据源**: 东方财富
- **URL**: 待提取
- **参数**: symbol (股票代码), market (市场)
- **返回字段**: 待提取

## 提取方法

### 方法1：查看AkShare源码
```bash
# 安装akshare
pip install akshare

# 查看源码位置
python -c "import akshare; print(akshare.__file__)"

# 查看具体函数实现
python -c "import inspect; import akshare as ak; print(inspect.getsource(ak.stock_cyq_em))"
```

### 方法2：抓包分析
使用浏览器开发者工具访问东方财富等网站，抓取实际的API请求

### 方法3：查看AkShare文档
访问 https://akshare.akfamily.xyz/data/ 查看每个接口的详细说明

## 下一步行动

1. 逐个提取每个接口的URL和参数
2. 分析响应数据结构
3. 设计统一的数据格式
4. 实现直连API版本
