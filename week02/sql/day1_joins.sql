-- =====================================
-- Exercise 1
-- Customer accounts with balances
-- =====================================

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;


-- =====================================
-- Exercise 2
-- Gauteng customers with balances > 25000
-- =====================================

SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng'
  AND a.balance > 25000
ORDER BY a.balance DESC;


-- =====================================
-- Exercise 3
-- Three-table JOIN
-- Debit transactions only
-- =====================================

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    t.amount,
    t.transaction_date,
    t.transaction_type
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'debit'
ORDER BY t.transaction_date DESC;


-- =====================================
-- Exercise 4
-- Customers with no transactions
-- LEFT JOIN + IS NULL
-- =====================================

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL;


-- =====================================
-- Exercise 5
-- Transactions > R10000
-- Western Cape or KwaZulu-Natal
-- =====================================

SELECT
    c.first_name,
    c.last_name,
    c.province,
    t.amount
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.amount > 10000
  AND c.province IN ('Western Cape', 'KwaZulu-Natal')
ORDER BY t.amount DESC;