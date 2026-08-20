-- Week 1 Day 2: Basic SELECT lab

USE fintrust;

-- Exercise 1: List customers by province.
SELECT first_name, last_name, province
FROM customers
ORDER BY province, last_name;

-- Exercise 2: Show the first 20 savings accounts.
SELECT account_number, account_type, balance
FROM accounts
WHERE account_type = 'SAVINGS'
LIMIT 20;

-- Exercise 3: List unique customer provinces.
SELECT DISTINCT province
FROM customers
ORDER BY province;

-- Exercise 4: Project each account balance after 10% interest.
SELECT
    account_number,
    balance,
    balance * 1.10 AS projected_balance
FROM accounts;

-- Exercise 5: Count all accounts.
SELECT COUNT(*) AS total_accounts
FROM accounts;
