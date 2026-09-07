CREATE DATABASE IF NOT EXISTS superstore
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE superstore;

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    Row_ID          INT,
    Order_ID        VARCHAR(20),
    Order_Date      DATE,
    Ship_Date       DATE,
    Ship_Mode       VARCHAR(20),
    Customer_ID     VARCHAR(15),
    Customer_Name   VARCHAR(60),
    Segment         VARCHAR(20),
    Country         VARCHAR(20),
    City            VARCHAR(40),
    State           VARCHAR(40),
    Postal_Code     INT NULL,          
    Region          VARCHAR(10),
    Product_ID      VARCHAR(20),
    Category        VARCHAR(20),
    Sub_Category    VARCHAR(20),
    Product_Name    VARCHAR(120),
    Sales           DECIMAL(10, 2),
    Quantity        INT,
    Discount        DECIMAL(3, 2),
    Profit          DECIMAL(10, 2)
);

-- 验证建表成功
SELECT COUNT(*) AS 表是否为空_应为0 FROM orders;
