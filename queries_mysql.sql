
SELECT * 
FROM superstore.orders LIMIT 10;
SELECT Order_ID, Order_Date, Category, Sub_Category, Sales, Discount, Profit
FROM superstore.orders LIMIT 10;

-- 总订单数、总销售额、总利润、利润率
SELECT
    COUNT(*)                                   AS 订单数,
    ROUND(SUM(Sales), 0)                       AS 总销售额,
    ROUND(SUM(Profit), 0)                      AS 总利润,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1)   AS 利润率_pct
FROM superstore.orders;

-- 按年份看趋势（逐年增长了吗？）
SELECT
    YEAR(Order_Date)            AS 年份,
    ROUND(SUM(Sales), 0)        AS 销售额,
    ROUND(SUM(Profit), 0)       AS 利润
FROM superstore.orders
GROUP BY 年份
ORDER BY 年份;

-- 按月份看趋势（Q4 是旺季吗？）
SELECT
    DATE_FORMAT(Order_Date, '%Y-%m') AS 月份,
    ROUND(SUM(Sales), 0)             AS 销售额
FROM superstore.orders
GROUP BY 月份
ORDER BY 月份;

-- 按品类看利润
SELECT
    Category,
    ROUND(SUM(Sales), 0)    AS 销售额,
    ROUND(SUM(Profit), 0)   AS 利润,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS 利润率_pct
FROM superstore.orders
GROUP BY Category
ORDER BY 利润率_pct;

-- 按子品类看（哪个子品类在亏钱？）
SELECT
    Sub_Category,
    ROUND(SUM(Sales), 0)    AS 销售额,
    ROUND(SUM(Profit), 0)   AS 利润,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS 利润率_pct
FROM superstore.orders
GROUP BY Sub_Category
ORDER BY 利润率_pct;

-- 按地区看（哪个地区亏钱？）
SELECT
    Region,
    ROUND(SUM(Sales), 0)    AS 销售额,
    ROUND(SUM(Profit), 0)   AS 利润,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS 利润率_pct
FROM superstore.orders
GROUP BY Region
ORDER BY 利润率_pct;

-- 找出所有亏损订单，看它们的共同点
SELECT Order_ID, Category, Sub_Category, Discount, Sales, Profit
FROM superstore.orders
WHERE Profit < 0
ORDER BY Profit
LIMIT 20;

-- 不同折扣档位下，利润如何变化？
SELECT
    Discount,
    COUNT(*)                AS 订单数,
    ROUND(AVG(Profit), 1)   AS 平均利润,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS 利润率_pct
FROM superstore.orders
GROUP BY Discount
ORDER BY Discount;

-- 每个客户累计消费排名（前 10 名高价值客户）
SELECT
    Customer_Name,
    ROUND(SUM(Sales), 0) AS 累计消费,
    RANK() OVER (ORDER BY SUM(Sales) DESC) AS 排名
FROM superstore.orders
GROUP BY Customer_Name
ORDER BY 排名
LIMIT 10;

-- 每月销售额 + 环比上月（窗口函数 LAG）
SELECT
    月份,
    销售额,
    ROUND((销售额 - LAG(销售额) OVER (ORDER BY 月份)) * 100.0
          / LAG(销售额) OVER (ORDER BY 月份), 1) AS 环比_pct
FROM (
    SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS 月份, ROUND(SUM(Sales), 0) AS 销售额
    FROM superstore.orders
    GROUP BY 月份
) t
ORDER BY 月份;


