-- Week 1 Day 2
-- SQL Introduction and Basic SELECT Statements

USE fintrust_db;

-- View all customer records

SELECT *
FROM customers;

-- View selected customer information

SELECT
    first_name,
    last_name,
    province
FROM customers;

-- Display customer details with aliases

SELECT
    first_name AS 'First Name',
    last_name AS 'Surname',
    province AS 'Province'
FROM customers;

-- View account balances with a calculated column

SELECT
    account_number,
    account_type,
    balance,
    balance * 1.10 AS projected_balance
FROM accounts;

-- Display first 10 customer records

SELECT
    first_name,
    last_name,
    email
FROM customers
LIMIT 10;

-- List unique provinces

SELECT DISTINCT province
FROM customers;

-- Count customers

SELECT COUNT(*) AS customer_count
FROM customers;

-- Count accounts

SELECT COUNT(*) AS account_count
FROM accounts;

-- Count transactions

SELECT COUNT(*) AS txn_count
FROM transactions;