-- Week 1 Day 4: WHERE practice and business-report queries

USE fintrust_db;

-- Practice 1: Customers from Gauteng.
SELECT *
FROM customers
WHERE province = 'Gauteng';

-- Practice 2: Accounts with balances above R5,000.
SELECT *
FROM accounts
WHERE balance > 5000;

-- Practice 3: Customers with a .co.za email address.
SELECT *
FROM customers
WHERE email LIKE '%.co.za';

-- Practice 4: Debit or payment transactions, using IN.
SELECT *
FROM transactions
WHERE transaction_type IN ('DEBIT', 'PAYMENT');

-- Practice 5: Savings accounts between R1,000 and R50,000.
SELECT *
FROM accounts
WHERE account_type = 'SAVINGS'
  AND balance BETWEEN 1000 AND 50000;

-- Practice 6: Transactions with a recorded merchant category.
SELECT *
FROM transactions
WHERE merchant_category IS NOT NULL;

-- Report 1: Gauteng customers for a regional campaign.
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE province = 'Gauteng'
ORDER BY last_name;

-- Report 2: Accounts above R10,000 for risk monitoring.
SELECT account_id, account_number, account_type, balance
FROM accounts
WHERE balance > 10000
ORDER BY balance DESC;

-- Report 3: Savings accounts for a product rollout.
SELECT account_id, customer_id, account_number, balance
FROM accounts
WHERE account_type = 'SAVINGS'
ORDER BY balance DESC;

-- Report 4: Grocery transactions above R500 for fraud review.
SELECT transaction_id, account_id, amount, transaction_type, transaction_date
FROM transactions
WHERE merchant_category = 'Groceries'
  AND amount > 500
ORDER BY amount DESC;

-- Report 5: Customers with Gmail addresses.
SELECT first_name, last_name, email
FROM customers
WHERE email LIKE '%gmail%'
ORDER BY last_name;

-- Stretch report: High-value debit activity for transaction monitoring.
SELECT transaction_id, account_id, amount, merchant_category, transaction_date
FROM transactions
WHERE transaction_type = 'DEBIT'
  AND amount >= 1000
ORDER BY amount DESC;
