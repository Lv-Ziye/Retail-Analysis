# 零售企业经营数据分析项目

用 SQL + Python 分析零售订单数据，回答经营问题，产出商业建议。

---

## 文件结构

```
零售经营分析项目/
├── README.md                 ← 项目说明
├── 分析报告.md                ← 完整分析报告（结论 + 建议）
├── data.py                      ← 数据
├── setup_db.py               ← 导入 SQLite（本地跑 SQL 用）
├── mysql_setup.sql           ← MySQL 建库建表
├── queries.sql               ← SQL 分析脚本（SQLite 版）
├── queries_mysql.sql         ← SQL 分析脚本（MySQL 版）
├── rfm_analysis.py           ← Python RFM 分层 + 画图
├── RFM客户分层结果.xlsx       ← RFM 分层结果
├── 图1~图4_*.png             ← 报告图表
└── data/
    ├── superstore.csv        ← 原始数据（9005 行 × 21 列）
    └── superstore_mysql.csv  ← MySQL 导入用
```

## 数据字典（orders 表 21 个字段）

| 字段 | 含义 | 字段 | 含义 |
|------|------|------|------|
| Row_ID | 行号 | Region | 大区（West/East/Central/South） |
| Order_ID | 订单号 | Product_ID | 商品编号 |
| Order_Date | 下单日期 | Category | 品类（3类） |
| Ship_Date | 发货日期 | Sub_Category | 子品类（17类） |
| Ship_Mode | 发货方式 | Product_Name | 商品名 |
| Customer_ID | 客户编号 | Sales | 销售额（元） |
| Customer_Name | 客户姓名 | Quantity | 数量 |
| Segment | 客户类型（3类） | Discount | 折扣（0~0.8） |
| Country | 国家 | Profit | 利润（元） |
| City / State / Postal_Code | 城市/州/邮编 | | |

## 要回答的业务问题

1. **整体经营健康度**：销售额/利润/利润率的时间趋势
2. **利润黑洞在哪**：哪些品类/子品类/地区在亏损？
3. **折扣侵蚀利润**：折扣力度和利润的关系
4. **客户分层**：RFM 找出高价值客户和流失风险客户
5. **增长机会**：哪个细分市场值得投入？
