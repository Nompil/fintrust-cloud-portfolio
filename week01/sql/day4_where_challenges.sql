-- Find all customers NOT from Gauteng or Western Cape.

SELECT *
FROM customers
WHERE province NOT IN ('Gauteng', 'Western Cape');

-- Find all accounts with a balance between R1000 and R20000
-- inclusive, of type CHEQUE or SAVINGS.

SELECT *
FROM accounts
WHERE balance BETWEEN 1000 AND 20000
AND account_type IN ('CHEQUE', 'SAVINGS');

-- Find all transactions with a merchant category that
-- contains the word Food OR Groceries,
-- for amounts over R200.

SELECT *
FROM transactions
WHERE
(
    merchant_category LIKE '%Food%'
    OR merchant_category LIKE '%Groceries%'
)
AND amount > 200;

-- Find DEBIT transactions where no merchant category
-- was recorded and the amount is greater than R100.

SELECT *
FROM transactions
WHERE transaction_type = 'DEBIT'
AND merchant_category IS NULL
AND amount > 100;

-- Find customers whose email ends in .co.za or .com,
-- ordered by last name ascending,
-- and who have their province recorded.

SELECT *
FROM customers
WHERE
(
    email LIKE '%.co.za'
    OR email LIKE '%.com'
)
AND province IS NOT NULL
ORDER BY last_name ASC;
