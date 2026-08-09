-- Week 1 Day 2 — Basic SELECT Lab Exercises

-- Exercise 1: List the first and last name of every customer, plus their province. Order by province alphabetically.
SELECT first_name, last_name, province
FROM customers
ORDER BY province ASC;

-- Exercise 2: Show the account number, account type, and current balance for all SAVINGS accounts. Show only the first 20 results.
SELECT account_number, account_type, balance
FROM accounts
WHERE account_type = 'SAVINGS'
LIMIT 20;

-- Exercise 3: List all unique provinces that have FinTrust customers.
SELECT DISTINCT province FROM customers;

-- Exercise 4: Calculate the total balance potential (balance + 10% interest for one year) for every account. Label the column `projected_balance`.
SELECT 
  account_number,
  balance,
  balance * 0.10 AS one_year_interest,
  balance * 1.10 AS projected_balance
FROM accounts;

-- Exercise 5: How many accounts are in the accounts table?
SELECT COUNT(*) AS total_accounts FROM accounts;
