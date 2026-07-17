-- INNER JOIN between customers and accounts

SELECT
    c.customer_id,
    c.customer_name,
    a.account_number
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id;

-- LEFT JOIN showing all customers

SELECT
    c.customer_id,
    c.customer_name,
    a.account_number
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id;

-- JOIN across customers, accounts and transactions

SELECT
    c.customer_name,
    a.account_number,
    t.transaction_amount
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN transactions t
    ON a.account_id = t.account_id;