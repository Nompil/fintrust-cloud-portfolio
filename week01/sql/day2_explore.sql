-- Week 1 Day 2: Explore the FinTrust sample data

USE fintrust;

-- 1. View all customers.
SELECT *
FROM customers;

-- 2. List customer names and provinces alphabetically by surname.
SELECT first_name, last_name, province
FROM customers
ORDER BY last_name;

-- 3. Show active account balances from highest to lowest.
SELECT account_number, account_type, balance
FROM accounts
WHERE status = 'ACTIVE'
ORDER BY balance DESC;

-- 4. List the represented provinces.
SELECT DISTINCT province
FROM customers
ORDER BY province;

-- 5. Calculate the total balance across active accounts.
SELECT SUM(balance) AS total_balance
FROM accounts
WHERE status = 'ACTIVE';
