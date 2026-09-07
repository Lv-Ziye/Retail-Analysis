# -*- coding: utf-8 -*-
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)   # 固定随机种子，保证每次生成结果一致（可复现）

N = 9000  # 约 9000 条订单明细（真实 Superstore 约 9994 条）

# 品类 / 子品类
CATEGORY_SUB = {
    'Furniture':       ['Bookcases', 'Chairs', 'Furnishings', 'Tables'],
    'Office Supplies': ['Appliances', 'Art', 'Binders', 'Envelopes',
                        'Fasteners', 'Labels', 'Paper', 'Storage', 'Supplies'],
    'Technology':      ['Accessories', 'Copiers', 'Machines', 'Phones'],
}
SUB_CATEGORY = {s: c for c, subs in CATEGORY_SUB.items() for s in subs}

# 子品类 -> 典型单价(元)
UNIT_PRICE = {
    'Bookcases': 160, 'Chairs': 320, 'Furnishings': 120, 'Tables': 500,
    'Appliances': 260, 'Art': 18, 'Binders': 15, 'Envelopes': 12,
    'Fasteners': 6, 'Labels': 9, 'Paper': 14, 'Storage': 45, 'Supplies': 22,
    'Accessories': 90, 'Copiers': 2600, 'Machines': 1200, 'Phones': 350,
}
# 子品类 -> 基础毛利率（未折扣时）
MARGIN = {
    'Bookcases': 0.22, 'Chairs': 0.18, 'Furnishings': 0.15, 'Tables': 0.12,
    'Appliances': 0.20, 'Art': 0.25, 'Binders': 0.28, 'Envelopes': 0.30,
    'Fasteners': 0.32, 'Labels': 0.30, 'Paper': 0.28, 'Storage': 0.26, 'Supplies': 0.25,
    'Accessories': 0.20, 'Copiers': 0.24, 'Machines': 0.22, 'Phones': 0.18,
}

# 地区 / 州 / 城市
REGION_STATE = {
    'West':    ['California', 'Washington', 'Oregon', 'Arizona', 'Colorado'],
    'East':    ['New York', 'Pennsylvania', 'New Jersey', 'Massachusetts'],
    'Central': ['Illinois', 'Texas', 'Ohio', 'Michigan', 'Wisconsin'],
    'South':   ['Florida', 'Georgia', 'North Carolina', 'Tennessee'],
}
CITY_BY_STATE = {
    'California': ['Los Angeles', 'San Francisco', 'San Diego'],
    'Washington': ['Seattle', 'Spokane'], 'Oregon': ['Portland'],
    'Arizona': ['Phoenix'], 'Colorado': ['Denver'],
    'New York': ['New York City', 'Buffalo'], 'Pennsylvania': ['Philadelphia'],
    'New Jersey': ['Newark'], 'Massachusetts': ['Boston'],
    'Illinois': ['Chicago'], 'Texas': ['Houston', 'Dallas', 'Austin'],
    'Ohio': ['Columbus'], 'Michigan': ['Detroit'], 'Wisconsin': ['Milwaukee'],
    'Florida': ['Miami', 'Orlando'], 'Georgia': ['Atlanta'],
    'North Carolina': ['Charlotte'], 'Tennessee': ['Nashville'],
}

FIRST = ['Alex', 'Emma', 'Noah', 'Olivia', 'Liam', 'Sophia', 'Mason', 'Ava',
         'Ethan', 'Isabella', 'Lucas', 'Mia', 'Henry', 'Grace', 'Daniel', 'Zoe',
         'David', 'Lily', 'James', 'Ella', 'Ryan', 'Chloe', 'Kevin', 'Nora']
LAST = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
        'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Lee',
        'Harris', 'Clark', 'Lewis', 'Walker', 'Hall', 'Young', 'King', 'Wright']

SEGMENTS = ['Consumer', 'Corporate', 'Home Office']
SEGMENT_P = [0.52, 0.30, 0.18]
SHIP_MODES = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
SHIP_P = [0.60, 0.20, 0.14, 0.06]
DISCOUNTS = [0.0, 0.1, 0.2, 0.3, 0.45, 0.5, 0.6, 0.7, 0.8]

# 生成基础字段
n_customers = 700
customer_ids = [f"{rng.choice(list('ABCDEFGH'))}{rng.choice(list('ABCDEFGH'))}-{10000 + i}"
                for i in range(n_customers)]
customer_names = [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(n_customers)]

subs = list(SUB_CATEGORY.keys())
sub_idx = rng.choice(len(subs), size=N)               # 每个订单的子品类
sub = [subs[i] for i in sub_idx]
cat = [SUB_CATEGORY[s] for s in sub]

region = rng.choice(list(REGION_STATE.keys()), size=N, p=[0.30, 0.30, 0.22, 0.18])
state = [rng.choice(REGION_STATE[r]) for r in region]
city = [rng.choice(CITY_BY_STATE[s]) for s in state]

seg_idx = rng.choice(3, size=N, p=SEGMENT_P)
segment = [SEGMENTS[i] for i in seg_idx]
ship = rng.choice(SHIP_MODES, size=N, p=SHIP_P)

cust_idx = rng.integers(0, n_customers, size=N)
customer_id = [customer_ids[i] for i in cust_idx]
customer_name = [customer_names[i] for i in cust_idx]

# 日期（2022~2024，Q4 旺季 + 逐年增长）
month_weights = np.array([0.9, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.15, 1.2, 1.5, 1.6])
month = rng.choice(np.arange(1, 13), size=N, p=month_weights / month_weights.sum())
year = rng.choice([2022, 2023, 2024], size=N, p=[0.30, 0.33, 0.37])
day = rng.integers(1, 29, size=N)  # 简化：每月 1~28 日
order_date = pd.Series([pd.Timestamp(int(y), int(m), int(d)) for y, m, d in zip(year, month, day)])

# 发货延迟：Same Day 0天，First 1-2天，Second 2-4天，Standard 3-7天
delay = np.select(
    [ship == 'Same Day', ship == 'First Class', ship == 'Second Class'],
    [rng.integers(0, 1, size=N), rng.integers(1, 3, size=N), rng.integers(2, 5, size=N)],
    default=rng.integers(3, 8, size=N))
ship_date = order_date + pd.to_timedelta(delay, unit='D')

# 数量 / 销售 / 折扣 / 利润
qty = rng.integers(1, 14, size=N)
# 单价按子品类对数正态分布，制造波动
base_price = np.array([UNIT_PRICE[s] for s in sub])
unit_price = base_price * rng.lognormal(0, 0.35, size=N)
sales = (unit_price * qty).round(2)

# 折扣：多数订单无折扣，家具类更容易出现高折扣（制造"折扣侵蚀利润"的真实规律）
furniture_mask = np.array([c == 'Furniture' for c in cat])
p_furniture = np.array([0.38, 0.14, 0.12, 0.10, 0.06, 0.08, 0.06, 0.04, 0.02])
p_other = np.array([0.55, 0.16, 0.12, 0.08, 0.04, 0.03, 0.015, 0.004, 0.001])
p_furniture = p_furniture / p_furniture.sum()
p_other = p_other / p_other.sum()
discount = np.array([
    rng.choice(DISCOUNTS, p=p_furniture if fm else p_other)
    for fm in furniture_mask
])

# 利润 = 销售 * (毛利率 - 折扣 * 0.65) + 噪声
# 折扣按 0.65 系数侵蚀毛利：低毛利 + 高折扣才会亏，整体公司保持盈利
margin = np.array([MARGIN[s] for s in sub])
profit = (sales * (margin - discount * 0.65) + rng.normal(0, sales * 0.03)).round(2)

# 组装 DataFrame
df = pd.DataFrame({
    'Row ID': np.arange(1, N + 1),
    'Order ID': [f"US-{d.year}-{100000 + i}" for i, d in enumerate(order_date)],
    'Order Date': order_date.dt.strftime('%Y-%m-%d'),
    'Ship Date': ship_date.dt.strftime('%Y-%m-%d'),
    'Ship Mode': ship,
    'Customer ID': customer_id,
    'Customer Name': customer_name,
    'Segment': segment,
    'Country': 'United States',
    'City': city,
    'State': state,
    'Postal Code': rng.integers(10000, 99999, size=N),
    'Region': region,
    'Product ID': [f"{'FUR' if c=='Furniture' else 'OFF' if c=='Office Supplies' else 'TEC'}-{s[:2].upper()}-{10000000+i}"
                   for i, (c, s) in enumerate(zip(cat, sub))],
    'Category': cat,
    'Sub-Category': sub,
    'Product Name': [f"{s} {rng.choice(['Deluxe', 'Premium', 'Standard', 'Compact', 'Pro'])} Series" for s in sub],
    'Sales': sales,
    'Quantity': qty,
    'Discount': discount,
    'Profit': profit,
})

# 注入少量数据质量问题（供清洗练习）
# 1) 8 个缺失的邮编
miss = rng.choice(df.index, size=8, replace=False)
df.loc[miss, 'Postal Code'] = np.nan

# 2) 5 行完全重复
dup = df.sample(5, random_state=1)
df = pd.concat([df, dup], ignore_index=True)

# 3) 3 行 Ship Date 早于 Order Date（不合逻辑）
for idx in rng.choice(df.index, size=3, replace=False):
    df.loc[idx, 'Ship Date'] = '2021-12-31'

# 4) 2 行负数量
neg = rng.choice(df.index, size=2, replace=False)
df.loc[neg, 'Quantity'] = -df.loc[neg, 'Quantity']

# 5) 1 个异常大额销售（离群值）
df.loc[df.index[-1], 'Sales'] = 99999.0

# 保存
import os
os.makedirs('data', exist_ok=True)
df.to_csv('data/superstore.csv', index=False, encoding='utf-8-sig')
print(f'已生成 {len(df)} 条记录 -> data/superstore.csv')
print(f'   字段 {len(df.columns)} 个；年份 {df["Order Date"].str[:4].min()}~{df["Order Date"].str[:4].max()}')
print(f'   注入了数据质量问题: 8缺失邮编 / 5重复行 / 3发货早于下单 / 2负数量 / 1离群销售')
