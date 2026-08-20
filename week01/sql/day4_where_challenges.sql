-- Week 1 Day 4: WHERE practical-guide challenges

USE fintrust_db;

-- Customer coverage outside the two largest portfolio regions.
SELECT *
FROM customers
WHERE province NOT IN ('Gauteng', 'Western Cape');

-- Mid-balance cheque and savings accounts for product analysis.
SELECT *
FROM accounts
WHERE balance BETWEEN 1000 AND 20000
  AND account_type IN ('CHEQUE', 'SAVINGS');

-- Food-related transactions above R200 for spending analysis.
SELECT *
FROM transactions
WHERE (
        merchant_category LIKE '%Food%'
        OR merchant_category LIKE '%Groceries%'
    )
  AND amount > 200;

-- Debit transactions needing category-data quality review.
SELECT *
FROM transactions
WHERE transaction_type = 'DEBIT'
  AND merchant_category IS NULL
  AND amount > 100;

-- Contactable customers with common email domains and a known province.
SELECT *
FROM customers
WHERE (
        email LIKE '%.co.za'
        OR email LIKE '%.com'
    )
  AND province IS NOT NULL
ORDER BY last_name;
