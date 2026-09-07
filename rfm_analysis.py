# -*- coding: utf-8 -*-
"""
RFM 客户分层：从 MySQL 读 superstore.orders，
算每个客户的 R（最近下单距今几天）/ F（下单次数）/ M（累计消费），
按中位数分高/低，组合成 8 类，输出 Excel + 柱状图。
"""

import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password=input('请输入 MySQL root 密码: '),
    database='superstore',
    charset='utf8mb4',
)

df = pd.read_sql('SELECT * FROM orders', conn)
conn.close()

print(f'读取到 {len(df)} 行订单数据')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# 2. 算 RFM
snapshot = df['Order_Date'].max()
print(f'分析基准日期（数据内最大下单日）: {snapshot.date()}')

rfm = df.groupby('Customer_ID').agg(
    R=('Order_Date', lambda x: (snapshot - x.max()).days),   # 距最近一次下单的天数
    F=('Order_ID', 'nunique'),                               # 下单次数（去重订单号）
    M=('Sales', 'sum'),                                      # 累计消费
).reset_index()

# 3. 打分：按中位数分高/低
rfm['R_hi'] = np.where(rfm['R'] <= rfm['R'].median(), 1, 0)  # R 越小越好 → 最近=1
rfm['F_hi'] = np.where(rfm['F'] >= rfm['F'].median(), 1, 0)  # F 越大越好
rfm['M_hi'] = np.where(rfm['M'] >= rfm['M'].median(), 1, 0)  # M 越大越好

# 4. 组合成 8 类
seg_map = {
    # (R_hi, F_hi, M_hi) → 标签
    (1, 1, 1): '重要价值客户',
    (1, 1, 0): '潜力客户',
    (1, 0, 1): '重要保持客户',
    (1, 0, 0): '新客户',
    (0, 1, 1): '重要挽留客户',
    (0, 1, 0): '一般客户',
    (0, 0, 1): '重要发展客户',
    (0, 0, 0): '流失客户',
}
rfm['客户分层'] = rfm.apply(
    lambda r: seg_map[(r['R_hi'], r['F_hi'], r['M_hi'])], axis=1)

# 5. 输出结果
print('\n===== RFM 分层结果概览 =====')
summary = rfm.groupby('客户分层').agg(
    客户数=('Customer_ID', 'count'),
    平均累计消费=('M', 'mean'),
    平均下单次数=('F', 'mean'),
    平均距今天数=('R', 'mean'),
).round(0).sort_values('客户数', ascending=False)
print(summary)

# 保存明细 + 汇总到 Excel
out_path = 'RFM客户分层结果.xlsx'
with pd.ExcelWriter(out_path) as writer:
    rfm[['Customer_ID', 'R', 'F', 'M', '客户分层']].to_excel(
        writer, sheet_name='客户明细', index=False)
    summary.to_excel(writer, sheet_name='分层汇总')
print(f'\n结果已保存到: {out_path}')

# 6. 画分层柱状图
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False

counts = rfm['客户分层'].value_counts().reindex(seg_map.values(), fill_value=0)
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(counts)))

fig, ax = plt.subplots(figsize=(10, 5))
counts.plot(kind='bar', color=colors, ax=ax)
ax.set_title('RFM 客户分层：各类客户数量', fontsize=14, fontweight='bold')
ax.set_ylabel('客户数')
ax.set_xlabel('')
plt.xticks(rotation=30, ha='right')
for i, v in enumerate(counts):
    ax.text(i, v + 1, str(v), ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('图4_RFM分层.png', dpi=150)
plt.show()
print('已生成分层柱状图: 图4_RFM分层.png')
